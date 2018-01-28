#### 签约支付宝当面付
参考[扫码支付接入指引](https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7629140.0.0.5d3mVW&treeId=194&articleId=106078&docType=1)
1. 创建应用并获取APPID

  要在您的应用中使用支付宝开放产品的接口能力，您需要先去蚂蚁金服开放平台（open.alipay.com），在管理中心中创建登记您的应用，并提交审核，审核通过后会为您生成应用唯一标识（APPID），并且可以申请开通开放产品使用权限，通过APPID您的应用才能调用开放产品的接口能力。需要详细了解开放平台创建应用步骤请参考[《开放平台应用创建指南》](https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.f06vVz&treeId=200&articleId=105308&docType=1)。

  - 主要需要配合完成的工作 : 创建应用
  - 需要反馈的信息: APPID 格式例如 ：2017030105981334

2. 配置密钥

  开发者调用接口前需要先生成RSA密钥，RSA密钥包含应用私钥(APP_PRIVATE_KEY)、应用公钥(APP_PUBLIC_KEY）。生成密钥后在开放平台管理中心进行密钥配置，配置完成后可以获取支付宝公钥(ALIPAY_PUBLIC_KEY)。详细步骤请参考[《配置应用环境》](https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.XZAA3d&treeId=200&articleId=105310&docType=1)。

  - 主要需要配合完成的工作 :
 | 1. 完善应用信息, 并通过审核   
 | 2. 设置应用公钥, 生成应用公钥的方式，请查看[签名专区](https://doc.open.alipay.com/docs/doc.htm?treeId=291&articleId=105971&docType=1)
  - 需要反馈的信息 :
 | 1. 支付宝公钥
 | 2. 应用私钥
 | 3. 应用公钥(上传到支付宝)

