# 一、快速开始
## 1、解压
```bash
$ tar -xvf obs_exporter-1.0.0.linux-amd64.tar.gz
```
## 2、进入安装目录
```bash
$ cd obs_exporter
```
## 3、修改配置文件`.obs.ini`
```bash
$ vi .obs.ini
```
```ini
[obs]
port= 9527  #监听的端口
obsEndpoint = http://xxx.xxx.xxx.xxx    #服务地址
bucketName = xxxxxx #桶名
AK = xxxxxxxxxxxxx  #Access Key ID，接入键标识
SK = xxxxxxxxxxxxxxxxxx #Secret Access Key，安全接入键
```
修改完后按`Esc`退出编辑，然后输入`:wq`保存并退出
## 4、启动服务
```bash
$ ./obs_exporter
```
>以上启动方式仅限于在安装目录，默认配置文件为`.obs.ini`,日志配置文件为`log.conf`

当然，你也可以以指定配置文件以及日志配置文件的形式启动
```bash
$ ${'安装目录'}/obs_exporter --config_file ${'配置文件所在目录'}/.obs.ini --log_config ${'日志配置文件所在目录'}/log.conf
```
>配置文件和日志配置文件名称支持自定义，但建议将配置文件设置为隐藏文件

>配置文件和日志配置文件支持绝对路径和相对路径
## 5、检查服务
```bash
$ ps -ef | grep obs_exporter
```
## 6、检查日志
```bash
$ tail -f ${'安装目录'}/logs/OBS.log
```
```log
2022-05-24 11:43:21,473|process:13683|thread:139935421814528|INFO|HTTP(s)+XML|obs_logger|_wrapperFinally,97|getObject cost 6 ms|
2022-05-24 11:43:21,536|process:13683|thread:139935413421824|INFO|HTTP(s)+XML|obs_logger|do_close,358|server inform to close connection|
2022-05-24 11:43:21,536|process:13683|thread:139935413421824|INFO|HTTP(s)+XML|obs_logger|_wrapperFinally,97|getBucketStorageInfo cost 72 ms|
2022-05-24 11:43:21,537|process:13683|thread:139935193491200|INFO|HTTP(s)+XML|obs_logger|do_close,358|server inform to close connection|
2022-05-24 11:43:21,538|process:13683|thread:139935193491200|INFO|HTTP(s)+XML|obs_logger|_wrapperFinally,97|putContent cost 73 ms|
```
# 二、使用说明
## 1、关于安装目录下的几个文件
启动前
```bash
$ tree -a ./
./
├── log.conf
├── obs_exporter
└── .obs.ini
```
>`obs_exporter`：采集程序

>`.obs.ini`：配置文件，里面记录被采集obs的相关信息

>`log.conf`：日志配置文件，里面记录采集程序日志的输出格式等

启动后
```bash
$ tree -a ./
./
├── forwritabletest.txt
├── log.conf
├── logs
│   └── OBS.log
├── obs_exporter
└── .obs.ini
```
新增文件如下
>`forwritabletest.txt`：用于测试obs读写功能产生的测试文件

>`logs/OBS.log`：日志文件，里面记录了每次访问obs的日志

## 2、采集的指标说明
```bash
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 724.0
python_gc_objects_collected_total{generation="1"} 278.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 70.0
python_gc_collections_total{generation="1"} 6.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="5",version="3.9.5"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 7.33618176e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.5821184e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.6532886629e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 1.27
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 8.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 655360.0
# HELP obs_bucket_max_bytes Maximum capacity of Huawei OBS bucket
# TYPE obs_bucket_max_bytes gauge
obs_bucket_max_bytes{bucket="xxxxxx",endpoint="http://xxx.xxx.xxx.xxx"} 5.36870912e+011
# HELP obs_bucket_used_bytes Used capacity of Huawei OBS bucket
# TYPE obs_bucket_used_bytes gauge
obs_bucket_used_bytes{bucket="xxxxxx",endpoint="http://xxx.xxx.xxx.xxx"} 4.309656907e+010
# HELP obs_bucket_object_total Object Number total of Huawei OBS bucket
# TYPE obs_bucket_object_total gauge
obs_bucket_object_total{bucket="xxxxxx",endpoint="http://xxx.xxx.xxx.xxx"} 479615.0
# HELP obs_bucket_object_write_success Huawei cloud OBS bucket object writable
# TYPE obs_bucket_object_write_success gauge
obs_bucket_object_write_success{bucket="xxxxxx",endpoint="http://xxx.xxx.xxx.xxx"} 1.0
# HELP obs_bucket_object_read_success Huawei cloud OBS bucket object readable
# TYPE obs_bucket_object_read_success gauge
obs_bucket_object_read_success{bucket="xxxxxx",endpoint="http://xxx.xxx.xxx.xxx"} 1.0
```
| 指标                 |数据类型    | 含义              | 说明            |
| -------------------- | ---------- | ---------------- | ---------------- |
| obs_bucket_max_bytes |  Gauge     |桶的配额（桶的最大容量） | - |
| obs_bucket_used_bytes |  Gauge    |桶当前使用量 | - |
| obs_bucket_object_total |  Gauge    |桶当前对象数量 | 一个文件即视为一个对象 |
| obs_bucket_object_write_success |  Gauge    |桶的可写性 | `1`代表正常，`0`代表异常 |
| obs_bucket_object_read_success |  Gauge    |桶的可读性 | `1`代表正常，`0`代表异常 |
## 3、Prometheus配置参考
```bash
vi prometheus.yml
```
```yaml
  - job_name: "obs_exporter"
    static_configs:
    - targets:
      - '19.15.xx.xx:9202'
      labels:
        server: 大数据服务平台
```
