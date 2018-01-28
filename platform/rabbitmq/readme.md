消息队列服务

1.创建消息队列服务镜像

# docker build -t index.boxlinker.com/boxlinker/centos-rabbitmq:1.0.1 ./

2.启动消息队列服务

# kubectl create -f rabbitmq.yaml
