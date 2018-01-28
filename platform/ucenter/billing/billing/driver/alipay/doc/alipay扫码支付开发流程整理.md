## 前期准备
### 查看 `需要配合完成的内容.md`

##
1. 支付宝扫码支付介绍[参考支付宝文档-扫码支付](
https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7629140.0.0.ycFhhC&treeId=193&articleId=105170&docType=1#s4)

  - 场景介绍

 | 扫码支付，指用户打开支付宝钱包中的“扫一扫”功能，扫描商户针对每个订单实时生成的订单二维码，并在手机端确认支付。

  - 调用流程

 | ![调用流程](https://img.alicdn.com/top/i1/LB1QKdBLXXXXXcvXXXXXXXXXXXX)
 | 1. 商户系统调用支付宝预下单接口`alipay.trade.precreate`，获得该订单二维码图片地址。

 | 2. 获取支付结果
 |   - 轮询 | 
 |   发起轮询获得支付结果：等待5秒后调用交易查询接口`alipay.trade.query`通过支付时传入的商户订单号(`out_trade_no`)查询支付结果（返回参数`TRADE_STATUS`），如果仍然返回等待用户付款（`WAIT_BUYER_PAY`），则再次等待5秒后继续查询，直到返回确切的支付结果（成功`TRADE_SUCCESS` 或 已撤销关闭`TRADE_CLOSED`），或是超出轮询时间。** 在最后一次查询仍然返回等待用户付款的情况下，必须立即调用交易撤销接口`alipay.trade.cancel`将这笔交易撤销，避免用户继续支付**。

 |   - 异步通知
 |   除了主动轮询，也可以通过接受异步通知获得支付结果，详见[当面付异步通知-仅用于扫码支付](https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7629140.0.0.g2hWXB&treeId=194&articleId=103296&docType=1)，注意一定要对异步通知做验签(详情看第四点 **签验** )，确保通知是支付宝发出的。

2. 退款
  - 场景介绍

 | 商户因业务原因需要退款时，可通过成功交易的商户订单号或支付宝交易号进行退款 ，支持部分退款。

  - 调用流程

 | ![调用流程](https://img.alicdn.com/top/i1/LB1XbK7KVXXXXceaXXXXXXXXXXX)

 | 商户系统调用交易退款接口alipay.trade.refund，传入商户订单号或支付宝交易号、退款请求号、退款金额等参数请求退款，并同步获得退款结果。

 | *特别注意: | 
 | 退款接口会根据外部请求号`out_request_no`幂等返回，因此同一笔需要多次部分退款时，必须使用不同的 out_request_no`*

3. 使用应用私钥生成请求签名
  参考支付宝文档[使用应用私钥生成请求签名](https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7629140.0.0.sCF6QO&treeId=291&articleId=105974&docType=1)
  - 需要把1).APPID，2).应用私钥，3).支付宝公钥，配置在代码中，对请求内容进行签名，并对支付宝返回的内容进行验签。
  由于支付宝并没有提供python的sdk,所以请求签名和对返回内容的验签，必须自行实现。
  - 签名步骤   
  参考支付宝文档[自行实现签名](https://doc.open.alipay.com/docs/doc.htm?docType=1&articleId=106118)
 | 1. 筛选并排序   
 |   获取所有请求参数，不包括字节类型参数，如文件、字节流，剔除sign字段，剔除值为空的参数，并按照第一个字符的键值ASCII码递增排序（字母升序排序），如果遇到相同字符则按照第二个字符的键值ASCII码递增排序，以此类推。
 | 2. 拼接 |  
 |   将排序后的参数与其对应值，组合成“参数=参数值”的格式，并且把这些参数用&字符连接起来，此时生成的字符串为待签名字符串。(两步合成 getSignVeryfy函数)
 | 3.调用签名函数   
 |   使用各自语言对应的SHA256WithRSA(对应sign_type为RSA2)或SHA1WithRSA(对应sign_type为RSA)签名函数利用商户私钥对待签名字符串进行签名，并进行Base64编码
 | 4. 把生成的签名赋值给sign参数，拼接到请求参数中 | 

4. 自行实现验签
 | 参考支付宝文档[异步通知验签](https://doc.open.alipay.com/docs/doc.htm?docType=1&articleId=106120#s1)
 |   - 在用户扫码支付成功后，支付宝会给商户发送异步通知，如果某商户设置的通知地址为https://api.xx.com/receive_notify.htm，对应接收到通知的示例如下
 | ```
 | https://api.xx.com/receive_notify.htm?total_amount=2.00&buyer_id=2088102116773037&body=大乐透2.1&trade_no=2016071921001003030200089909&refund_fee=0.00&notify_time=2016-07-19 14:10:49&subject=大乐透2.1&sign_type=RSA2&charset=utf-8&notify_type=trade_status_sync&out_trade_no=0719141034-6418&gmt_close=2016-07-19 14:10:46&gmt_payment=2016-07-19 14:10:47&trade_status=TRADE_SUCCESS&version=1.0&sign=kPbQIjX+xQc8F0/A6/AocELIjhhZnGbcBN6G4MM/HmfWL4ZiHM6fWl5NQhzXJusaklZ1LFuMo+lHQUELAYeugH8LYFvxnNajOvZhuxNFbN2LhF0l/KL8ANtj8oyPM4NN7Qft2kWJTDJUpQOzCzNnV9hDxh5AaT9FPqRS6ZKxnzM=&gmt_create=2016-07-19 14:10:44&app_id=2015102700040153&seller_id=2088102119685838&notify_id=4a91b7a78a503640467525113fb7d8bg8e
 | ```
 |   -  验签流程：
 |  | 1. 在通知返回参数列表中，除去sign、sign_type两个参数外，凡是通知返回回来的参数皆是待验签的参数。 | 
 |  | 2.将剩下参数进行url_decode, 然后进行字典排序，组成字符串，得到待签名字符串：
 |  | ```
 |  | body=大乐透2.1&buyer_id=2088102116773037&charset=utf-8&gmt_close=2016-07-19 14:10:46&gmt_payment=2016-07-19 14:10:47&notify_time=2016-07-19 14:10:49&notify_type=trade_status_sync&out_trade_no=0719141034-6418&refund_fee=0.00&subject=大乐透2.1&total_amount=2.00&trade_no=2016071921001003030200089909&trade_status=TRADE_SUCCESS&version=1.0
 |  | ```   
 |  | 3. 将签名参数（sign）使用base64解码为字节码串
 |  | 4. 使用RSA的验签方法，通过签名字符串、签名参数（经过base64解码）及支付宝公钥验证签名，根据返回结果判定是否验签通过。
