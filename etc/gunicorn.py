import multiprocessing

bind = ":5000"
# 监听队列数量，64-2048
backlog = 512
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'sync'
# 进程数
workers = multiprocessing.cpu_count()
# 指定每个进程开启的线程数
threads = multiprocessing.cpu_count() * 4
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 访问日志文件
accesslog = "logs/gunicorn_access.log"
# accesslog = '-'
# 错误日志文件
errorlog = "logs/gunicorn_error.log"
# errorlog = '-'
# 进程名
proc_name = 'apscheduler_manage'