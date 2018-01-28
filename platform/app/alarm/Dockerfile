FROM index.boxlinker.com/boxlinker/centos7-base:latest
MAINTAINER xiaofengwang
RUN easy_install sqlalchemy

#RUN easy_install flask
RUN pip install flask-restful

#RUN easy_install flask_cors==3.0.0
RUN pip install flask-cors

#RUN easy_install requests
RUN pip install requests
RUN easy_install pika
RUN easy_install pymysql
RUN yum install MySQL-python -y
RUN yum install -y net-snmp*
COPY ./alarm /data/
EXPOSE 9000
CMD python /data/alarm/service/device_resources_service.py
# python /data/alarm/service/service.py & python /data/alarm/restserver/restapi_server.py & python /data/alarm/rpcserver/rpcapi_callserver.py