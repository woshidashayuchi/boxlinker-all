# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos7-base:latest

RUN pip install flask-restful
RUN pip install requests
RUN pip install flask-cors
RUN pip install pika
RUN yum install -y MySQL-python

COPY ./conf /security/conf/
COPY ./common /security/common/
COPY ./security /security/security/

CMD python /security/security/restserver/restapi_server.py & python /security/security/rpcserver/rpcapi_callserver.py & python /security/security/rpcserver/rpcapi_castserver.py
