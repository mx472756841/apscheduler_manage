# 背景
APScheduler是一个非常好用的调度平台，不过目前所有Scheduler的JOB信息都无法通过可视化的方式展示，只能通过后台日志来查看调度信息，管理上非常不便。

但APScheduler扩展及预留非常多，其预留的event功能可以来实现job的生命周期跟踪。

另外APScheduler的Scheduler也可以实现动态的增删查job等操作，可以提前定义一些job，在web上快速方便的添加一些调度任务等，目前Flask-APScheduler库已经将apscheduler中的方法抽象成api接口，开启后直接可以使用

# 目标
- [x] 跟踪所有job状态及生命周期
- [x] web页动态增删job调度

# 部署
## 环境

- python3.8+
```
ubuntu 上要先安装python3.8
```
[可参考资料](https://www.jb51.net/article/182392.htm)

- mysql

## virtualenv部署

```
配套安装python3.8需要的虚拟环境创建工具
sudo apt install python3.8-venv
python3.8 -m venv <准备创建虚拟环境的路径>
```

1. python3.8 -m venv venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. gunicorn -c etc/gunicorn.py manage:app [记得要配置数据库相关信息]

## docker部署
这里没有提供docker镜像，可直接使用Dockerfile从本地生成镜像即可
- 生成镜像

```shell
# 在当前目录执行以下命令
docker build -t apscheduler:latest .
```
- 启动服务

生成镜像之后启动镜像即可
```shell
docker run -p 10050:5000 -v "/etc/localtime:/etc/localtime" \
    -e "DEV_DATABASE_URL=mysql+pymysql://root:realpw@127.0.0.1:3306/testing?charset=utf8mb4" \
    -it -d --name apscheduler apscheduler
```

# 使用
- 动态添加JOB执行

通过config中的参数SCHEDULER_API_ENABLED已经开启flask_apscheduler的api，所以可以直接使用，下面是具体的api信息
```python
def _load_api(self):
    """
    Add the routes for the scheduler API.
    """
    self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
    self._add_url_route('add_job', '/jobs', api.add_job, 'POST')
    self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
    self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
    self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
    self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
    self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
    self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
    self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')
```
直接动态调用接口添加， 具体的参数需要到apscheduler的源码进行查看，就是通过apscheduler add_job的那些参数
```
请求添加接口：http://127.0.0.1:5000/scheduler/jobs
请求方法：POST
请求header:
{
    "Content-Type": "application/json"
}
请求body:
{
    "id": "test_add_job",
    "name":"管理平台添加job测试",
    "func": "app:jobs.test.test_job", # 这里就是模块:函数，本地定义的方法保证可以import
    "trigger": "date" # 触发器为指定时间，这里时间没有指定，就是立马执行
}
返回结果:
{
    "id": "test_add_job",
    "name": "管理平台添加job测试",
    "func": "app:jobs.test.test_job",
    "args": [],
    "kwargs": {},
    "trigger": "date",
    "run_date": "2021-03-05T15:17:10.107210+08:00",
    "misfire_grace_time": 1,
    "max_instances": 1,
    "next_run_time": "2021-03-05T15:17:10.107210+08:00"
}
```

- 监控JOB状态

![](images/1.png)

- 监控JOB执行事件

![](images/2.png)