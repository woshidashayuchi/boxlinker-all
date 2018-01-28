#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/28 13:46
"""

import time
from common.mysql_base import MysqlInit
from common.logs import logging as log
import uuid

from pyTools.tools.timeControl import get_now_time

from imageAuth.db import ormData as ORMDT


class OauthDb(MysqlInit):

    def __init__(self):
        super(OauthDb, self).__init__()


    def del_code_oauth(self, team_uuid, src_type):
        """ 删除code_oauth """
        sql = "delete from code_oauth where team_uuid='%s' and src_type='%s'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def get_code_oauth(self, team_uuid, src_type):
        """根据组织uuid 和 第三方类型, 获取 CodeOauth 信息"""
        sql = "select code_oauth_uuid, team_uuid, src_type, git_name, git_emain, git_uid, access_token from code_oauth where team_uuid='%s' and src_type='%s'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_select_sql(sql)

    def get_code_oauth_type(self, team_uuid):
        """ 获取一个用户的绑定类型 """
        sql = "select src_type, git_name from code_oauth where team_uuid='%s'" % (team_uuid)
        return super(OauthDb, self).exec_select_sql(sql)

    def save_access_token(self, code_oauth_uuid, team_uuid, src_type, access_token):
        """ 存储 access_token """
        sql = "insert into code_oauth(code_oauth_uuid, team_uuid, src_type, access_token) \
               values('%s', '%s', '%s', '%s')" \
              % (code_oauth_uuid, team_uuid, src_type, access_token)
        return super(OauthDb, self).exec_update_sql(sql)

    def update_code_oauth_only_user(self, team_uuid, src_type, git_name, git_emain, git_uid):
        """ 仅仅更新 CodeOauth 中的用户信息 """
        sql = "update code_oauth set git_name='%s', git_emain='%s', git_uid='%s' where team_uuid='%s' and src_type='%s'" \
              % (git_name, git_emain, git_uid, team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def update_code_oauth_access_token(self, team_uuid, src_type, access_token):
        """ 更新 CodeOauth 的 access_token """
        sql = "update code_oauth set  access_token='%s' where team_uuid='%s' and src_type='%s'" \
              % ( access_token, team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)


    def update_code_oauth(self, team_uuid, src_type, git_name, git_emain, git_uid, access_token):
        """ 更新 CodeOauth 的所有信息 """
        sql = "update code_oauth set git_name='%s', git_emain='%s', git_uid='%s', access_token='%s' \
               where team_uuid='%s' and src_type='%s'" \
              % (git_name, git_emain, git_uid, access_token, team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def update_code_repo_web_hook(self, team_uuid, repo_name, repo_hook_token, hook_url, src_type):
        sql = "update code_repo set is_hook='1', repo_hook_token='%s', hook_url='%s' \
               where team_uuid='%s' and repo_name='%s' and src_type='%s'" \
              % (repo_hook_token, hook_url, team_uuid, repo_name, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def get_code_repo(self, team_uuid, src_type):
        """ 获取代码项目 """
        sql = "select code_repo_uuid, team_uuid, repo_uid, repo_id, repo_name, repo_branch, repo_hook_token, hook_url, \
               html_url, ssh_url, git_url, description, is_hook, src_type, deleted, creation_time, update_time \
               from code_repo where team_uuid='%s' and src_type='%s'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_select_sql(sql)

    def get_code_repo_repo_id(self, team_uuid, src_type):
        """ 获取代码项目的repo_id """
        sql = "select repo_id from code_repo where team_uuid='%s' and src_type='%s'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_select_sql(sql)

    def set_all_code_repo_deleted(self, team_uuid, src_type):
        """ 全部标记已经删除 """
        sql = "update code_repo set deleted='1' where team_uuid='%s' and src_type='%s'" \
              % (team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def del_code_repo_deleted(self, team_uuid, src_type):
        """ 删除已经被标记的删除的项目 """
        sql = "delete from code_repo where team_uuid='%s' and src_type='%s' and deleted='1'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)


    def del_code_repo(self, team_uuid, src_type):
        """ 删除所有项目 """
        sql = "delete from code_repo where team_uuid='%s' and src_type='%s'" % (team_uuid, src_type)
        return super(OauthDb, self).exec_update_sql(sql)

    def add_code_repo(self, team_uuid, repo_uid, repo_id, repo_name, repo_branch, html_url, ssh_url, git_url, description, src_type):
        """ 添加新记录 """
        sql = "insert into code_repo(team_uuid, repo_uid, repo_id, repo_name, repo_branch, html_url, ssh_url, git_url, \
               description, src_type, is_hook, hook_url, repo_hook_token, deleted, creation_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '0', '0', '', '0', now(), now())" \
              % (team_uuid, repo_uid, repo_id, repo_name, repo_branch, html_url, ssh_url, git_url, description, src_type)
        return super(OauthDb, self).exec_update_sql_dict(sql)

    def add_code_repo_dict(self, argsd):
        """ 添加新记录 """
        sql = "insert into code_repo(team_uuid, repo_uid, repo_id, repo_name, repo_branch, html_url, ssh_url, git_url, \
               description, src_type, is_hook, deleted, creation_time, update_time) \
               values(%(team_uuid)s, %(repo_uid)s, %(repo_id)s, %(repo_name)s, %(repo_branch)s, \
                %(html_url)s, %(ssh_url)s, %(git_url)s, %(description)s, %(src_type)s, '0', '0', now(), now())"
        return super(OauthDb, self).exec_update_sql_dict(sql, argsd)

    def modify_code_repo_dict(self, argsd):
        """ 添加新记录 """
        sql = "update code_repo set repo_name=%(repo_name)s, repo_branch=%(repo_branch)s, html_url=%(html_url)s, \
               ssh_url=%(ssh_url)s, git_url=%(git_url)s, \
               description=%(description)s, update_time=now(), deleted='0' \
               where team_uuid=%(team_uuid)s and repo_id=%(repo_id)s and src_type=%(src_type)s"
        return super(OauthDb, self).exec_update_sql_dict(sql, argsd)

    def set_code_repo_hook_token(self, repo_hook_token, team_uuid, src_type, repo_name):
        """ 设置hook token """
        sql = "update code_repo set is_hook='1', repo_hook_token='%s' \
               where team_uuid='%s' and src_type='%s' and repo_name='%s'" \
               % (repo_hook_token, team_uuid, src_type, repo_name)
        return super(OauthDb, self).exec_update_sql(sql)





class OauthDbManager(object):
    def __init__(self):
        self.oauthdb = OauthDb()

    def add_code_repo_dict(self, argsd):
        return self.oauthdb.add_code_repo_dict(argsd)

    def modify_code_repo_dict(self, argsd):
        return self.oauthdb.modify_code_repo_dict(argsd)

    def set_all_code_repo_deleted(self, team_uuid, src_type):
        return self.oauthdb.set_all_code_repo_deleted(team_uuid, src_type)

    def del_code_repo_deleted(self, team_uuid, src_type):
        return self.oauthdb.del_code_repo_deleted(team_uuid, src_type)




    def del_code_oauth(self, team_uuid, src_type):
        return self.oauthdb.del_code_oauth(team_uuid, src_type)


    def del_code_repo(self, team_uuid, src_type):
        return self.oauthdb.del_code_repo(team_uuid, src_type)


    def get_code_repo_repo_id(self, team_uuid, src_type):
        ret = self.oauthdb.get_code_repo_repo_id(team_uuid, src_type)
        if len(ret) <= 0:
            return False, None
        return True, [node[0] for node in ret]

    def get_code_oauth(self, team_uuid, src_type):
        """ 根据组织uuid 和 第三方类型, 获取 CodeOauth 信息 """
        ret = self.oauthdb.get_code_oauth(team_uuid, src_type)
        if len(ret) <= 0:
            return False, None

        code_oauth_uuid, team_uuid, src_type, git_name, git_emain, git_uid, access_token = ret[0]

        codeOauth = ORMDT.CodeOauth
        codeOauth.code_oauth_uuid = code_oauth_uuid
        codeOauth.team_uuid = team_uuid
        codeOauth.src_type = src_type
        codeOauth.git_name = git_name
        codeOauth.git_emain = git_emain
        codeOauth.git_uid = git_uid
        codeOauth.access_token = access_token
        return True, codeOauth

    def save_access_token(self, team_uuid, src_type, access_token):
        """ 存储 access_token """
        time_str = str(time.time())
        auth_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(team_uuid) + str(src_type) + time_str).__str__()
        return self.oauthdb.save_access_token(code_oauth_uuid=auth_id, team_uuid=team_uuid, src_type=src_type, access_token=access_token)

    def update_code_oauth_only_user(self, team_uuid, src_type, git_name, git_emain, git_uid):
        try:
            self.oauthdb.update_code_oauth_only_user(team_uuid, src_type, git_name, git_emain, git_uid)
            return True
        except Exception, e:
            log.error('update_code_oauth_only_user is error%s' % (e))
            return False

    def update_code_oauth(self, team_uuid, src_type, git_name, git_emain, git_uid, access_token):
        try:
            log.info('update_code_oauth access_token')
            self.oauthdb.update_code_oauth(team_uuid, src_type, git_name, git_emain, git_uid, access_token)
            return True
        except Exception, e:
            log.error('update_code_oauth is error%s' % (e))
            return False

    def update_code_repo_web_hook(self, team_uuid, repo_name, repo_hook_token, hook_url, src_type):
        try:
            self.oauthdb.update_code_repo_web_hook(team_uuid, repo_name, repo_hook_token, hook_url, src_type)
            return True
        except Exception, e:
            log.error('update_code_repo_web_hook is error %s' % (e))
            return False

    def get_code_repo(self, team_uuid, src_type):
        """ 获取代码项目 """
        ret = self.oauthdb.get_code_repo(team_uuid, src_type)
        if ret <= 0:
            return None

        coderepolist = list()
        for node in ret:
            code_repo_uuid, team_uuid, repo_uid, repo_id, repo_name, repo_branch, repo_hook_token, hook_url, \
            html_url, ssh_url, git_url, description, is_hook, src_type, deleted, creation_time, update_time = node
            codeRepo = ORMDT.CodeRepo()

            codeRepo.code_repo_uuid = code_repo_uuid
            codeRepo.team_uuid = team_uuid
            codeRepo.repo_uid = repo_uid
            codeRepo.repo_id = repo_id
            codeRepo.repo_name = repo_name
            codeRepo.repo_branch = repo_branch
            codeRepo.repo_hook_token = repo_hook_token
            codeRepo.hook_url = hook_url
            codeRepo.html_url = html_url
            codeRepo.ssh_url = ssh_url
            codeRepo.git_url = git_url
            codeRepo.description = description
            codeRepo.is_hook = is_hook
            codeRepo.src_type = src_type
            codeRepo.creation_time = creation_time
            codeRepo.update_time = update_time

            coderepolist.append(codeRepo)

        return coderepolist

    def update_code_oauth_access_token(self, team_uuid, src_type, access_token):
        return self.oauthdb.update_code_oauth_access_token(team_uuid, src_type, access_token)

    def get_code_oauth_type(self, team_uuid):
        src_types = self.oauthdb.get_code_oauth_type(team_uuid)
        # li = [{src_type: '1', 'name': git_name} for src_type, git_name in src_types]
        # # [{u'github': '1', 'name': u'livenowhy'}, {u'coding': '1', 'name': u'bowumanman'}]
        li = {src_type: git_name for src_type, git_name in src_types}  # {u'github': u'livenowhy'}
        return li



# 09757939-b6dc-4da3-add6-b3775c8efb7a

if __name__ == '__main__':
    OADBM = OauthDbManager()
    # ret, codeOauth = OADBM.get_code_repo_repo_id(team_uuid='2e8e7b37-a957-4770-9075-aaa67eaa49ce', src_type='github')
    # print ret
    # print codeOauth
    #
    # if 75517981 in codeOauth:
    #     print 'is ok int '
    #
    # if '75517981' in codeOauth:
    #     print 'is ok STR '
    ret = OADBM.get_code_oauth_type(team_uuid='cabb719f-4a9a-475f-89f1-717231ae7eb5')
    print ret
