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
COPY ./apprecover /data/
EXPOSE 9000
CMD python /data/apprecover/restserver/restapi_server.py & python /data/apprecover/rpcserver/rpcapi_callserver.py