FROM python:3.8.8-alpine3.12

# 构建本地代码
COPY / /apscheduler_manage/

WORKDIR /apscheduler_manage/

RUN echo Asia/Shanghai > /etc/timezone

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5000