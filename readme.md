# Boxlinker

#### 文件结构说明

* `deploy` 环境部署
    - k8s k8s 环境部署脚本
    - storage 分布式存储环境部署脚本
* `platform` 平台相关服务模块
    - email 邮件
    - loadbalancer 负载均衡
    - log 日志
    - monitor 监控报警
    - registry 镜像库
    - rolling-update 滚动更新
    - service k8s 服务
    - storage 存储
    - user 用户 组织
    - verify-code 验证码
    - web 前端
    
#### 生成 doc
    make doc
