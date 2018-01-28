# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/14 上午11:01

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define as restapi_define


def rest_app_run():
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)

    # 规则维护,即:增查告警规则
    api.add_resource(restapi_define.AlarmApiDefine,
                     '/api/v1.0/application/alarm')

    # 服务与规则的对应关系维护
    api.add_resource(restapi_define.RestApiDefine,
                     '/api/v1.0/application/services/alarm/<alarm_uuid>')

    # 规则维护,有修改与删除某条规则之责
    api.add_resource(restapi_define.UpApiDefine,
                     '/api/v1.0/application/alarm/<alarm_uuid>')

    # 管理员:平台资源的告警
    api.add_resource(restapi_define.AdminResourceDefine,
                     '/api/v1.0/device/alarms')

    app.run(host="0.0.0.0", port=9000, threaded=True, debug=True)
