# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from common.logs import logging as log
import restapi_define


def rest_app_run():
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)
    api.add_resource(restapi_define.RestApiDefine, '/api/v1.0/application/services')

    app.run(host="0.0.0.0", port=9000, threaded=True, debug=True)


