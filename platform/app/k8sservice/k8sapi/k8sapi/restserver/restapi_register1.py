# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define1 as restapi_define


def rest_app_run():
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)

    api.add_resource(restapi_define.ServicesApi,
                     '/api/v1.0/application/services')

    api.add_resource(restapi_define.ServiceApi,
                     '/api/v1.0/applicataion/services/<service_uuid>')

    api.add_resource(restapi_define.ServiceName,
                     '/api/v1.0/application/services/service_name/<service_name>')

    api.add_resource(restapi_define.Certify,
                     '/api/v1.0/application/certifies')

    api.add_resource(restapi_define.CertifyUp,
                     '/api/v1.0/application/certifies/<certify_uuid>')

    api.add_resource(restapi_define.AdminService,
                     '/api/v1.0/application/admin/services')

    app.run(host="0.0.0.0", port=9000, threaded=True, debug=False)

