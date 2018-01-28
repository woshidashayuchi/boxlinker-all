kibana初始化

首次安装的kibana需要添加一个索引

部署完成后，在浏览器中打开kibana界面，然后根据提示进行初始化。
1. 选择Management菜单
2. 【Index name or pattern 】项保持默认配置
3. 【Time-field name】项点击输入框，选择【@timestamp】
4. 点击创建，完成初始化配置。

1. 创建elasticsearch镜像

# docker build -t index.boxlinker.com/boxlinker/elasticsearch:1.0.1 ./
