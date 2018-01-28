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

    api.add_resource(restapi_define.UcenterUsersApi,
                     '/api/v1.0/ucenter/users')

    api.add_resource(restapi_define.UcenterUserApi,
                     '/api/v1.0/ucenter/users/<user_uuid>')

    api.add_resource(restapi_define.UcenterUserStatusApi,
                     '/api/v1.0/ucenter/users/status/<user_uuid>')

    api.add_resource(restapi_define.UcenterRolesApi,
                     '/api/v1.0/ucenter/roles')

    api.add_resource(restapi_define.UcenterRoleApi,
                     '/api/v1.0/ucenter/roles/<role_uuid>')

    api.add_resource(restapi_define.UcenterPasswordApi,
                     '/api/v1.0/ucenter/passwords/<user_uuid>')

    api.add_resource(restapi_define.UcenterTokensApi,
                     '/api/v1.0/ucenter/tokens')

    api.add_resource(restapi_define.UcenterTeamsApi,
                     '/api/v1.0/ucenter/teams')

    api.add_resource(restapi_define.UcenterTeamApi,
                     '/api/v1.0/ucenter/teams/<team_uuid>')

    api.add_resource(restapi_define.UcenterProjectsApi,
                     '/api/v1.0/ucenter/projects')

    api.add_resource(restapi_define.UcenterProjectApi,
                     '/api/v1.0/ucenter/projects/<project_uuid>')

    api.add_resource(restapi_define.UcenterUsersTeamsApi,
                     '/api/v1.0/ucenter/usersteams')

    api.add_resource(restapi_define.UcenterUserTeamApi,
                     '/api/v1.0/ucenter/usersteams/<user_uuid>')

    api.add_resource(restapi_define.UcenterUsersProjectsApi,
                     '/api/v1.0/ucenter/usersprojects')

    api.add_resource(restapi_define.UcenterUserProjectApi,
                     '/api/v1.0/ucenter/usersprojects/<user_uuid>')

    @app.route('/api/v1.0/ucenter/users/activate/<status>',
               methods=['GET'])
    def activate(status):
        return restapi_define.user_activate(status)

    app.run(host=conf.api_host, port=conf.api_port,
            threaded=True, debug=conf.api_debug)
