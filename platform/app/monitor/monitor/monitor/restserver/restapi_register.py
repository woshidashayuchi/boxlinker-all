# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/03/01


from flask import Flask
from flask_cors import CORS
from time import sleep
from common.logs import logging as log
from restapi_define import MonitorClientApi


app = Flask(__name__)
CORS(app=app)


@app.route('/api/v1.0/monitors/pods/<pod_name>/<rtype>', methods=['GET'])
def monitor_service(pod_name, rtype):
    return MonitorClientApi.monitor_for(pod_name, rtype)


@app.route('/api/v1.0/monitors/broads', methods=['GET'])
def broad_service():
    return MonitorClientApi.broad_for()


def rest_app_run():

    while True:
        try:
            app.run(debug=True, host="0.0.0.0", port=9008, threaded=True)
        except Exception, e:
            log.warning('k8s API Server running error, reason=%s' % e)

        sleep(8)
