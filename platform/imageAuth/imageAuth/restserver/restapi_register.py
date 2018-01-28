#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/6 16:59
"""


import rest_image_api_define

import rest_oauth_api_define   # 第三方绑定

from flask import Flask, render_template, request
from flask_restful import Api
from flask_cors import CORS

# 注册接口;并启动 restful 服务
def rest_app_run():
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app=app)

    @app.route('/oauth/gredirect', methods=['GET', 'POST'])
    def front_building():

        code = request.args.get('redirect', '').decode('utf-8').encode('utf-8')
        if code == '':
            item = 'http://test.boxlinker.com/building/create'
        else:
            item = code
        return render_template('front_building.html', item=item)

    api.add_resource(rest_image_api_define.TestApi, '/api/v1.0/imagerepo/test')

    api.add_resource(rest_image_api_define.CreateImage, '/api/v1.0/pictures')

    api.add_resource(rest_image_api_define.RegistryToken, '/api/v1.0/registry/token')

    # 镜像通知
    api.add_resource(rest_image_api_define.RegistryNotice, '/api/v1.0/registry/notifications')

    # 1.1 镜像名是否存在
    api.add_resource(rest_image_api_define.ImageRepoExist, '/api/v1.0/imagerepo/publicimage/')

    # 1.2 镜像排名
    api.add_resource(rest_image_api_define.ImageRepoRankApi, '/api/v1.0/imagerepo/ranks')

    # 平台公开镜像  /api/v1.0/imagerepo/publicimages/<int:page>/<int:page_size>'
    # 平台公开镜像搜索: /api/v1.0/imagerepo/publicimages/<int:page>/<int:page_size>/?repo_fuzzy=library%2Fnginx
    api.add_resource(rest_image_api_define.ImageRepoPublic,
                     '/api/v1.0/imagerepo/publicimages/<int:page>/<int:page_size>',   # 平台公开镜像
                     '/api/v1.0/imagerepo/publicimages/<int:page>/<int:page_size>/')  # 平台公开镜像搜索

    # 我的镜像  /api/v1.0/imagerepo/ownimages/<int:page>/<int:page_size>
    # 我的镜像: 搜索操作 /api/v1.0/imagerepo/ownimages/<int:page>/<int:page_size>/?repo_fuzzy=library%2Fnginx
    api.add_resource(rest_image_api_define.OwnImageRepo,
                     '/api/v1.0/imagerepo/ownimages/<int:page>/<int:page_size>',   # 我的镜像
                     '/api/v1.0/imagerepo/ownimages/<int:page>/<int:page_size>/',  # 我的镜像: 搜索操作
                     )

    # 获取一个镜像详情; 删除一个镜像  /api/v1.0/imagerepo/image/<string:repoid>
    api.add_resource(rest_image_api_define.ImageRepo,
                     '/api/v1.0/imagerepo/image/<string:repoid>')

    # 获取一个镜像详情 token 对即可
    api.add_resource(rest_image_api_define.ImageRepoSystem,
                     '/api/v1.0/imagerepo/image/<string:repoid>/public_info')

    # 通过tagid拿到镜像名和版本
    api.add_resource(rest_image_api_define.ImageTag,
                     '/api/v1.0/imagerepo/image/tagid/<string:tagid>')

    # 修改详情
    api.add_resource(rest_image_api_define.ImageRepoDetail,
                     '/api/v1.0/imagerepo/image/<string:repoid>/detail/<string:detail_type>')

    # 修改详情
    api.add_resource(rest_image_api_define.ImageRepoTagID,
                     '/api/v1.0/imagerepo/image/tagids/')

    # http://imageauth.boxlinker.com/api/v1.0/imagerepo/image/tagids/?repo_name=boxlinker/pause&repo_tag=2.0


    # 第三方认证
    # 2.0 get    获取用户是否已经绑定 /api/v1.0/oauthclient/oauth
    # 2.4 delete 解除绑定
    api.add_resource(rest_oauth_api_define.OauthStatus,
                     '/api/v1.0/oauthclient/oauth',
                     '/api/v1.0/oauthclient/oauth/<string:src_type>')

    # 2.1 获取用户授权跳转链接
    api.add_resource(rest_oauth_api_define.OauthUrl, '/api/v1.0/oauthclient/url')

    # 2.2 用户点击授权链接之后,第三方回调授权地址
    api.add_resource(rest_oauth_api_define.CallBack,
                     '/api/v1.0/oauthclient/callback/',
                     '/api/v1.0/oauthclient/callback')
    # 2.0 2.1 2.2 github 和 coding 公用


    # 2.3 2.4
    # get 获取代码项目列表;
    # put 刷新代码列表,返回新的代码项目列表
    # Python 代码处理 coding
    api.add_resource(rest_oauth_api_define.OauthCodeRepo,
                     '/api/v1.0/oauthclient/repos/<string:src_type>')



    # 2.3 授权平台可以对某个项目具有 hooks 权限
    api.add_resource(rest_oauth_api_define.WebHook,
                     '/api/v1.0/oauthclient/webhooks/<string:src_type>/<string:repo_name>')



    # api.add_resource(rest_oauth_api_define.OauthCodeRepo, '/api/v1.0/oauthclient/repos/github')
    app.run(host='0.0.0.0', port=8001, threaded=True, debug=True)

    # app.run(host='0.0.0.0', port=8001, threaded=True, debug=True, ssl_context=('/ImageRepo/registry/ssl/ca.crt',
    #                                                                            '/ImageRepo/registry/ssl/ca.key'))