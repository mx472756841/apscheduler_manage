# 背景
APScheduler是一个非常好用的调度平台，不过目前所有Scheduler的JOB信息都无法通过可视化的方式展示，只能通过后台日志来查看调度信息，管理上非常不便。

但APScheduler扩展及预留非常多，其预留的event功能可以来实现job的生命周期跟踪。

另外APScheduler的Scheduler也可以实现动态的增删查job等操作，可以提前定义一些job，在web上快速方便的添加一些调度任务等。

# 目标
- [x] 跟踪所有job状态及生命周期
- [ ] web页动态增删job调度

# 部署
## virtualenv部署
```buildoutcfg
ubuntu 上要先安装python3.8
具体可参考资料 https://www.jb51.net/article/182392.htm
安装完成python3.8之后，配套安装python3.8需要的虚拟环境创建工具
sudo apt install python3.8-venv
python3.8 -m venv <准备创建虚拟环境的路径>
```
1. python3.8 venv venv
2. . venv/bin/activate
3. pip install -r requirements.txt
4. gunicorn -c etc/gunicorn.py manage:app [记得要配置好数据库]

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
docker run -p 10050:5000 -i -t -d \
    --name apscheduler apscheduler
```