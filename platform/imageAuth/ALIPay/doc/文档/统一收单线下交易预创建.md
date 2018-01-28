请求参数:   
需要  `aliapy公共请求参数.md` 中的参数     
附加：

参数 | 类型 | 是否必填 | 最大长度 | 描述 | 示例值
--- | --- | --- | --- | --- | ---
out_trade_no | String | 必须 | 64 | 商户订单号,64个字符以内、只能包含字母、数字、下划线；需保证在商户端不重复 | 20150320010101001
seller_id | String | 可选 | 28 | 卖家支付宝用户ID。 如果该值为空，则默认为商户签约账号对应的支付宝用户ID | 2088102146225135
total_amount | Price | 必须 | 11 | 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000] 如果同时传入了【打折金额】，【不可打折金额】，【订单总金额】三者，则必须满足如下条件：【订单总金额】=【打折金额】+【不可打折金额】 | 88.88
discountable_amount | Price | 可选 | 11 | 可打折金额. 参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000] 如果该值未传入，但传入了【订单总金额】，【不可打折金额】则该值默认为【订单总金额】-【不可打折金额】 | 8.88
undiscountable_amount | Price | 可选 | 11 | 不可打折金额. 不参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000] 如果该值未传入，但传入了【订单总金额】,【打折金额】，则该值默认为【订单总金额】-【打折金额】 | 80
subject | String | 必须 | 256 | 订单标题 | Iphone6 16G
body | String | 可选 | 128 | 对交易或商品的描述 | Iphone6 16G
timeout_express | String | 可选 | 6 | 该笔订单允许的最晚付款时间，逾期将关闭交易。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。 该参数数值不接受小数点， 如 1.5h，可转换为 90m。 | 90m
goods_detail | GoodsDetail [] | 可选 | - | 订单包含的商品列表信息.Json格式. 其它说明详见：“商品明细说明” |
└ goods_id | String | 必填 | 32 | 商品的编号 | apple-01
└ alipay_goods_id | String | 可选 | 32 | 支付宝定义的统一商品编号 | 20010001
└ goods_name | String | 必填 | 256 | 商品名称 | ipad
└ quantity | Number | 必填 | 10 | 商品数量 | 1
└ price | Price | 必填 | 9 | 商品单价，单位为元 | 2000
└ goods_category | String | 可选 | 24 | 商品类目 | 34543238
└ body | String | 可选 | 1000 | 商品描述信息 | 特价手机
└ show_url | String | 可选 | 400 | 商品的展示地址 | http://www.alipay.com/xxx.jpg




```
class ALIPrecreatePay(ALITradePay):
    def __init():
        # 必选参数
        self.out_trade_no = ''
        self.total_amount = ''
        self.subject = ''
        self.timeout_express = ''

        # 可选参数
        self.body = ''
        # 不设置则默认商户的签约支付宝id
        self.seller_id = ''

```

响应参数：

参数 | 类型 | 是否必填 | 描述 | 示例值
--- | --- | --- | --- | ---
code | String | 是 | 网关返回码,[详见文档](https://doc.open.alipay.com/docs/doc.htm?treeId=291&articleId=105806&docType=1)(公共请求参数) | 40004
msg | String | 是 | 网关返回码描述(公共请求参数) | Business Failed
sub_code | String | 否 | 业务返回码(当code!=10000时才有)(公共请求参数) | 	ACQ.TRADE_HAS_SUCCESS
sub_msg | String | 否 | 业务返回码描述(当code!=10000时才有)(公共请求参数) | 交易已被支付
sign | String | 是 | 签名,详见文档(公共请求参数) | 略
out_trade_no | String |  是 | 商户的订单号 | 6823789339978248
qr_code | String |  是 | 当前预下单请求生成的二维码码串 | 	https://qr.alipay.com/bavh4wjlxf12tper3a
