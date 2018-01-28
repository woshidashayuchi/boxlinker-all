日志服务

1.创建日志服务镜像

# docker build -t index.boxlinker.com/boxlinker/log:1.0.1 ./

2.启动日志服务

修改log_conf.yaml文件中环境变量值，启动日志服务

# kubectl create -f log_conf.yaml
