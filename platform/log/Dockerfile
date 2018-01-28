# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos7-base:latest

RUN pip install flask-restful
RUN pip install requests
RUN pip install flask-cors
RUN pip install pika
RUN yum install -y MySQL-python

COPY ./conf /log/conf/
COPY ./common /log/common/
COPY ./log /log/log/

CMD python /log/log/restserver/restapi_server.py & python /log/log/rpcserver/rpcapi_callserver.py
