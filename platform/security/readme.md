安全服务

1.创建安全服务镜像

# docker build -t index.boxlinker.com/boxlinker/security:1.0.1 ./

2.启动安全服务

修改security_conf.yaml文件中环境变量值，启动安全服务

# kubectl create -f security_conf.yaml
