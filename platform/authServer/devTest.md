
开发环境信息：

M: boxlinker

一. ceph存储

1. mon节点

172.20.1.11 172.20.1.12 172.20.1.21

2. osd节点

172.20.1.13 172.20.1.14 172.20.1.22 172.20.1.23

二. etcd

172.20.1.15 172.20.1.24 172.20.1.25

三. kubernetes节点

1. master节点

172.20.1.16 172.20.1.17 172.20.1.26

2. node节点

172.20.1.18(负责均衡)
172.20.1.18(系统服务) 172.20.1.19 172.20.1.27 172.20.1.28

四. 系统节点：

网关： 192.168.1.8

跳转机： 192.168.1.9

KVM01： 192.168.1.11
KVM02： 192.168.1.12

ucenter: 192.168.1.6

镜像仓库：192.168.1.5

负载均衡：192.168.1.10

# kubectl label node 172.20.1.10 role=loadbalancer
# kubectl label node 172.20.1.18 role=system
# kubectl label node 172.20.1.19 role=user
# kubectl label node 172.20.1.27 role=user
# kubectl label node 172.20.1.28 role=user