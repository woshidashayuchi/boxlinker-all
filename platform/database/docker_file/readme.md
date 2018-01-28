MariaDB集群 Dockerfile

MariaDB集群镜像文件build步骤如下；

1.创建MariaDB基础镜像，该镜像包含MariaDB相关包

# docker build -t index.boxlinker.com/boxlinker/centos-mariadb:cluster-base-1.0.1 ./MariaDB-base

2.创建MariaDB集群节点镜像

# docker build -t index.boxlinker.com/boxlinker/centos-mariadb:cluster-node-1.0.2 ./MariaDB-node

