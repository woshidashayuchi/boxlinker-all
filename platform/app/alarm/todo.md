* 提供接口,设置告警相关信息
  1. 纵向维度:
     1) namespace
     2) service
  2. 横向维度:
     1) cpu
     2) memory
     3) network
     4) storage
  3. 告警阈值
     cpu: %, memory: num, network: xxx, storage: G
  4. 告警时间间隔(默认: 2h)


* 数据库表
  1. 当前告警状态(是否正在告警)
  2. 更新时间