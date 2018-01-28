# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos7-base:latest

RUN pip install flask-restful
RUN pip install requests
RUN pip install flask-cors
RUN pip install pika
RUN pip install pycrypto
RUN yum install -y MySQL-python

COPY ./conf /ucenter/conf/
COPY ./common /billing/common/
COPY ./billing /billing/billing/

CMD python /billing/billing/restserver/restapi_server.py & python /billing/billing/rpcserver/rpcapi_callserver.py & python /billing/billing/rpcserver/rpcapi_castserver.py & python /billing/billing/service/billing_service.py
