# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos7-base:latest

RUN pip install flask-restful
RUN pip install requests
RUN pip install flask-cors
RUN pip install pika
RUN yum install -y MySQL-python

COPY ./conf /storage/conf/
COPY ./common /storage/common/
COPY ./storage /storage/storage/

CMD python /storage/storage/restserver/restapi_server.py & python /storage/storage/rpcserver/rpcapi_callserver.py & python /storage/storage/service/storage_service.py
