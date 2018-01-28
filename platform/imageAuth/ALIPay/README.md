# ALIPay
alipay的Python sdk
主要做统一收单方面的sdk
第一步完成统一收单预创建(扫码付)接口([alipay.trade.precreate](https://doc.open.alipay.com/docs/api.htm?spm=a219a.7395905.0.0.KeLae8&docType=4&apiId=862))
签名 验签 代码参考了https://github.com/fzlee/alipay  致谢


使用时 直接把 代码文件ALIPAY.py放到你的项目目录下就可以了

但是签名 验证签名依赖pycrypto(信息安全模块) 请先安装好(pip install pycrypto)
