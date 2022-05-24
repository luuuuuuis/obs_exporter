#!python3
# -*- encoding: utf-8 -*-
'''
@File    :   obs_exporter.py
@Time    :   2022/05/20 22:21:23
@Author  :   Luis
@Version :   1.0
@Contact :   luis9527@163.com
'''

import argparse
import os
import sys
import configparser
from obs import ObsClient, LogConf, ObsClient
from prometheus_client import start_http_server, Gauge
from threading import Thread
import time

# 定义版本
def get_version():
    return 'v1.0.0'

# 定义传入的参数
description = "\033[33m Welcome To Use Obs Exporter\033[0m"
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v', '--version', action='version', version=get_version(),help='查看版本')
parser.add_argument('-c', '--config_file', type=str, default='.obs.ini', help='指定配置文件；不填默认为：\033[32m .obs.ini\033[0m')
parser.add_argument('-l', '--log_config', type=str, default='log.conf', help='指定日志配置文件；不填默认为：\033[32m log.conf\033[0m')
args = parser.parse_args()
configPath = args.config_file
logConfigPath = args.log_config


# 获取当前目录文件
root_dir = os.path.abspath('.')
# 拼接配置文件路径
if os.path.isabs(configPath):
    coniniPath = configPath
else:
    coniniPath = os.path.join(root_dir, configPath)
# 拼接日志配置文件路径
if os.path.isabs(logConfigPath):
    finalLogConfigPath = logConfigPath
else:
    finalLogConfigPath = os.path.join(root_dir, logConfigPath)

# 实例化configParser对象
config = configparser.ConfigParser()
config.read(coniniPath,encoding='utf8')
port = int(config.get('obs', 'port'))
obsEndpoint = str(config.get('obs', 'obsEndpoint'))
bucketName = str(config.get('obs', 'bucketName'))
AK = str(config.get('obs', 'AK'))
SK = str(config.get('obs', 'SK'))

# 创建连接对应Obs的客户端
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=obsEndpoint)
# 创建连接对应桶的客户端
bucketClient = obsClient.bucketClient(bucketName)

# 开启日志
# 指定日志配置文件路径，初始化ObsClient日志
obsClient.initLog(LogConf(finalLogConfigPath), 'obs_logger')

#定义数据类型，metric，describe(描述)，标签
obs_bucket_max_bytes = Gauge('obs_bucket_max_bytes','Maximum capacity of Huawei OBS bucket', ['bucket', 'endpoint'],)
obs_bucket_used_bytes = Gauge('obs_bucket_used_bytes','Used capacity of Huawei OBS bucket', ['bucket', 'endpoint'],)
obs_bucket_object_total = Gauge('obs_bucket_object_total','Object Number total of Huawei OBS bucket', ['bucket', 'endpoint'],)
obs_bucket_object_write_success = Gauge('obs_bucket_object_write_success','Huawei cloud OBS bucket object writable', ['bucket', 'endpoint'],)
obs_bucket_object_read_success = Gauge('obs_bucket_object_read_success','Huawei cloud OBS bucket object readable', ['bucket', 'endpoint'],)

# 获取桶配额
def getBucketQuota():
    # print('getBucketQuota')
    try: 
        resp = bucketClient.getBucketQuota()     
        if resp.status < 300: 
            bucketQuota = int(resp.body.quota)
            # print(bucketQuota)
            obs_bucket_max_bytes.labels(bucket=bucketName, endpoint=obsEndpoint).set(bucketQuota)
        else: 
            print('errorCode:', resp.errorCode) 
            print('errorMessage:', resp.errorMessage)
    except:    
        import traceback    
        print(traceback.format_exc())

# 获取桶存量信息
def getBucketStorageInfo():
    # print('getBucketStorageInfo')
    try: 
        resp = bucketClient.getBucketStorageInfo()
        if resp.status < 300:
            bucketMemoryUsed = int(resp.body['size'])
            bucketObjectNum = int(resp.body['objectNumber'])
            obs_bucket_used_bytes.labels(bucket=bucketName, endpoint=obsEndpoint).set(bucketMemoryUsed)
            obs_bucket_object_total.labels(bucket=bucketName, endpoint=obsEndpoint).set(bucketObjectNum)
            # print(bucketMemoryUsed, bucketObjectNum)
        else:
            print(resp.errorCode)
    except:    
        import traceback    
        print(traceback.format_exc())

# 测试写功能
def getObjectWritable():
    # print('getObjectWritable')
    try:
        resp = bucketClient.putContent(objectKey='forwritabletest.txt', content='A writable test')
            
        if resp.status < 300: 
            objectWritable = 1
            # print(objectWritable)
            obs_bucket_object_write_success.labels(bucket=bucketName, endpoint=obsEndpoint).set(objectWritable)
        else: 
            print('errorCode:', resp.errorCode) 
            print('errorMessage:', resp.errorMessage)
            objectWritable = 0
            obs_bucket_object_write_success.labels(bucket=bucketName, endpoint=obsEndpoint).set(objectWritable)
    except:
        import traceback
        print(traceback.format_exc())

# 测试读功能
def getObjectReadable():
    # print('getObjectReadable')
    try:
        resp = bucketClient.getObject(objectKey='forwritabletest.txt' ,downloadPath='./forwritabletest.txt') 
            
        if resp.status < 300: 
            objectReadable = 1
            # print(objectReadable)
            obs_bucket_object_read_success.labels(bucket=bucketName, endpoint=obsEndpoint).set(objectReadable)
        else: 
            print('errorCode:', resp.errorCode) 
            print('errorMessage:', resp.errorMessage)
            objectReadable = 0
            obs_bucket_object_read_success.labels(bucket=bucketName, endpoint=obsEndpoint).set(objectReadable)
    except:
        import traceback
        print(traceback.format_exc())

func_list = [getBucketQuota, getBucketStorageInfo, getObjectWritable, getObjectReadable]

if __name__ == "__main__":
 #暴露端口
    start_http_server(port=port)  
 #不断传入数据
    while True:
        threads = []
        for i in func_list:
            t = Thread(target=i)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print('采集完毕！')
        time.sleep(5)
