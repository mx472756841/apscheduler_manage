FROM python:3.6-alpine3.9

# 构建本地代码
COPY / /apscheduler_manage/

WORKDIR /apscheduler_manage/

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 5000