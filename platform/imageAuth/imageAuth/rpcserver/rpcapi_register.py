#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/7 10:15
"""

import rpc_image_api_define
import rpc_oauth_api_define

from common.logs import logging as log
from common.code import request_result
from common.rpc_api import RpcAPI

class RabbitmqResponse(object):
    def __init__(self):
        self.rpc_api = RpcAPI()
        self.rpc_add_resource()

    def rpc_add_resource(self):
        self.rpc_image_api_define = rpc_image_api_define.ImageRepoRpcAPI()
        self.rpc_oauth_api_define = rpc_oauth_api_define.OauthCodeRpcApi()

        # RunImageRepoClient(api='user_team_token', context=context, parameters=parameters)
        # context 中的 resource_uuid  可以与 RunImageRepoClient 中的 api 不同(概念不同)
        # user_team_token    获取一个用户对应组织的token
        # get_image_uuid_by_name   镜像名得到镜像id  (old  image_repo_name_exist)
        # registry_notice 镜像库消息通知 （old registry_notice)
        # registry_token  镜像库通知
        # image_repo_rank     镜像排名 (token验证即可)
        # image_repo_public   平台公开镜像; 搜索
        # image_repo_own      我的镜像; 搜索
        # image_repo_public_info      当个镜像 操作 (系统注册用户都可以调用该接口)
        # image_repo_detail_get       获取镜像详情
        # image_repo_del
        # image_repo_detail_modify     修改详情 (old image_repo_modify_detail)

        self.rpc_api.add_resource(
            "testapi", self.rpc_image_api_define.test_api)

        self.rpc_api.add_resource(
            "get_pictures", self.rpc_image_api_define.get_pictures)

        self.rpc_api.add_resource(
            "image_repo_rank", self.rpc_image_api_define.image_repo_rank)

        self.rpc_api.add_resource(
            "image_repo_public", self.rpc_image_api_define.image_repo_public)

        # 获取镜像公开信息,token 对即可
        self.rpc_api.add_resource(
            "image_repo_public_info", self.rpc_image_api_define.image_repo_get_public_detail)

        self.rpc_api.add_resource(
            "image_repo_own", self.rpc_image_api_define.image_repo_own)

        self.rpc_api.add_resource(
            "image_repo_detail_get", self.rpc_image_api_define.image_repo_get_detail)

        self.rpc_api.add_resource(
            "image_repo_del", self.rpc_image_api_define.image_repo_del)

        self.rpc_api.add_resource(
            "image_repo_detail_modify", self.rpc_image_api_define.image_repo_modify_detail)

        # 镜像名是否存在
        self.rpc_api.add_resource(
            "get_image_uuid_by_name", self.rpc_image_api_define.image_repo_name_exist)

        # 通过tagid得到镜像名和tag
        self.rpc_api.add_resource(
            "image_tag_id", self.rpc_image_api_define.image_tag_id)

        # registry token 第一接口
        self.rpc_api.add_resource(
            'registry_token', self.rpc_image_api_define.registry_token)

        #  登录获取token, 有用户token  直接调用该接口
        self.rpc_api.add_resource(
            "registry_token_generate_login", self.rpc_image_api_define.generate_registry_token)

        self.rpc_api.add_resource(
            "registry_notice", self.rpc_image_api_define.registry_notice)

        self.rpc_api.add_resource(
            "image_get_tagid", self.rpc_image_api_define.image_get_tagid)

        #


        ####  第三方绑定
        self.rpc_api.add_resource("oauth_status", self.rpc_oauth_api_define.OauthStatus)
        self.rpc_api.add_resource("get_oauth_url", self.rpc_oauth_api_define.OauthUrl)
        self.rpc_api.add_resource("oauth_callback", self.rpc_oauth_api_define.CallBack)

        self.rpc_api.add_resource("get_oauth_code_repo", self.rpc_oauth_api_define.OauthCodeRepo)
        self.rpc_api.add_resource("set_web_hook", self.rpc_oauth_api_define.WebHook)
        self.rpc_api.add_resource("del_oauth_status", self.rpc_oauth_api_define.DelOauthStatus)


        # get_oauth_url   获取用户授权跳转链接  (token 对即可)
        # oauth_callback  第三方授权回调,不需要用调用
        # get_oauth_code_repo 获取用户代码对应平台下的代码项目(token 对即可)
        # set_web_hook    授权平台可以对某个项目具有 hooks 权限(token 对即可)



    def rpc_exec(self, dict_data):
        try:
            log.info('rpc_exec ---> :')
            log.info(str(dict_data))
            return self.rpc_api.rpcapp_run(dict_data)
        except Exception, e:
            log.error('RPC Server exec error: %s' % (e))
            return request_result(599)