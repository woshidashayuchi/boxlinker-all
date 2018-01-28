#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/13 18:54
"""

import time
import uuid

from sqlalchemy import or_, func, desc


from common.logs import logging as log

from imageAuth.db.db import ImageRepository, RepositoryEvents, ResourcesAcl, RepositoryPull
from pyTools.tools.timeControl import get_now_time

from imageAuth.db.db import Session


class ImageRepositoryDb(object):
    def __init__(self):
        log.info('ImageRepositoryDb __init__')
        self.db_session = Session()

    # 第一次上传
    def add_image_repo(self, image, team_uuid, is_public=1):
        try:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            image_name = str(image)
            repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image_name).__str__()

            image_repo = ImageRepository(
                image_uuid=repo_uuid, team_uuid=team_uuid, repository=image_name,
                creation_time=now, update_time=now,
                is_public=is_public, short_description='Push the mirror between terminals',
                detail='Push the mirror between terminals', is_code=0, download_num=1)
            self.db_session.add(image_repo)
            self.db_session.commit()
            return True, repo_uuid
        except Exception, e:
            log.error('add_image_repo is error %s' % (e))
            self.db_session.rollback()
            return False, None

    # 通过image id删除一个镜像
    def del_image_repo_by_uuid(self, repo_uuid):
        try:
            log.info('del_image_repo_by_uuid repo_uuid: %s ' % (repo_uuid))
            imagerepo = ImageRepository(image_uuid=repo_uuid)
            self.db_session.delete(imagerepo)
            self.db_session.commit()
            return True
        except Exception, e:
            log.error('del_image_repo_by_uuid is error %s' % (e))
            self.db_session.rollback()
            return False


    # 添加资源的ACL记录
    def add_resources_acl(self, resource_uuid, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid):
        try:
            now = get_now_time()
            acl = ResourcesAcl(
                resource_uuid=resource_uuid, resource_type=resource_type, admin_uuid=admin_uuid,
                user_uuid=user_uuid,
                team_uuid=team_uuid, project_uuid=project_uuid, create_time=now, update_time=now)
            self.db_session.add(acl)
            self.db_session.commit()
            return True
        except Exception, e:
            log.error('add_resources_acl is error %s' % (e))
            self.db_session.rollback()
            return False

    # 初始化记录
    def init_image_repo(self, imagename, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid, is_public=1):
        try:
            retbool, repo_uuid = self.add_image_repo(image=imagename, team_uuid=team_uuid, is_public=is_public)
            if retbool is False:
                log.error('add_image_repo is error')
                return retbool, repo_uuid

            retbool = self.add_resources_acl(resource_uuid=repo_uuid, resource_type=resource_type, user_uuid=user_uuid, admin_uuid=admin_uuid, team_uuid=team_uuid, project_uuid=project_uuid)
            if retbool is False:
                log.error('add_resources_acl is error')
                self.del_image_repo_by_uuid(repo_uuid=repo_uuid)
                return False, None
            return True, repo_uuid
        except Exception, e:
            log.error('add_resources_acl is error %s' % (e))
            return False, None

    def get_repo_uuid(self, scopes, team_uuid, is_public=1):
        try:
            # repository:libary/nginx:push, pull

            return True, 'a9563a2c-f461-3656-8319-8957f3d9c637'

            # 特殊调试
            type_, image, actions = scopes.split(':')
            actionlist = actions.split(',')
            log.info('actions : %s,  actionlist: %s' % (actions, actionlist))

            log.info('get_repo_uuid get_image_repo_name_exist begin: %s' % image)
            log.info('get_repo_uuid get_image_repo_name_exist begin: %s' % (type(image)))
            retbool, image_repo = self.get_image_repo_name_exist(image)
            log.info('get_repo_uuid get_image_repo_name_exist end:')

            if retbool:
                log.info('get_image_repo_name_exist is True uuid: %s' % (image_repo.image_uuid))
                return True, image_repo.image_uuid

            log.info('get_image_repo_name_exist is False uuid: null ')

            if 'push' in actionlist:
                retbool, repo_uuid = self.init_image_repo(imagename=image, resource_type='image_repo',
                                                         user_uuid='0', admin_uuid='global',
                                                         team_uuid=team_uuid, project_uuid='0', is_public=is_public)
                return retbool, repo_uuid

            return False, None
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None


    # 获取一个镜像的详细
    def get_repo_detail(self, repoid):
        try:
            image_repo = self.db_session.query(ImageRepository).filter(
                ImageRepository.image_uuid == repoid,
                ImageRepository.deleted == 0).first()
            return True, image_repo
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None


    # 获取一个镜像的全部 RepositoryEvents 信息
    def get_repo_events(self, imagerep_name):
        try:
            repo_event = self.db_session.query(RepositoryEvents).filter(
                RepositoryEvents.repository == imagerep_name).all()
            return True, repo_event
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None

    # 平台镜像
    def get_public_image(self, offset, limit):
        try:
            from sqlalchemy import func
            image_repo = self.db_session.query(ImageRepository).filter(
                    ImageRepository.deleted == 0,
                    ImageRepository.is_public == 1).offset(offset).limit(limit)

            for inn in image_repo:
                log.info('get_public_image image_uuid: %s' % (inn.image_uuid))
            return True, image_repo
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None

        # 获取镜像排名
    def get_image_rank(self, count=20):
        try:
            Image_repo = self.db_session.query(ImageRepository).filter(
                ImageRepository.is_public == 1, ImageRepository.deleted == 0).order_by(
                desc(ImageRepository.download_num)).limit(count)
            return True, Image_repo
        except Exception, e:
            log.error('get_image_rank is error %s' % (e))
            return False, None

    # 得到平台镜像的个数
    def get_public_image_count(self):
        try:
            from sqlalchemy import func
            count = self.db_session.query(ImageRepository).filter(
                ImageRepository.deleted == 0,
                ImageRepository.is_public == 1
            ).count()
            return True, count
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None


    # 镜像条件搜索
    def get_search_image_repo(self, repovalue, offset, limit):
        try:
            image_repo = self.db_session.query(ImageRepository).filter(
                or_(ImageRepository.repository.like(repovalue),
                    ImageRepository.short_description.like(repovalue),
                    ImageRepository.detail.like(repovalue)
                    ), ImageRepository.is_public == '1', ImageRepository.deleted == '0'
            ).offset(offset).limit(limit)
            return True, image_repo
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None



    # 满足搜索条件镜像的个数
    def get_search_count(self, repovalue):
        try:
            count = self.db_session.query(ImageRepository).filter(
                or_(ImageRepository.repository.like(repovalue),
                    ImageRepository.short_description.like(repovalue),
                    ImageRepository.detail.like(repovalue)
                    ), ImageRepository.is_public == '1', ImageRepository.deleted == '0'
            ).count()
            return True, count
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None

    # 我的没有删除镜像的个数
    def get_image_repo_own_count(self, team_uuid):
        try:
            count = self.db_session.query(ImageRepository).filter(
                ImageRepository.deleted == '0',
                ImageRepository.team_uuid == team_uuid
            ).count()
            return True, count
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None

    # 我的镜像
    def get_image_repo_own(self, team_uuid, offset, limit):
        try:
            image_repo = self.db_session.query(ImageRepository).filter(
                ImageRepository.deleted == '0',
                ImageRepository.team_uuid == team_uuid).offset(offset).limit(limit)  # 组织id区分镜像
            return True, image_repo
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None


    # 得到我的镜像满足搜索条件的个数
    def get_image_repo_own_search_count(self, repovalue, team_uuid):
        try:
            count = self.db_session.query(ImageRepository).filter(
                or_(ImageRepository.repository.like(repovalue),
                    ImageRepository.short_description.like(repovalue),
                    ImageRepository.detail.like(repovalue)
                    ), ImageRepository.deleted == '0', ImageRepository.team_uuid == team_uuid
            ).count()
            return True, count
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None

    # 得到满足搜索条件的我的镜像
    def get_image_repo_own_search(self, repovalue, team_uuid, offset, limit):
        try:
            image_repo = self.db_session.query(ImageRepository).filter(
                or_(ImageRepository.repository.like(repovalue),
                    ImageRepository.short_description.like(repovalue),
                    ImageRepository.detail.like(repovalue)
                    ), ImageRepository.deleted == '0', ImageRepository.team_uuid == team_uuid
            ).offset(offset).limit(limit)
            return True, image_repo
        except Exception, e:
            log.error('get_image_repo_own_search is error %s' % (e))
            return False, None






    # 删除镜像
    def delRepo(self, repoid, team_uuid):
        try:

            image_repo = self.db_session.query(ImageRepository).filter(ImageRepository.image_uuid == repoid).first()

            if image_repo is None:
                log.error('image no have: %' + str(repoid))
                return False

            # if image_repo.team_uuid != team_uuid:
            #     return request_result(806)

            self.db_session.query(ImageRepository).filter(ImageRepository.image_uuid == repoid,
                                                     ImageRepository.team_uuid == team_uuid
                                                     ).update({"deleted": '1'})
            self.db_session.commit()
            return True
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            self.db_session.rollback()
            return False

    # 镜像名是否存在
    def get_image_repo_name_exist(self, imagename):
        try:
            log.info('get_image_repo_name_exist begin')
            image_repo = self.db_session.query(ImageRepository).filter(ImageRepository.repository == imagename).first()
            log.info('get_image_repo_name_exist end')

            if image_repo is None:
                log.info('get_image_repo_name_exist not exist')
                return False, None
            log.info('get_image_repo_name_exist is end')
            return True, image_repo
        except Exception, e:
            log.error('get_image_repo_name_exist is error %s' % (e))
            return False, None

    # push 通知
    def image_repo_push_event(self, repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr):
        try:
            ret = self.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == repository,
                                                              RepositoryEvents.tag == tag).first()
            if ret is None:
                repo_enents = RepositoryEvents(repository=repository, url=url, length=length,
                                               tag=tag, actor=actor, action=action, creation_time=timestamp,
                                               update_time=timestamp, digest=digest, size=size, repo_id=repo_id,
                                               source_instanceID=source_instanceID, source_addr=source_addr)

                self.db_session.add(repo_enents)
            else:
                self.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == repository,
                                                            RepositoryEvents.tag == tag).update(
                    {"action": action, "url": url, "length": length, "actor": actor, "update_time": timestamp,
                     "digest": digest, "size": size, "repo_id": repo_id, "source_instanceID": source_instanceID,
                     "source_addr": source_addr})
            self.db_session.commit()
            return True
        except Exception, e:
            self.db_session.rollback()
            log.error('image_repo_push_event is error %s' % (e))
            return False


    # 下载次数加1  pull
    def image_repo_download(self, image, action):
        try:

            log.info('image_repo_download begin')
            image_repo = self.db_session.query(ImageRepository).filter(ImageRepository.repository == image).first()
            if image_repo is None:
                log.error('auto_ImageRepository is error no have %s' % (image))
                return False

            log.info('image_repo_download begin 0')

            download_num = int(image_repo.download_num) + 1

            if 'push' == action and image_repo.deleted == 1:  # 已经被标记删除的镜像，再次push 恢复非删除状态
                self.db_session.query(ImageRepository).filter(ImageRepository.repository == image).update(
                    {"deleted": '0'})
            elif 'pull' == action:
                self.db_session.query(ImageRepository).filter(ImageRepository.repository == image).update(
                    {"download_num": download_num, "deleted": '0'})
            self.db_session.commit()

            if image_repo.logo == '' or image_repo.logo is None:  # 判断logo 是否为空
                self.AutoSetLogo(repositoryname=image)

        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            self.db_session.rollback()
            return False


    # 设置图像
    def AutoSetLogo(self, repositoryname):
        try:
            from pyTools.tools.images import setRepoLogo
            import conf.conf as CONF

            dd = setRepoLogo(repositoryname, fonttype=CONF.FONTTYPE, localpath=CONF.LOCAL_PATH,
                             remopath=CONF.RepositoryObject, access_key_id=CONF.AccessKeyID,
                             access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
                             bucker_name=CONF.BucketName)

            if dd is False:
                log.error('AutoSetLogo is error')
                return False

            log.info('setRepoLogo : %s' % (dd))

            self.db_session.query(ImageRepository).filter(ImageRepository.repository == repositoryname).update(
                {'logo': dd}
            )
            self.db_session.commit()
            return True
        except Exception, e:
            log.error('AutoSetLogo is error %s' % (e))
            self.db_session.rollback()
            return False


    # image_repo_pull_event

    def image_repo_pull_event(self, repository, tag, actor, url, length, action, timestamp, digest, repo_id, size, source_instanceID, source_addr):
        try:
            ret = self.db_session.query(RepositoryPull).filter(RepositoryPull.repository == repository,
                                                            RepositoryPull.tag == tag,
                                                            RepositoryPull.actor == actor).first()

            if ret is None:
                repo_pull = RepositoryPull(repository=repository, url=url, length=length, tag=tag, actor=actor,
                                           action=action, timestamp=timestamp,
                                           digest=digest, repo_id=repo_id, size=size,
                                           source_instanceID=source_instanceID,
                                           source_addr=source_addr)
                self.db_session.add(repo_pull)
            else:
                self.db_session.query(RepositoryPull).filter(RepositoryPull.repository == repository,
                                                          RepositoryPull.tag == tag,
                                                          RepositoryPull.actor == actor).update(
                    {"action": action, "url": url, "length": length, "timestamp": timestamp, "digest": digest,
                     "size": size, "repo_id": repo_id, "source_instanceID": source_instanceID,
                     "source_addr": source_addr})

            self.db_session.commit()
            return True
        except Exception, e:
            log.error('image_repo_pull_event is error %s' % (e))
            self.db_session.rollback()
            return False


    # 修改镜像信息
    def modify_image_repo(self, image_uuid, detail_type, detail):
        try:
            image_repo = self.db_session.query(ImageRepository).filter(ImageRepository.image_uuid == image_uuid).first()

            if image_repo is None:
                return False

            self.db_session.query(ImageRepository).filter(ImageRepository.image_uuid == image_uuid).update(
                {detail_type: detail}
            )
            self.db_session.commit()
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            self.db_session.rollback()
            return False, None

    def sdsd(self):
        try:
            log.info('sdsd')
        except Exception, e:
            log.error('auto_ImageRepository is error %s' % (e))
            return False, None
