#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/25 10:42
"""

from common.mysql_base import MysqlInit
from common.logs import logging as log
import uuid

from pyTools.tools.timeControl import get_now_time


class ImageRepoDB(MysqlInit):

    def __init__(self):
        super(ImageRepoDB, self).__init__()

    def del_image_repo_by_uuid(self, repo_uuid):
        """通过image id删除一个镜像"""
        sql = "delete from image_repository where image_uuid='%s'" % (repo_uuid)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def add_resources_acl(self, resource_uuid, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid):
        """ 添加资源的ACL记录 """
        sql = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, \
               team_uuid, project_uuid, user_uuid, create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
              % (resource_uuid, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def add_image_repo(self, repo_uuid, image, team_uuid, short_description='Push by terminals', detail='Push by terminals', is_code=0, download_num=1, is_public=1):
        """ 第一次上传 """
        detail = ''
        sql = "insert into image_repository(image_uuid, team_uuid, repository, \
               is_public, short_description, detail, is_code, download_num, creation_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
              % (repo_uuid, team_uuid, image, str(is_public), short_description, detail, str(is_code), str(download_num))
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def get_repo_uuid_by_image_name(self, imagename):
        """通过一个镜像获取镜像的uuid, 获取一个镜像的uuid """
        sql = "select image_uuid from image_repository where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_select_sql(sql)


    def get_imagename_tag_by_tagid(self, tagid):
        """ 通过 tagid 得到 """
        sql = "select repository, tag from repository_events where id='%s'" % (tagid)
        return super(ImageRepoDB, self).exec_select_sql(sql)


    def get_image_tagid(self, repo_name, repo_tag):
        """ 通过镜像名和tag 获取 tagid """
        sql = "select id from repository_events where repository='%s' and tag='%s'" % (repo_name, repo_tag)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_repo_detail_by_uuid(self, repoid):
        """获取一个镜像的详细"""
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
              download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type from image_repository where image_uuid='%s' and deleted=0" % (repoid)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_repo_publice(self, repoid):
        """获取一个镜像的 is_public 属性"""
        sql = "select is_public from image_repository where image_uuid='%s'" % (repoid)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_repo_team_uuid(self, repoid):
        """获取一个镜像的 team_uuid 属性"""
        sql = "select team_uuid from image_repository where image_uuid='%s'" % (repoid)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_repo_detail_by_imagename(self, imagename):
        """获取一个镜像的详细, 镜像名是否存在"""
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
              download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type from image_repository where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_select_sql(sql)


    def get_image_uuid_and_team_uuid_by_imagename(self, imagename):
        """ image_uuid, team_uuid 镜像名是否存在"""
        sql = "select image_uuid, team_uuid from image_repository where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def init_image_repo(self, repo_uuid, imagename, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid, is_public=1):
        """ 初始化记录 """

        detail = ''
        sql_init_repo = "insert into image_repository(image_uuid, team_uuid, repository, \
                         is_public, short_description, detail, is_code, download_num, creation_time, update_time) \
                         values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
                         % (repo_uuid, team_uuid, imagename, str(is_public), detail, detail, str(0), str(0))

        sql_init_acl = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, \
                        team_uuid, project_uuid, user_uuid, create_time, update_time) \
                        values('%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
                        % (repo_uuid, resource_type, user_uuid, admin_uuid, team_uuid, project_uuid)
        return super(ImageRepoDB, self).exec_update_sql(sql_init_repo, sql_init_acl)


    def get_image_repo_uuid_by_name(self, imagename):
        """通过镜像名得到镜像, uuid"""
        sql = "select image_uuid from image_repository where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_select_sql(sql)



    def modify_image_repo(self, image_uuid, detail_type, detail):
        """修改镜像信息"""
        sql_detail = "update image_repository set detail=%(detail)s, update_time=now() where image_uuid=%(image_uuid)s"
        sql_short_description = "update image_repository set short_description=%(detail)s, update_time=now() where image_uuid=%(image_uuid)s"
        sql_is_public = "update image_repository set is_public=%(detail)s, update_time=now() where image_uuid=%(image_uuid)s"

        detail_dict =dict()
        detail_dict['image_uuid'] = image_uuid
        detail_dict['detail'] = detail
        if 'detail' == detail_type:
            sql = sql_detail
        elif 'short_description' == detail_type:
            sql = sql_short_description
        elif 'is_public' == detail_type:
            sql = sql_is_public

        return super(ImageRepoDB, self).exec_update_sql_dict(sql, detail_dict)
        # return super(ImageRepoDB, self).exec_update_sql(sql)

    def get_image_repo_own_search_count(self, repovalue, team_uuid):
        """ 得到我的镜像满足搜索条件的个数,  repovalue 不需要再 % """
        repovalue = '%' + repovalue + '%'
        sql = "select count(*) from image_repository where (repository like '%s' or short_description like '%s' or detail like '%s') and deleted='0' and team_uuid='%s'" \
               % (repovalue, repovalue, repovalue, team_uuid)
        return super(ImageRepoDB, self).exec_select_sql(sql)[0][0]

    def get_search_image_repo(self, repovalue, offset, limit):
        """ 镜像条件搜索 """
        repovalue = '%' + repovalue + '%'
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
              download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type \
              from image_repository \
              where (repository like '%s' or short_description like '%s' or detail like '%s') and is_public='1' and deleted=0 limit %s offset %s" \
               % (repovalue, repovalue, repovalue, limit, offset)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def image_repo_download_add(self, imagename):
        """ pull 操作, 下载加 1 """
        sql = "update image_repository set download_num=download_num+1 where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def image_repo_set_deleted_by_imagename(self, imagename, is_deleted=True): # 已经被标记删除的镜像，再次push 恢复非删除状态
        """ 设置镜像的删除状态, is_deleted=True 表示删除, False表示设置为不删除 """
        if is_deleted:
            sql = "update image_repository set deleted=1 where repository='%s'" % (imagename)
        else:
            sql = "update image_repository set deleted=0 where repository='%s'" % (imagename)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def get_public_image(self, offset, limit):
        """ 获取平台镜像, 分页 """
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
               download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type \
               from image_repository where is_public=1 \
               limit %s offset %s" % (limit, offset)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_image_rank(self, count=20):
        """ 镜像排名, 按照下载次数进行排名, 默认取前20条数据 """
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, \
               short_description, detail, \
               download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type \
               from image_repository where is_public=1 and deleted=0 order by download_num DESC limit %s" % (count)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_public_image_count(self):
        """ 得到平台镜像的个数 """
        sql = "select count(*) from image_repository where deleted='0' and is_public=1"
        return super(ImageRepoDB, self).exec_select_sql(sql)[0][0]

    # 先调用 from pyTools.tools.images import setRepoLogo 生成图片,并上传到 oss, import conf.conf as CONF
    #         dd = setRepoLogo(repositoryname, fonttype=CONF.FONTTYPE, localpath=CONF.LOCAL_PATH,
    #                          remopath=CONF.RepositoryObject, access_key_id=CONF.AccessKeyID,
    #                          access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
    #                          bucker_name=CONF.BucketName)
    def image_repo_set_logo(self, imagename, logourl):
        """ 设置一个镜像的logo url """
        sql = "update image_repository set logo='%s' where repository='%s'" % (logourl, imagename)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def get_image_repo_own(self, team_uuid, offset, limit):
        """ 我的镜像, 组织 uuid 区分镜像 """
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
               download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type \
               from image_repository where deleted=0 and team_uuid='%s' \
               limit %s offset %s" % (team_uuid, limit, offset)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def set_image_repo_deleted(self, image_uuid, team_uuid, deleted):
        """ 删除镜像 """
        sql = "update image_repository set deleted='%s' where image_uuid='%s' and team_uuid='%s'" % (deleted, image_uuid, team_uuid)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def get_image_repo_own_search(self, repovalue, team_uuid, offset, limit):
        """ 得到满足搜索条件的我的镜像 """
        repovalue = '%' + repovalue + '%'
        sql = "select image_uuid, team_uuid, repository, deleted, creation_time, update_time, is_public, short_description, detail, \
               download_num, enshrine_num, review_num, version, latest_version, pushed, is_code, logo, src_type \
               from image_repository where (repository like '%s' or short_description like '%s' or detail like '%s') and deleted=0 and team_uuid='%s' \
               limit %s offset %s" % (repovalue, repovalue, repovalue, team_uuid, limit, offset)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def get_search_count(self, repovalue):
        """ 满足搜索条件镜像的个数 """
        repovalue = '%' + repovalue + '%'
        sql = "select count(*) from image_repository \
               where (repository like '%s' or short_description like '%s' or detail like '%s') and deleted='0' and is_public=1" \
               % (repovalue, repovalue, repovalue)
        return super(ImageRepoDB, self).exec_select_sql(sql)[0][0]


    def get_image_repo_own_count(self, team_uuid):
        """ 我的没有被删除的镜像个数 """
        sql = "select count(*) from image_repository where deleted='0' and team_uuid='%s'" % (team_uuid)
        return super(ImageRepoDB, self).exec_select_sql(sql)[0][0]


    def get_image_repo_events(self, repository, tag):
        """ 通过镜像名和标签验证是否已经上传"""
        sql = "select count(*) from repository_events where repository='%s' and tag='%s'" % (repository, tag)
        return super(ImageRepoDB, self).exec_select_sql(sql)[0][0]

    def add_image_repo_events(self, repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr):
        """ 添加, events 记录 """
        sql = "insert into \
               repository_events(repository, url, lengths, tag, actor, actions, \
               digest, sizes, repo_id, source_instanceID, source_addr, creation_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now(), now())" \
              % (repository, url, length, tag, actor, action, digest, size, repo_id, source_instanceID, source_addr)
        return super(ImageRepoDB, self).exec_update_sql(sql)

    def modify_image_repo_events(self, repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr):
        """ 修改, events 记录 """
        sql = "update repository_events \
               set actions='%s', url='%s', lengths='%s', actor='%s', digest='%s', sizes='%s', repo_id='%s', \
               source_instanceID='%s', source_addr='%s', update_time=now() \
               where repository='%s' and tag='%s'" % \
              (action, url, length, actor, digest, size, repo_id, source_instanceID, source_addr, repository, tag)
        return super(ImageRepoDB, self).exec_update_sql(sql)


    def get_repo_events_by_imagename(self, imagerep_name):
        """获取一个镜像的全部 RepositoryEvents 信息"""
        sql = "select id, repository, url, lengths, tag, actor, actions, digest, sizes, repo_id, \
               source_instanceID, source_addr, deleted, creation_time, update_time \
               from repository_events where repository='%s'" % (imagerep_name)
        return super(ImageRepoDB, self).exec_select_sql(sql)

    def image_repo_push_event(self, repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr):
        """ 通知 """
        ret = self.get_image_repo_events(repository=repository, tag=tag)
        if 0 == ret:
            return self.add_image_repo_events(repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr)
        else:
            return self.modify_image_repo_events(repository, tag, url, length, actor, action, timestamp,
                              digest, size, repo_id, source_instanceID, source_addr)


    def get_repo_publice_manger(self, repoid):
        ret = self.get_repo_publice(repoid=repoid)
        if len(ret) > 0:
            return True if 1 == ret[0][0] else False
        else:
            return False


        # get_repo_team_uuid
    def get_repo_team_uuid_manger(self, repoid):
        ret = self.get_repo_team_uuid(repoid=repoid)
        print ret
        if len(ret) > 0:
            return ret[0][0]
        return None





if __name__ == '__main__':
    IRDB = ImageRepoDB()

    # ret = IRDB.get_repo_detail(repoid='02a7f39-2208-3415-baf2-62ae7bd3c316')
    # print type(ret)
    # print ret

    # while True:
    #     import time
    #     time.sleep(1)
    #     ret = IRDB.get_image_repo_uuid_by_name(imagename='zhangsan/paussdsd')
    #     print ret
    # #
    # ret = IRDB.get_repo_uuid_by_image_name(imagename='sssss')
    # print ret[0][0]


    # ret = IRDB.get_repo_publice_manger("239f8d4e-f3ce-3788-8c83-bc9d847d113a")
    # print ret
    # ret = IRDB.get_repo_team_uuid_manger("239f8d4e-f3ce-3788-8c83-bc9d847d113a")
    # print ret



    # ret = IRDB.get_repo_detail_by_imagename('sss')
    # print ret
    #
    ret = IRDB.get_image_uuid_and_team_uuid_by_imagename('sss')
    print ret



    # ret = IRDB.modify_image_repo(image_uuid='002a7f39-2208-3415-baf2-62ae7bd3c316', detail_type='is_public', detail=1)
    # print ret

    # ret = IRDB.get_image_repo_own_search_count('%搜dsds%', '502f8981-6217-4310-ad68-c5c57079e32b')
    # print ret

    # ret = IRDB.image_repo_set_deleted_by_imagename(imagename='liuzhangpei/phpmysd', is_deleted=False)
    # print ret
    #
    # ret = IRDB.get_public_image(10, 10)
    # print ret
    # ret = IRDB.get_image_rank()
    # print ret
    # ret = IRDB.get_public_image_count()
    # print ret

    # ret = IRDB.image_repo_set_logo(imagename='liuzhangpei/phpmysd', logourl='sdsdsdsd')
    # print ret

    # ret = IRDB.get_search_image_repo(repovalue='s', limit=5, offset=3)
    # print ret
    #
    # ret = IRDB.set_image_repo_deleted(image_uuid='e69884d5-1763-3288-a1df-1ce9cb191061', team_uuid='2e8e7b37-a957-4770-9075-aaa67eaa49ce', deleted='1')
    # print ret

    # ret = IRDB.get_image_repo_own_search(repovalue='z', team_uuid='2e8e7b37-a957-4770-9075-aaa67eaa49ce', offset=1, limit=3)
    # print ret

    # ret = IRDB.get_search_count(repovalue='z')
    # print ret

    # ret = IRDB.get_image_repo_events(repository='sss', tag='de')
    # print type(ret)
    # print ret

    # ret = IRDB.get_repo_detail_by_uuid('4bd1ca3f-1752-33e6-b8d0-b9348a58ced7')
    # print ret

    # ret = IRDB.get_repo_events_by_imagename('liuzhangpei/phpmyadmi')
    # print ret



