用户中心

一. 基础服务

1.消息队列启动

# docker run -itd -h rabbitmq -p 127.0.0.1:5672:5672 index.boxlinker.com/library/rabbitmq

2.数据库启动

# docker run -itd -h mariadb -v /database:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=ucenter -p 127.0.0.1:3306:3306 index.boxlinker.com/library/mariadb

二. 用户服务

1.构建用户服务镜像

# docker build -t index.boxlinker.com/boxlinker/ucenter:1.0.1 -f ./ucenter/Dockerfile ./ucenter

2.启动用户服务

修改ucenter.yaml文件中环境变量值，启动存储服务

# kubectl create -f ucenter.yaml

三. 计费服务

1.创建计费服务镜像

# docker build -t index.boxlinker.com/boxlinker/billing:1.0.1 -f ./billing/Dockerfile ./billing

2.启动计费服务

修改billing_conf.yaml文件中环境变量值，启动计费服务

# kubectl create -f billing.yaml
