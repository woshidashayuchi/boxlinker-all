## Author: YanHua <it-yanh@all-reach.com>
#
#FROM index.boxlinker.com/boxlinker/centos7-base:latest
#
#RUN pip install flask-restful
#RUN pip install requests
#RUN pip install flask-cors
#RUN pip install pika
#RUN yum install -y MySQL-python
#
#RUN pip install sqlalchemy
#
#RUN pip install RSA
#RUN pip install PyJWT
#
#RUN yum install -y libffi-devel
#RUN yum install -y gcc openssl make
#
#RUN yum install -y python-devel
#RUN yum install -y openssl-devel
#
#RUN pip install cryptography
#
#RUN pip install jwt
#
#EXPOSE 8001
#
#RUN echo '/ImageRepo' >> /usr/lib/python2.7/site-packages/mypath.pth
##COPY ./common /ImageRepo/common/
##COPY ./imageAuth /ImageRepo/imageAuth/
##COPY ./conf /ImageRepo/conf/
#
#CMD python /ImageRepo/imageAuth/restserver/restapi_server.py & python /ImageRepo/imageAuth/rpcserver/rpcapi_callserver.py
#
## index.boxlinker.com/boxlinker/alpine:python_2.7.10_pip

FROM index.boxlinker.com/liuzhangpei/python:2.7.10-ubuntu-flask_sup
EXPOSE 8001

RUN echo '/ImageRepo' >> /usr/local/lib/python2.7/site-packages/mypath.pth
#CMD python /ImageRepo/imageAuth/restserver/restapi_server.py & python /ImageRepo/imageAuth/rpcserver/rpcapi_callserver.py

