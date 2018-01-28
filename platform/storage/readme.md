存储服务

1.创建存储服务镜像

# docker build -t index.boxlinker.com/boxlinker/storage:1.0.1 ./

2.启动存储服务

修改storage_conf.yaml文件中环境变量值，启动存储服务

# kubectl create -f storage_conf.yaml
