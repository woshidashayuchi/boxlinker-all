# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define1 as restapi_define1


def rest_app_run():
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)

    api.add_resource(restapi_define1.RollClientApi,
                     '/api/v1.0/application/services/rollings')

    app.run(host="0.0.0.0", port=9000, threaded=True, debug=True)

