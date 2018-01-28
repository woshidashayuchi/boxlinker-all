FROM index.boxlinker.com/boxlinker/centos7-base:latest
MAINTAINER xiaofengwang
RUN easy_install sqlalchemy
RUN easy_install flask
RUN easy_install flask_cors==3.0.0
RUN easy_install requests
RUN easy_install pika
RUN easy_install pymysql
RUN yum install MySQL-python -y
COPY ./appstatus /data/
CMD python /data/appstatus/service/appstatus_service.py
