#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/7 10:08
"""

from common.logs import logging as log
from common.code import request_result
from common.parameters import parameter_check, context_data
from common.acl import acl_check
from common.token_ucenterauth import token_auth

from imageAuth.manager import images_manage, user_manage, resoucesStorage
from imageAuth.db import image_repo_db

import os
import conf.conf as CONF

from pyTools.imagetools.images import CreatePutRetUrl





def SetImageIco(team_uuid, resource_type, resource_uuid, resource_domain, imagename):
    retbool, image_dir = resoucesStorage.GetFileByLocation(team_uuid, resource_type, resource_uuid, resource_domain)
    if retbool:
        return True

    retbool, image_dir = CreatePutRetUrl(imagename, localpath=CONF.LOCAL_PATH, remopath=CONF.RepositoryObject,
                                         fonttype=CONF.FONTTYPE, access_key_id=CONF.AccessKeyID,
                                         access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
                                         bucker_name=CONF.BucketName)

    if retbool is False:
        log.info("retbool is False")
        log.info(image_dir)
        return False
    log.info(image_dir)

    resoucesStorage.SetFileUrlSave(team_uuid, resource_type, resource_uuid, resource_domain, image_dir)


class ImageRepoRpcAPI(object):
    def __init__(self):
        self.images_manage = images_manage.ImageRepoManager()
        self.usercenter = user_manage.UcenterManager()
        self.image_repo_db = image_repo_db.ImageRepoDB()

    def test_api(self, context, parameters):
        return request_result(0, 'test api is ok')


    @acl_check
    def get_pictures(self, context, parameters):
        """ 获取图片"""
        try:
            name = parameters.get('name').decode('utf-8').encode('utf-8')
            if name == '':
                return request_result(101)
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        retbool, image_dir = CreatePutRetUrl(name, localpath=CONF.LOCAL_PATH, remopath=CONF.RepositoryObject,
                             fonttype=CONF.FONTTYPE, access_key_id=CONF.AccessKeyID,
                             access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
                             bucker_name=CONF.BucketName)

        if retbool is False:
            return request_result(601)
        ret = dict()
        ret['oss_host'] = CONF.OssHost
        ret['image_dir'] = image_dir
        ret['image_url'] = CONF.OssHost + os.path.sep + image_dir
        return request_result(0, ret=ret)

    @acl_check
    def image_repo_rank(self, context, parameters):
        """ 镜像排名 """
        log.info('image_repo_rank begin')
        return self.images_manage.image_rank()

    # 平台镜像; 平台镜像搜索
    @acl_check
    def image_repo_public(self, context, parameters):
        try:
            page = parameters.get('page')
            page_size = parameters.get('page_size')
            repo_fuzzy = parameters.get('repo_fuzzy')

            page = parameter_check(page, ptype='pint')
            page_size = parameter_check(page_size, ptype='pint')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        log.info('image_repo_public begin')

        if repo_fuzzy is None:
            return self.images_manage.image_repo_public(page, page_size)

        return self.images_manage.image_repo_public_search(page, page_size, repo_fuzzy)


    # 平台镜像; 平台镜像搜索
    @acl_check
    def image_repo_own(self, context, parameters):
        try:

            user_info = token_auth(context['token'])['result']

            log.info('image_repo_own user_info: %s' % (user_info))
            team_uuid = user_info.get('team_uuid')

            page = parameters.get('page')
            page_size = parameters.get('page_size')
            repo_fuzzy = parameters.get('repo_fuzzy')

            page = parameter_check(page, ptype='pint')
            page_size = parameter_check(page_size, ptype='pint')

        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        log.info('image_repo_own begin')

        if repo_fuzzy is None:
            return self.images_manage.image_repo_own(page, page_size, team_uuid)

        return self.images_manage.image_repo_own_search(page, page_size, repo_fuzzy, team_uuid)


    # image_repo_own  image_repo_get_detail

    # @acl_check  由于对于public 属性的镜像非组织成员不能查看详细, 第一步, 不能采用 acl 控制
    def image_repo_get_detail(self, context, parameters):
        try:
            repoid = parameters.get('repoid')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        is_publice = self.image_repo_db.get_repo_publice_manger(repoid=repoid)

        if is_publice:
            log.info('image_repo_get_detail: %s is publie' % (repoid))
            return self.images_manage.GetRepoDetail(repoid)

        log.info('image_repo_get_detail: %s not is publie' % (repoid))
        return self.image_repo_get_detail_acl(context=context, parameters=parameters)


    # 获取一个镜像的详情 acl 控制权限
    @acl_check
    def image_repo_get_detail_acl(self, context, parameters):
        try:
            repoid = parameters.get('repoid')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.images_manage.GetRepoDetail(repoid)

    # 获取一个镜像的公开详情
    @acl_check
    def image_repo_get_public_detail(self, context, parameters):
        try:

            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
            repoid = parameters.get('repoid')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.images_manage.GetRepoDetail(repoid, private=False)


    # 删除一个镜像
    @acl_check
    def image_repo_del(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
            repoid = parameters.get('repoid')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        own_team_uuid = self.image_repo_db.get_repo_team_uuid_manger(repoid=repoid)

        if own_team_uuid is None:
            return request_result(701)
        if own_team_uuid == team_uuid:
            return self.images_manage.delRepo(repoid)
        else:
            return request_result(101)


    # 修改镜像详情
    @acl_check
    def image_repo_modify_detail(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            repoid = parameters.get('repoid')
            detail_type = parameters.get('detail_type')
            detail = parameters.get('detail')

            log.info('image_repo_modify_detail --> repoid: %s, detail_type=%s, detail=%s' % (repoid, detail_type, detail))

            Type = ['short_description', 'detail', 'is_public']

            if detail_type not in Type:
                log.error('detail_type is short_description or detail')
                return request_result(101)

            if detail_type == 'is_public' and ('1' != detail and '0' != detail):
                log.error('detail_type is is_public but detail not is 0/1')
                return request_result(101)

        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        # 是否是资源拥有者
        own_team_uuid = self.image_repo_db.get_repo_team_uuid_manger(repoid=repoid)

        log.info('own_team_uuid : %s' % (own_team_uuid))
        log.info('team_uuid : %s' % (team_uuid))

        if own_team_uuid is None:
            return request_result(701)
        if own_team_uuid == team_uuid:
            return self.images_manage.modifyRepoDetail(repoid, detail_type, detail)
        else:
            return request_result(101)

    def image_repo_name_exist(self, context, parameters):
        """ 镜像名是否存在 """
        try:
            imagename = parameters.get('imagename')
            if imagename is None or imagename == '':
                log.error('imagename is null')
                return request_result(101)
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.images_manage.image_repo_name_exist(imagename)

    def image_tag_id(self, context, parameters):
        """  通过tagid得到镜像名和tag """
        try:
            tagid = parameters.get('tagid')
            if tagid is None or tagid == '':
                log.error('tagid is null')
                return request_result(101)
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.images_manage.get_imagename_tag_by_tagid(tagid)

    def registry_token(self, context, parameters):
        """ 第一接口 """
        try:
            username = parameters.get('username')
            password = parameters.get('password')
            service = parameters.get('service')
            account = parameters.get('account')
            scopes = parameters.get('scopes')
            team_name = parameters.get('team_name')
            imagename = parameters.get('imagename')
            team_name = parameter_check(team_name, ptype='pnam', exist='no')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s' % (context, parameters, e))
            return request_result(101)

        # 系统账号, 开放镜像, 任意用户都可以 pull 获取到(不需要登录)
        # boxlinker 和 library 可以推送 library 镜像
        open_library = ('library')
        if team_name in open_library:
            is_public = 1
        else:
            is_public = 0

        if '' != scopes and team_name in open_library:
            type_, image, actions = scopes.split(':')
            actionlist = actions.split(',')
            if 'push' in actionlist:  # 不能用pull判断, 应该用 push 判断, 存在 push 即为拉去操作
                log.info('push library images no access permission')
                pass  # 执行正常的用户操作
            else:
                log.info('pull library images ')
                return self.images_manage.get_registry_token(account, service, scopes)
        try:
            user_name = parameter_check(username, ptype='pnam')  # 对 pull library 镜像的临时用户
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s' % (context, parameters, e))
            return request_result(101)

        # 获取token
        try:
            token = ''
            log.info('GetTokenByUnamePassTeam: user_name: %s, password: %s, team_name: %s' % (user_name, password, team_name))
            admin_user = ('boxlinker')
            if user_name in admin_user:  # admin 账号自己操作自己的镜像
                retbool, token = self.usercenter.username_password_authentication(user_name, password)
                if retbool is False:
                    return request_result(201)
            else:
                retbool, token = self.usercenter.username_password_teams_token(user_name, password, team_name)
                if retbool is False:
                    return request_result(201)

            retbool, team_info = self.usercenter.get_team_uuid(token=token, team_name=team_name)
            if retbool is False:
                log.error('registry_token get_team_uuid is error')
                return request_result(702)
            team_uuid = team_info['team_uuid']
            log.info('registry_token token new : %s, team_uuid: %s' % (token, team_uuid))
        except Exception, e:
            log.error('get token  error %s ' % (e))
            return request_result(201)

        # 登录操作,没有镜像, 只是登录操作,用户名和密码认证之后既可以返回token
        if '' == scopes:
            context = context_data(token, 'registry_token_generate_login', 'create')
            return self.generate_registry_token(context, parameters)

        type_, image, actions = scopes.split(':')
        actionlist = actions.split(',')
        retbool, repo_uuid = self.images_manage.get_repo_uuid(scopes, team_uuid, is_public=is_public)
        if retbool is False:
            log.error('get_repo_uuid is error, scopes: %s, team_uuid: %s' % (scopes, team_uuid))
            return request_result(703)

        # admin 账号  只要token正确  可以任意权限, 不能比 self.images_manage.get_repo_uuid 先执行,否则无法初始化数据
        if user_name in admin_user:
            context = context_data(token, 'registry_token_generate_login', 'create')
            return self.generate_registry_token(context, parameters)

        log.info('repo_uuid: %s, token: %s' % (repo_uuid, token))
        if 'push' in actionlist:  # 修改更新镜像
            context = context_data(token, repo_uuid, 'create')
        else:  # pull 读取
            context = context_data(token, repo_uuid, 'read')
        log.info('generate_registry_token begin context: %s' % (context))
        return self.generate_registry_token(context, parameters)

    @acl_check
    def generate_registry_token(self, context, parameters):
        """ 生成token """
        try:
            service = parameters.get('service')
            account = parameters.get('account')
            scopes = parameters.get('scopes')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s' % (context, parameters, e))
            return request_result(101)
        return self.images_manage.get_registry_token(account, service, scopes)

    # 获取自增id
    def image_get_tagid(self, context, parameters):
        """ 生成token """
        try:
            repo_name = parameters.get('repo_name')
            repo_tag = parameters.get('repo_tag')
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s' % (context, parameters, e))
            return request_result(101)
        return self.images_manage.get_image_tagid(repo_name, repo_tag)

    def registry_notice(self, context, parameters):
        """ registry 通知 """
        try:
            event = parameters['event']
            assert isinstance(event, dict)
            action = event['action']
        except Exception, e:
            log.error('event parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        try:
            if 'push' == action or 'pull' == action:
                target_mediaType = event['target']['mediaType']
                if target_mediaType == 'application/vnd.docker.distribution.manifest.v2+json':
                    url = event['target']['url']
                    tag = event['target']['tag']  # 有些通知不含有  tag  标记
                    repository = event['target']['repository']
                    length = event['target']['length']
                    timestamp = event['timestamp']
                    log.info('registry_notice timestamp: %s' % (timestamp))
                    timestamp = str(timestamp).rsplit('.')[0].replace('T', ' ')
                    actor = event['actor']['name']
                    action = event['action']
                    digest = event['target']['digest']
                    size = event['target']['size']
                    repo_id = event['id']
                    source_instanceID = event['source']['instanceID']
                    source_addr = event['source']['addr']

                    if 'push' == action:
                        log.info('registry_notice push')
                        self.image_repo_db.image_repo_push_event(repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr)
                        ret = self.images_manage.get_image_team_uuid_by_imagename(repository)
                        if ret is None:
                            pass
                        else:
                            image_uuid, team_uuid = ret
                            repository = str(repository).split('/')
                            if len(repository) > 1:
                                repository = repository[1]
                            log.info('team_uuid: %s, repository: %s' % (team_uuid, repository))
                            SetImageIco(team_uuid=team_uuid, resource_type='ImageAvatars',
                                        resource_uuid=image_uuid, resource_domain='boxlinker', imagename=repository)
                    elif 'pull' == action:
                        log.info('registry_notice pull')
                        # 对于 pull 操作,也就是download + 1
                        self.image_repo_db.image_repo_download_add(imagename=repository)

            return request_result(0)
        except Exception, e:
            log.error('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)