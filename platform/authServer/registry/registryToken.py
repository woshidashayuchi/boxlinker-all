#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/23 2:40
"""

from base64 import b64decode
from collections import namedtuple

from flask import request,g
from flask_restful import Resource

from authServer.conf.conf import private_key
from authServer.models.hub_db_meta import ImageRepository, Session, UserBase
from authServer.tools.db_check import login_username, get_uuid_by_name
from authServer.tools.logs import logging as log
from authServer.pyTools.decode.jwt_token import JwtToken
from authServer.pyTools.tools.codeString import request_result
import time
import uuid

from authServer.tools.decorate import image_repository_is_exist

Scope = namedtuple('Scope', ['type', 'image', 'actions'])

def safe_JwtToken(account, service, scope, private_key):
    """
    解决: self._backend._lib.RSA_R_DIGEST_TOO_BIG_FOR_RSA_KEY 报错问题
    """
    safe_num = 3
    while safe_num > 0:
        try:
            token = JwtToken(account=account, service=service, scope=scope, private_key=private_key).generate()
            return token
        except Exception as msg:
            print ' ---- safe_JwtToken --- is error ---- '
            safe_num -= 1
            print msg.message
            print msg.args
    return None


def parse_scopes(scopes):
    """ 解析 scopes """
    scope = None
    uname = ''
    imagename = ''
    actions = ''
    if scopes != '':
        # repository:libary/nginx:push, pull
        type_, image, actions = scopes.split(':')
        actionlist = actions.split(',')
        scope = Scope(type_, image, actionlist)

        uname, imagename = image.split('/')

    return scope, uname, imagename


def auto_ImageRepository(username, image):

    try:
        user_uuid = get_uuid_by_name(username=username)
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image).__str__()

        image_repo = ImageRepository(
            uuid=repo_uuid, uid=user_uuid, repository=image,
            creation_time=now, update_time=now,
            is_public='0', short_description='Push the mirror between terminals',
            detail='Push the mirror between terminals', is_code='0')

        g.db_session.add(image_repo)
        g.db_session.commit()
        return request_result(0)
    except Exception as msg:
        print msg.message
        return request_result(401, ret=msg.message)


def get_token_msg(func):
    """ 获取镜像库, token请求的数据参数 """
    def _deco():
        try:
            print "---------- get_token_msg ---------- 01"
            Authorization = request.headers.get('Authorization', default='').decode('utf-8').encode('utf-8')

            # 符号分隔为三组，分别描述范围、资源名、动作
            # repository:libary/nginx:push,pull
            scopes = request.args.get('scope', '').decode('utf-8').encode('utf-8')
            account = request.args.get('account', '').decode('utf-8').encode('utf-8')
            service = request.args.get('service', '').decode('utf-8').encode('utf-8')

            print '----- scopes -----:' + scopes
            request_headers = dict(request.headers)
            print("-----headers--- begin")
            for kk in request_headers:
                print ("kk: " + str(kk))
                print("kk: " + str(kk) + "     value: " + str(request_headers[kk]))
            print("-----headers--- end")
        except Exception as msg:
            print ' get_token_msg error', msg.message


        try:
            print "---------- get_token_msg ---------- 02"
            print Authorization
            print "---------- get_token_msg ---------- 03"
            username, password = b64decode(Authorization.replace('Basic', '').replace(' ', '')).split(':')
            log.info("----- username: " + str(username))
            log.info("----- password: " + str(password))

        except Exception as msg:
            print msg.message
            res = {"token": '', "msg": 'username or password is wrong', 'status': 1, "message": "ddsdsd"}
            return res  # 无权限访问

        # 用户名和密码认证
        if login_username(username=username, password=password) is False:
            res = {"token": '', "msg": 'username or password is wrong', 'status': 1, "message": "ddsdsd"}
            return res

        if scopes == '':  # 只是登录操作,用户名和密码认证之后既可以返回token
            scope = None
            return func(account=account, service=service, scope=scope)
        else:
            # repository:libary/nginx:push, pull
            print scopes
            # search
            type_, image, actions = scopes.split(':')
            actionlist = actions.split(',')
            scope = Scope(type_, image, actionlist)

            imagelist = image.split('/')
            if len(imagelist) != 2:   # 镜像地址不合法
                res = {"token": '', "msg": 'username or password is wrong', 'status': 1, "message": "ddsdsd"}
                return res

            repositoryname, imagename = imagelist

            # repository:boxlinker/alpine:push,pull


            image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.repository == image).first()

            # 这是 bug ,所有的操作都有 pull
            # if image_repo is None and "pull" in actions:  # 镜像不存在，而且是查询操作
            #     res = {"token": '', "msg": 'repository no have', 'status': 1, "message": "ddsdsd"}
            #     return res

            if image_repo is None and "push" in actions:  # 镜像不存在，而且是 push 操作
                if repositoryname != username:  # 镜像名前缀和用户名不符, 非法操作
                    return {"token": '', "msg": 'repository no have', 'status': 1, "message": "ddsdsd"}

                ret = auto_ImageRepository(username, image)
                if str(ret['status']) != '0':

                    print "ret['status']"
                    print ret['status']

                    return ret

            print '------ scope ------'
            print scope

            if 'boxlinker' == username:  # 对于boxlinker用户可以做任何操作
                print 'is admin'
                return func(account=account, service=service, scope=scope)


            # 20161008 这里增加镜像组认证数据库查询

            # 公有镜像 或 登录用户和镜像所属用户相同
            if image_repo.is_public == 0: # or ret.owner_name == username:
                return func(account=account, service=service, scope=scope)
        res = {"token": '', "msg": 'username or password is wrong', 'status': 1, "message": "ddsdsd"}
        return res  # 无权限访问
    return _deco


@get_token_msg
def _Server_Token(account, service, scope):

    # token = JwtToken(account=account, service=service, scope=scope, private_key=private_key).generate()
    token = safe_JwtToken(account=account, service=service, scope=scope, private_key=private_key)
    print token
    res = {"token": token}
    return res


class ServerToken(Resource):
    def get(self):
        """
        镜像库token认证,镜像操作权限验证
        """
        return _Server_Token()


def get_jwt_token(account, service, scopes):

    if scopes == '':
        scope = None
    else:
        print scopes
        type_, image, actions = scopes.split(':')
        actionlist = actions.split(',')
        scope = Scope(type_, image, actionlist)

    # token = JwtToken(account=account, service=service, scope=scope, private_key=private_key).generate()
    token = safe_JwtToken(account=account, service=service, scope=scope, private_key=private_key)
    res = {"token": token}
    return res