# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import restapi_define

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from conf import conf


def rest_app_run():

    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)

    api.add_resource(restapi_define.LevelApi,
                     '/api/v1.0/billing/levels')

    api.add_resource(restapi_define.BalanceApi,
                     '/api/v1.0/billing/balances')

    api.add_resource(restapi_define.RechargesApi,
                     '/api/v1.0/billing/recharges')

    api.add_resource(restapi_define.RechargeApi,
                     '/api/v1.0/billing/recharges/<recharge_uuid>')

    api.add_resource(restapi_define.CostsApi,
                     '/api/v1.0/billing/costs')

    api.add_resource(restapi_define.LimitsApi,
                     '/api/v1.0/billing/limits')

    api.add_resource(restapi_define.ResourcesApi,
                     '/api/v1.0/billing/resources')

    api.add_resource(restapi_define.ResourceApi,
                     '/api/v1.0/billing/resources/<resource_uuid>')

    api.add_resource(restapi_define.VouchersApi,
                     '/api/v1.0/billing/vouchers')

    api.add_resource(restapi_define.VoucherApi,
                     '/api/v1.0/billing/vouchers/<voucher_uuid>')

    api.add_resource(restapi_define.BillsAPI,
                     '/api/v1.0/billing/bills')

    api.add_resource(restapi_define.OrdersApi,
                     '/api/v1.0/billing/orders')

    api.add_resource(restapi_define.OrderApi,
                     '/api/v1.0/billing/orders/<order_uuid>')

    # api.add_resource(restapi_define.WeiXinNotifyApi,
    #                 '/api/v1.0/billing/weixin/notify')

    app.run(host=conf.api_host, port=conf.api_port,
            threaded=True, debug=conf.api_debug)
