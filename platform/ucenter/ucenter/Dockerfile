# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos7-base:latest

RUN pip install flask-restful
RUN pip install requests
RUN pip install flask-cors
RUN pip install pika
RUN yum install -y MySQL-python

COPY ./conf /ucenter/conf/
COPY ./common /ucenter/common/
COPY ./ucenter /ucenter/ucenter/

CMD python /ucenter/ucenter/restserver/restapi_server.py & python /ucenter/ucenter/rpcserver/rpcapi_callserver.py
