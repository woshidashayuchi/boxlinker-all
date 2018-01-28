# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos-base:latest

COPY MariaDB.repo /etc/yum.repos.d/

RUN yes | cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN yum update -y && yum install -y MariaDB-server
RUN yum install -y telnet

