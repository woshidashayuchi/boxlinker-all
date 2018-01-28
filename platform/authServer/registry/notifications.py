#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/2 11:07
@镜像库 notifications 接口
"""
from flask_restful import Resource
from flask import request,g, jsonify

import requests

from authServer.models.hub_db_meta import RepositoryEvents, RepositoryPull
from authServer.pyTools.tools.timeControl import get_now_time

from authServer.conf.conf import DEBUG


"""
push 成功
    u'events':
        [
            {
                u'target':
                    {
                        u'repository': u'boxlinker/nginx-apidoc',
                        u'url': u'http://index.boxlinker.com/v2/boxlinker/nginx-apidoc/manifests/sha256:2291baa3410cf7cff964d25dde582c5a61a572561812df34a454be642149de41',
                        u'mediaType': u'application/vnd.docker.distribution.manifest.v2+json',
                        u'length': 1785,
                        u'tag': u'latest',
                        u'digest': u'sha256:2291baa3410cf7cff964d25dde582c5a61a572561812df34a454be642149de41',
                        u'size': 1785
                    },
                u'timestamp': u'2016-10-10T09:55:18.377124465Z',
                u'request':
                    {
                        u'method': u'PUT',
                        u'host': u'index.boxlinker.com',
                        u'useragent': u'docker/1.12.1 go/go1.6.3 git-commit/23cf638 kernel/4.4.20-moby os/linux arch/amd64 UpstreamClient(Docker-Client/1.12.1 \\(darwin\\))',
                        u'id': u'51bd8ed1-b86b-46ff-8a9c-43625aec00eb',
                        u'addr': u'103.43.187.162:41715'
                    },
                u'actor': {u'name': u'boxlinker'},
                u'source': {u'instanceID': u'9f9e72eb-178b-4861-a778-b5bac06d62fc', u'addr': u'bd4f9ff650f3:5000'},
                u'action': u'push',
                u'id': u'a7865b9b-7795-49c3-bf60-e46306d882c3'
            }
        ]
}
"""

import time
import uuid
from authServer.models.hub_db_meta import ImageRepository
from authServer.tools.db_check import login_username, get_uuid_by_name, get_orgsuuid_by_name
from authServer.pyTools.tools.codeString import request_result

from authServer.v1.repository.repoLogo import AutoSetLogo

# 是否是第一上传镜像;
def auto_ImageRepository(image, event):

    print " auto_ImageRepository "
    print image


    imagelist = image.split('/')
    if len(imagelist) != 2:  # 镜像地址不合法
        res = {"token": '', "msg": 'username or password is wrong', 'status': 1, "message": "ddsdsd"}
        return res

    repositoryname, imagename = imagelist  # 前缀  可能是   组织名
    print "repositoryname, imagename = imagelist"
    print repositoryname
    print imagename

    image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.repository == image).first()

    if image_repo is None:  # 镜像不存在
        try:
            # user_uuid = get_uuid_by_name(username=repositoryname)
            user_uuid = get_orgsuuid_by_name(username=repositoryname)   # 使用组织id, 不使用用户id, 后期全部修改成组织id
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image).__str__()

            print "repo_uuid"
            print repo_uuid

            is_public = '0'
            if 'library' == repositoryname:  # library 账号下的镜像全部公开
                is_public = '1'

            image_repo = ImageRepository(
                uuid=repo_uuid, uid=user_uuid, repository=image,
                creation_time=now, update_time=now,
                is_public=is_public, short_description='Push the mirror between terminals',
                detail='Push the mirror between terminals', is_code='0', download_num='1')

            g.db_session.add(image_repo)
            g.db_session.commit()

            AutoSetLogo(repositoryname=image)  # 立即设置图片

            print "auto_ImageRepository is ok"
            return request_result(0)
        except Exception as msg:
            print msg.message
            print msg.args
            print "auto_ImageRepository is error"
            return request_result(401, ret=msg.message)
    else:  # 镜像存在 download_num + 1
        try:
            download_num = int(image_repo.download_num) + 1

            if 'push' == event and image_repo.deleted == 1:
                g.db_session.query(ImageRepository).filter(ImageRepository.repository == image).update(
                    {"deleted": '0'})
                g.db_session.commit()
            elif 'pull' == event:
                g.db_session.query(ImageRepository).filter(ImageRepository.repository == image).update(
                    {"download_num": download_num, "deleted": '0'})
                g.db_session.commit()

            if image_repo.logo == '' or image_repo.logo is None:  # 判断logo 是否为空
                AutoSetLogo(repositoryname=image)
            else:
                print 'logo image_repo.logo != null'

        except Exception as msg:
            return request_result(401, ret=msg.message)

    print "auto_ImageRepository end"

    return request_result(0)


def push_event(event):
    """推送镜像操作"""
    try:
        url = event['target']['url']
        tag = event['target']['tag']  # 有些通知不含有  tag  标记
        repository = event['target']['repository']
        length = event['target']['length']

        timestamp = event['timestamp']
        timestamp = str(timestamp).rsplit('.')[0].replace('T', ' ')
        # timestamp = get_now_time()
        actor = event['actor']['name']
        action = event['action']

        digest = event['target']['digest']
        size = event['target']['size']
        repo_id = event['id']
        source_instanceID = event['source']['instanceID']
        source_addr = event['source']['addr']

        auto_ImageRepository(image=str(repository), event='push')

        print "----push--->begin"
        print url
        print tag
        print repository
        print type(repository)
        print length
        print timestamp
        print actor
        print action
        print "----push---> end"

    except Exception as msg:
        print 'error in push_event'
        print msg

    try:

        ret = g.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == repository,
                                                          RepositoryEvents.tag == tag).first()
        if ret is None:
            repo_enents = RepositoryEvents(repository=repository, url=url, length=length,
                                           tag=tag, actor=actor, action=action, creation_time=timestamp,
                                           update_time=timestamp, digest=digest, size=size, repo_id=repo_id,
                                           source_instanceID=source_instanceID, source_addr=source_addr)

            g.db_session.add(repo_enents)
        else:
            g.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == repository,
                                                        RepositoryEvents.tag == tag).update(
                {"action": action, "url": url, "length": length, "actor": actor, "update_time": timestamp,
                 "digest": digest, "size": size ,"repo_id": repo_id, "source_instanceID": source_instanceID,
                 "source_addr": source_addr})
        g.db_session.commit()
    except Exception as msg:
        print "error in push_event db"
        print msg.message

def pull_event(event):
    """ 拉取镜像操作 """
    try:
        url = event['target']['url']
        tag = event['target']['tag']  # 有些通知不含有  tag  标记
        repository = event['target']['repository']
        length = event['target']['length']

        timestamp = event['timestamp']
        timestamp = str(timestamp).rsplit('.')[0].replace('T', ' ')
        # timestamp = get_now_time()
        actor = event['actor']['name']
        action = event['action']

        digest = event['target']['digest']
        size = event['target']['size']
        repo_id = event['id']
        source_instanceID = event['source']['instanceID']
        source_addr = event['source']['addr']
        print "----pull--->begin"
        print url
        print tag
        print repository

        print type(repository)
        print length
        print timestamp
        print actor
        print action
        auto_ImageRepository(image=str(repository), event='pull')
        print "----pull---> end"
    except Exception as msg:
        print 'error in pull_event'
        print msg.message


    try:

        ret = g.db_session.query(RepositoryPull).filter(RepositoryPull.repository == repository,
                                                        RepositoryPull.tag == tag,
                                                        RepositoryPull.actor == actor).first()

        if ret is None:
            repo_pull = RepositoryPull(repository=repository, url=url, length=length, tag=tag, actor=actor,
                                       action=action, timestamp=timestamp,
                                       digest=digest, repo_id=repo_id, size=size, source_instanceID=source_instanceID,
                                       source_addr=source_addr)
            g.db_session.add(repo_pull)

        else:
            g.db_session.query(RepositoryPull).filter(RepositoryPull.repository == repository,
                                                      RepositoryPull.tag == tag,
                                                      RepositoryPull.actor == actor).update(
                {"action": action, "url": url, "length": length, "timestamp": timestamp, "digest": digest,
                 "size": size, "repo_id": repo_id, "source_instanceID": source_instanceID, "source_addr": source_addr})

        g.db_session.commit()
    except Exception as msg:
        print "error in pull_event db"
        print msg.message


# 镜像库回调通知接口
class Notifications(Resource):
    def post(self):
        # print '------------Notifications--------------------begin'
        # # docker 仓库通知消息
        # print request.json
        # print '------------Notifications--------------------end'
        try:

            events = request.json['events']

            # print "type(events) ---->"
            # print type(events)
            for event in events:
                # print "type(event) ---->"
                # print type(event)
                action = event['action']
                print "actor ---->" + action
                if action == 'push':
                    print "------------Notifications--------------------push"
                    # 并不是所有的通知都含有 target-->mediaType  标记
                    assert isinstance(event, dict)
                    target_mediaType = event['target']['mediaType']
                    print target_mediaType
                    if target_mediaType == 'application/vnd.docker.distribution.manifest.v2+json':
                        push_event(event=event)
                elif action == 'pull':
                    print "------------Notifications--------------------pull"
                    assert isinstance(event, dict)
                    target_mediaType = event['target']['mediaType']
                    if target_mediaType == 'application/vnd.docker.distribution.manifest.v2+json':
                        pull_event(event=event)

        except Exception as msg:
            print 'is error  sssssss'
            print msg.message


        # 通知滚动更新程序,进行服务更新操作
        # if DEBUG:
        #     try:
        #         # response = requests.post('http://krud.boxlinker.com', json=request.json)
        #         print "request.json : "
        #         print request.json
        #
        #         response = requests.post(ROLLING_UPDATE, json=request.json)
        #         print response.status_code
        #     except Exception as msg:
        #         print 'Notifications is error'
        #         print msg.message

        return ''

    def get(self):
        print 'Notifications  is sss'
        return jsonify({"code": "0"})