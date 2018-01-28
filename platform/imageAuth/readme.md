用户中心服务

1.消息队列启动

# docker run -itd -h rabbitmq -p 127.0.0.1:5672:5672 index.boxlinker.com/library/rabbitmq
# docker run -itd -h rabbitmq -p 5672:5672 index.boxlinker.com/library/rabbitmq

2.数据库启动

# docker run -itd -h mariadb -v /database:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=ucenter -p 127.0.0.1:3306:3306 index.boxlinker.com/library/mariadb

3.构建用户中心服务镜像

# docker build -t index.boxlinker.com/boxlinker/ucenter:1.0.1 ./

4.启动用户中心服务

修改ucenter.yaml文件中环境变量值，启动存储服务

# kubectl create -f ucenter.yaml
