FROM python:3.8.8-alpine3.12
MAINTAINER "mx472756841<lanlmeng@qq.com>"

# 构建本地代码
COPY / /apscheduler_manage/

WORKDIR /apscheduler_manage/

# apscheduler对于时区的使用，使用上海时间
RUN echo Asia/Shanghai > /etc/timezone

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5000