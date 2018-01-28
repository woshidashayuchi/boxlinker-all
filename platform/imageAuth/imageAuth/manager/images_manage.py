#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/6 18:40
"""

import json
import uuid
import time

from conf.conf import OssHost

from common.code import request_result
from common.logs import logging as log
from common.json_encode import CJsonEncoder

from common.local_cache import LocalCache
from pyTools.token.jwt_token import safe_JwtToken
from pyTools.token.token import get_md5

from collections import namedtuple
from imageAuth.manager import resoucesStorage

from conf.conf import issuer, private_key
from imageAuth.db import image_repo_db

Scope = namedtuple('Scope', ['type', 'image', 'actions'])

caches = LocalCache(100)
def retImageRepo(page, page_size, count, repolist):
    RepoImageResult = dict()
    RepoImageResult['page'] = page
    RepoImageResult['page_size'] = page_size
    RepoImageResult['count'] = count
    RepoImageResult['current_size'] = len(repolist)

    retlist = list()
    for image_project_node in repolist:
        image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, \
        short_description, detail, \
        download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type = image_project_node
        temp_d = dict()
        temp_d['uuid'] = image_uuid
        temp_d['repository'] = repository
        temp_d['creation_time'] = creation_time
        temp_d['update_time'] = update_time
        temp_d['is_public'] = is_public
        temp_d['short_description'] = short_description  # 简单描述
        temp_d['detail'] = detail  # 详细描述
        temp_d['type'] = is_code  # 0-->手动推送;   1-->代码构建
        temp_d['download_num'] = download_num  # 下载次数

        temp_d['is_code'] = is_code
        temp_d['src_type'] = src_type

        # 每次都调用是否影响性能
        retbool, image_dir = resoucesStorage.GetFileByLocation(team_uuid=team_uuid, resource_type="ImageAvatars",
                                                               resource_uuid=image_uuid,
                                                               resource_domain="boxlinker")
        if retbool:
            temp_d['logo'] = OssHost + '/' + image_dir
        else:
            temp_d['logo'] = OssHost + '/' + 'repository/default.png'

        temp_d = json.dumps(temp_d, cls=CJsonEncoder)
        temp_d = json.loads(temp_d)
        retlist.append(temp_d)

    RepoImageResult['result'] = retlist
    return request_result(0, ret=RepoImageResult)

class ImageRepoManager(object):
    def __init__(self):
        log.info('ImageRepoManager __init__')
        self.image_repo_db = image_repo_db.ImageRepoDB()

    def get_repo_uuid(self, scopes, team_uuid, is_public=0):
        """得到一个镜像的uuid"""
        try:
            # repository:libary/nginx:push, pull
            type_, image, actions = scopes.split(':')
            actionlist = actions.split(',')
            log.info('actions : %s,  actionlist: %s, imagename=%s' % (actions, actionlist, image))

            image_uuid = self.image_repo_db.get_image_repo_uuid_by_name(imagename=image)
            if len(image_uuid) > 0:
                log.info('get_repo_uuid is True uuid: %s' % (image_uuid[0][0]))
                return True, image_uuid[0][0]

            if 'push' in actionlist:
                image_name = str(image)
                repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image_name).__str__()
                self.image_repo_db.init_image_repo(repo_uuid=repo_uuid, imagename=image_name, resource_type='image_repo',
                                                   user_uuid='0', admin_uuid='global', team_uuid=team_uuid,
                                                   project_uuid='0', is_public=is_public)
                return True, repo_uuid
            return False, None
        except Exception, e:
            log.error('ImageRepoManager get_repo_uuid is error: %s' % (e))
            return False, None

    def image_rank(self):
        """ 获取镜像排名 """
        Image_repo = self.image_repo_db.get_image_rank()
        log.info('image_rank info: %s' % (type(Image_repo)))
        log.info('image_rank info: %s' % (str(Image_repo)))
        return retImageRepo(page=0, page_size=20, count=20, repolist=Image_repo)

    # 平台镜像
    def image_repo_public(self, page, page_size):
        try:
            offset = (page - 1) * page_size
            limit = page_size

            if offset < 0 or limit <= 0:
                log.error('image_repo_public page or page_size is error')
                return request_result(101, "page or page_size is error")

            count = self.image_repo_db.get_public_image_count()
            image_repo = self.image_repo_db.get_public_image(offset, limit)
            return retImageRepo(page=page, page_size=page_size, count=count, repolist=image_repo)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(404)

    # 平台镜像搜索
    def image_repo_public_search(self, page, page_size, repo_fuzzy):
        repovalue = '%' + repo_fuzzy + '%'
        offset = (page - 1) * page_size
        limit = page_size

        if offset < 0 or limit <= 0:
            log.error('image_repo_public page or page_size is error')
            return request_result(101)

        try:
            # 获取满足搜索条件的镜像个数
            count = self.image_repo_db.get_search_count(repovalue)
            image_repo = self.image_repo_db.get_search_image_repo(repovalue, offset, limit)
            return retImageRepo(page=page, page_size=page_size, count=count, repolist=image_repo)
        except Exception as msg:
            log.error('Database update error, reason=%s' % (msg.message))
            return request_result(404)

    def image_repo_own(self, page, page_size, team_uuid):
        """ 我的镜像 """
        try:
            log.info('image_repo_own team_uuid: %s' % (team_uuid))
            offset = (page - 1) * page_size
            limit = page_size

            if offset < 0 or limit <= 0:
                log.error('page or page_size is error')
                return request_result(101)

            count = self.image_repo_db.get_image_repo_own_count(team_uuid)  # 个数

            # 我的镜像
            image_repo = self.image_repo_db.get_image_repo_own(team_uuid, offset, limit)
            return retImageRepo(page=page, page_size=page_size, count=count, repolist=image_repo)
        except Exception as msg:
            log.error('Database update error, reason=%s' % (msg.message))
            return request_result(404)



    def image_repo_own_search(self, page, page_size, repo_fuzzy, team_uuid):
        repovalue = '%' + repo_fuzzy + '%'

        offset = (page - 1) * page_size
        limit = page_size

        if offset < 0 or limit <= 0:
            log.error('page or page_size is error')
            return request_result(101)

        try:
            # 得到我的镜像满足搜索条件的个数
            count = self.image_repo_db.get_image_repo_own_search_count(repovalue, team_uuid)

            # 得到满足搜索条件的我的镜像
            image_repo = self.image_repo_db.get_image_repo_own_search(repovalue, team_uuid, offset, limit)
            return retImageRepo(page=page, page_size=page_size, count=count, repolist=image_repo)
        except Exception as msg:
            log.error('Database update error, reason=%s' % (msg.message))
            return request_result(404)


    def GetRepoDetail(self, repoid, private=True):
        """ 获取一个镜像详情, private 为 False 时表示只获取基本公开信息, 对任何用户都看见"""
        image_repo = self.image_repo_db.get_repo_detail_by_uuid(repoid)

        if len(image_repo) <= 0:
            return request_result(809, ret="Resources does not exist or has been deleted")

        image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, \
        short_description, detail, \
        download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type = image_repo[0]

        ret_d = dict()
        ret_d['repository'] = repository
        ret_d['creation_time'] = creation_time
        ret_d['update_time'] = update_time
        ret_d['is_public'] = is_public
        ret_d['team_uuid'] = team_uuid



        if private:
            ret_d['short_description'] = short_description
            ret_d['detail'] = detail
            ret_d['download_num'] = download_num
            ret_d['enshrine_num'] = enshrine_num
            ret_d['review_num'] = review_num
            ret_d['pushed'] = pushed
            ret_d['is_code'] = is_code

            retbool, image_dir = resoucesStorage.GetFileByLocation(team_uuid=team_uuid, resource_type="ImageAvatars",
                                                                   resource_uuid=image_uuid,
                                                                   resource_domain="boxlinker")
            if retbool:
                ret_d['logo'] = OssHost + '/' + image_dir
            else:
                ret_d['logo'] = OssHost + '/' + 'repository/default.png'


        repo_event = self.image_repo_db.get_repo_events_by_imagename(repository)

        repo_tags = list()
        for repo_event_node in repo_event:
            tagid, repository, url, lengths, tag, actor, actions, digest, \
            sizes, repo_id, source_instanceID, source_addr, deleted, \
            creation_time, update_time = repo_event_node
            tag_temp = dict()
            tag_temp['repo_id'] = repo_id
            tag_temp['tag'] = tag
            tag_temp['tagid'] = tagid

            if private:
                tag_temp['url'] = url
                tag_temp['length'] = lengths
                tag_temp['actor'] = actor
                tag_temp['action'] = actions
                tag_temp['digest'] = digest
                tag_temp['creation_time'] = creation_time
                tag_temp['update_time'] = update_time
            tag_temp = json.dumps(tag_temp, cls=CJsonEncoder)
            tag_temp = json.loads(tag_temp)
            repo_tags.append(tag_temp)

        ret_d['tags'] = repo_tags
        ret_d = json.dumps(ret_d, cls=CJsonEncoder)
        ret_d = json.loads(ret_d)

        return request_result(0, ret=ret_d)


    def GetRepoPublicDetail(self, repoid):
        """ 获取公开信息 GetRepoPublicDetail """
        image_repo = self.image_repo_db.get_repo_detail_by_uuid(repoid)

        if len(image_repo) <= 0:
            return request_result(701)

        image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
        download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type = image_repo

        ret_d = dict()
        ret_d['repository'] = repository
        ret_d['creation_time'] = creation_time
        ret_d['update_time'] = update_time
        ret_d['team_uuid'] = team_uuid

        retbool, image_dir = resoucesStorage.GetFileByLocation(team_uuid=team_uuid, resource_type="ImageAvatars",
                                                               resource_uuid=image_uuid, resource_domain="boxlinker")

        if retbool:
            ret_d['logo'] = OssHost + '/' + image_dir
        else:
            ret_d['logo'] = OssHost + '/' + 'repository/default.png'


        repo_event = self.image_repo_db.get_repo_events_by_imagename(repository)

        repo_tags = list()
        for repo_event_node in repo_event:
            tagid, repository, url, lengths, tag, actor, actions, digest, \
            sizes, repo_id, source_instanceID, source_addr, deleted, \
            creation_time, update_time = repo_event_node
            tag_temp = dict()
            tag_temp['tagid'] = tagid
            tag_temp['url'] = url
            tag_temp['length'] = lengths
            tag_temp['tag'] = tag
            tag_temp['actor'] = actor
            tag_temp['action'] = actions
            tag_temp['digest'] = digest
            tag_temp['repo_id'] = repo_id
            tag_temp['creation_time'] = creation_time
            tag_temp['update_time'] = update_time
            tag_temp = json.dumps(tag_temp, cls=CJsonEncoder)
            tag_temp = json.loads(tag_temp)
            repo_tags.append(tag_temp)

        ret_d['tags'] = repo_tags
        ret_d = json.dumps(ret_d, cls=CJsonEncoder)
        ret_d = json.loads(ret_d)

        return request_result(0, ret=ret_d)

    def delRepo(self, repoid):
        """ 删除镜像 """
        try:
            self.image_repo_db.del_image_repo_by_uuid(repoid)
        except Exception as msg:
            return request_result(403, ret=msg.message)

        return request_result(0)

    def image_repo_name_exist(self, imagename):
        try:
            # 镜像名是否存在
            image_repo = self.image_repo_db.get_repo_uuid_by_image_name(imagename)
            if len(image_repo) <= 0:
                return request_result(701)

            return request_result(0, image_repo[0][0])
        except Exception, e:
            log.error("image_repo_name_exist is error: %s", (e))
            return request_result(404)

    def get_imagename_tag_by_tagid(self, tagid):
        try:
            image_repo = self.image_repo_db.get_imagename_tag_by_tagid(tagid)
            if len(image_repo) <= 0:
                return request_result(701)

            repository, tag = image_repo[0]
            msg = dict()
            msg['image_name'] = repository
            msg['tag'] = tag

            image_repo = self.image_repo_db.get_repo_uuid_by_image_name(repository)
            if len(image_repo) <= 0:
                return request_result(701)

            msg['image_uuid'] = image_repo[0][0]

            return request_result(0, ret=msg)
        except Exception, e:
            log.error("image_repo_name_exist is error: %s", (e))
            return request_result(404)

    def modifyRepoDetail(self, repoid, detail_type, detail):
        """ 修改镜像详情 """
        try:
            ret = self.image_repo_db.modify_image_repo(image_uuid=repoid, detail_type=detail_type, detail=detail)
            return request_result(0)
        except Exception as msg:
            return request_result(403)

    # 生成token
    def get_registry_token(self, account, service, scopes):

        md1 = get_md5(account)
        md2 = get_md5(service)
        md3 = get_md5(scopes)

        key = md1 + md2 + md3

        tokeninfo = caches.get(key=key)
        if tokeninfo != caches.notFound:
            log.info('get_registry_token caches token : %s' % (tokeninfo['token']))
            return {"token": tokeninfo['token']}

        if '' == scopes:
            scope = None
        else:
            type_, image, actions = scopes.split(':')
            actionlist = actions.split(',')
            scope = Scope(type_, image, actionlist)

        token = safe_JwtToken(account=account, service=service, scope=scope, issuer=issuer, private_key=private_key)
        log.info('first safe_JwtToken: token %s' % (token))

        expire = int(time.time()) + 300
        caches.set(key=key, value={"token": token, "expire": expire})

        res = {"token": token}
        return res

    def get_image_team_uuid_by_imagename(self, imagename):
        ret = self.image_repo_db.get_image_uuid_and_team_uuid_by_imagename(imagename=imagename)
        if len(ret) == 0:
            return None
        return ret[0]

    def get_image_tagid(self, repo_name, repo_tag):
        ret = self.image_repo_db.get_image_tagid(repo_name=repo_name, repo_tag=repo_tag)
        if len(ret) == 0:
            return request_result(703)
        return request_result(0, ret=ret[0][0])

