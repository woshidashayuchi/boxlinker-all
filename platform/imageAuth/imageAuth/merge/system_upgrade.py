#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/27 10:39
"""

import json
import requests
from imageAuth.merge import conf
from imageAuth.merge import confrelease
from pyTools.tools.mysql_base import MysqlInit
import uuid

# http://192.168.1.7:8001/api/v1.0/ucenter/users
ucenter_api = 'https://ucenter.boxlinker.com'
ucenter_api_prefix = 'https://ucenter.boxlinker.com'

# 验证用户名和密码, 返回: bool, token
def username_password_authentication(username, password):
    url_suffix = '/api/v1.0/ucenter/tokens'
    url = ucenter_api_prefix + url_suffix
    body = {"user_name": username, "password": password}
    headers = {'content-type': "application/json"}
    body = json.dumps(body)
    ret = requests.post(url=url, data=body, headers=headers)

    if ret.json()['status'] == 0:
        return True, ret.json()['result']['user_token']

    return False, ''


# 通过组织名获取组织uuid
def get_team_uuid(token, team_name):
    url_suffix = '/api/v1.0/ucenter/teams?team_name=' + team_name + '&uuid_info=true'
    url = ucenter_api_prefix + url_suffix

    headers = {'content-type': "application/json",
               'token': token}

    ret = requests.get(url=url, headers=headers)
    if 0 == ret.json()['status']:
        return True, ret.json()['result']
    return False, None

def signin(user_name, password, email):
    url_suffix = '/api/v1.0/ucenter/users'
    url_request = ucenter_api + url_suffix
    data = {
        "user_name": user_name,
        "password": password,
        "email": email
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url=url_request, data=json.dumps(data), headers=headers)

    response_json = response.json()
    print response_json

    if 0 != response_json['status']:
        print 'is error'
        print user_name
        print email


class OldDB(MysqlInit):

    def __init__(self):
        super(OldDB, self).__init__(conf)

    def del_image_repo_by_uuid(self, repo_uuid):
        """通过image id删除一个镜像"""
        sql = "delete from image_repository where image_uuid='%s'" % (repo_uuid)
        return super(OldDB, self).exec_update_sql(sql)

    def get_image_repo(self):
        """ 获取镜像 """
        sql = "select repository, is_public, short_description, detail, deleted from image_repository "
        return super(OldDB, self).exec_select_sql(sql)

    def get_all_image_repo_name(self):
        old_repo_list = self.get_image_repo()
        name_dict = {str(node[0]): str(node[0]).split('/')[0] for node in old_repo_list}
        return name_dict

    def get_all_user(self):
        """ 获取全部镜像 """
        sql = "select username, email from user "
        return super(OldDB, self).exec_select_sql(sql)

    def get_old_user_name(self):
        old_user_list = self.get_all_user()
        for node in old_user_list:
            user_name, email = node
            print node[0]
            print node[1]
            signin(user_name=user_name, email=email, password='123456')
            return True

        # name = [str(node[0]).split('/')[0] for node in old_repo_list]
        # print name
        #
        # name_dict = {str(node[0]).split('/')[0]: str(node[0]).split('/')[1] for node in old_repo_list}
        # print name_dict
        # print name_dict.iterkeys()
        # print name_dict.keys()

class NewDbManager():
    def __init__(self):
        print 'sss'

    def get_team_uuid(self, user_name, password, team_name):
        retbool, token = username_password_authentication(username=user_name, password=password)

        retbool, team_info = get_team_uuid(token=token, team_name=team_name)
        if retbool is False:
            return None
        team_uuid = team_info['team_uuid']
        return team_uuid




class NewDb(MysqlInit):
    def __init__(self):
        super(NewDb, self).__init__(confrelease)

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
        return super(NewDb, self).exec_update_sql(sql_init_repo, sql_init_acl)


    def update_image(self, args):
        """ 设置一个镜像的logo url """
        sql = "update image_repository set is_public=%(is_public)s, short_description=%(short_description)s, \
              detail=%(detail)s, deleted=%(deleted)s where repository=%(repository)s"
        return super(NewDb, self).exec_update_sql_dict(sql, args=args)


    def insert_image(self, image, team_uuid, is_public):
        image_name = str(image)
        repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, image_name).__str__()
        self.init_image_repo(repo_uuid=repo_uuid, imagename=image_name, resource_type='image_repo',
                                           user_uuid='0', admin_uuid='global', team_uuid=team_uuid,
                                           project_uuid='0', is_public=is_public)




def one():
    old = OldDB()
    name_dict = old.get_all_image_repo_name()
    ndm = NewDbManager()

    new = NewDb()

    for imagename in name_dict:
        user_name = name_dict[imagename]
        team_name = user_name
        if user_name == 'library':
            is_publice = '1'
        else:
            is_publice = '0'

        if user_name == 'boxlinker':
            password = 'QAZwsx123'
        elif user_name == 'allreach':
            user_name = 'cabernety'
            team_name = 'allreach'
            password = '123456'
        else:
            password = '123456'

        team_uuid = ndm.get_team_uuid(user_name=user_name, team_name=team_name, password=password)
        if team_uuid is None:
            print user_name
            print team_name
            print 'is error'
        else:
            new.insert_image(image=imagename, team_uuid=team_uuid, is_public=is_publice)


def two_envent():
    old = OldDB()
    image = old.get_image_repo()
    new = NewDb()

    for node in image:
        print node
        repository, is_public, short_description, detail, deleted = node
        print repository
        args = dict()
        args['is_public'] = is_public
        args['repository'] = repository
        args['short_description'] = short_description
        args['detail'] = detail
        args['deleted'] = deleted
        # print repository, is_public, short_description, detail, deleted

        new.update_image(args=args)



if __name__ == '__main__':
    print 'ss'
    two_envent()
    # one()  # 导, 镜像表数据