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

    api.add_resource(restapi_define.CephClustersApi,
                     '/api/v1.0/admin/storage/cephclusters')

    api.add_resource(restapi_define.CephClusterApi,
                     '/api/v1.0/admin/storage/cephclusters/<cluster_uuid>')

    api.add_resource(restapi_define.CephHostsApi,
                     '/api/v1.0/admin/storage/cephhosts')

    api.add_resource(restapi_define.CephHostApi,
                     '/api/v1.0/admin/storage/cephhosts/<host_uuid>')

    api.add_resource(restapi_define.CephMonsApi,
                     '/api/v1.0/admin/storage/cephmons')

    api.add_resource(restapi_define.CephMonApi,
                     '/api/v1.0/admin/storage/cephmons/<mon_uuid>')

    api.add_resource(restapi_define.CephOsdsApi,
                     '/api/v1.0/admin/storage/cephosds')

    api.add_resource(restapi_define.CephOsdApi,
                     '/api/v1.0/admin/storage/cephosds/<osd_uuid>')

    api.add_resource(restapi_define.CephPoolsApi,
                     '/api/v1.0/admin/storage/cephpools')

    api.add_resource(restapi_define.CephPoolApi,
                     '/api/v1.0/admin/storage/cephpools/<pool_uuid>')

    api.add_resource(restapi_define.VolumesApi,
                     '/api/v1.0/storage/volumes')

    api.add_resource(restapi_define.VolumeApi,
                     '/api/v1.0/storage/volumes/<volume_uuid>')

    api.add_resource(restapi_define.VolumesReclaimsApi,
                     '/api/v1.0/storage/volumes/reclaims')

    api.add_resource(restapi_define.VolumeReclaimApi,
                     '/api/v1.0/storage/volumes/reclaims/<volume_uuid>')

    app.run(host=conf.api_host, port=conf.api_port,
            threaded=True, debug=conf.api_debug)
