FROM index.boxlinker.com/boxlinker/centos7-base:latest
MAINTAINER xiaofengwang
RUN easy_install requests
RUN easy_install pika
RUN easy_install pymysql
RUN yum install MySQL-python -y
ENV TOKEN_PATH /run/secrets/kubernetes.io/serviceaccount/token
COPY ./k8sserver /data/
CMD python /data/k8sserver/kuber_callserver.py & python /data/k8sserver/kuber_castserver.py
