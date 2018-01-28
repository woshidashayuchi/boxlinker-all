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

    api.add_resource(restapi_define.OperationsApi,
                     '/api/v1.0/security/operations')

    app.run(host=conf.api_host, port=conf.api_port,
            threaded=True, debug=conf.api_debug)
