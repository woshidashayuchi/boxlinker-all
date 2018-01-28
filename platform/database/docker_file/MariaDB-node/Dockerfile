# Author: YanHua <it-yanh@all-reach.com>

FROM index.boxlinker.com/boxlinker/centos-mariadb:cluster-base-1.0.1

COPY ./my.cnf /etc/
COPY ./server_cluster.cnf /etc/my.cnf.d/
COPY ./mysql_secure_installation /run/console/
COPY ./run.sh /run/console/

RUN chmod 755 /run/console/run.sh
RUN yes | cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN yum install -y telnet
