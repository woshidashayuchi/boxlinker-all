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
COPY ./k8sapi /data/
EXPOSE 9000
CMD python /data/k8sapi/restserver/restapi_server1.py & python /data/k8sapi/rpcserver/rpcapi_callserver.py & python /data/k8sapi/service/app_service.py
