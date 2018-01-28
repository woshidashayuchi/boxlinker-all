#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/9 16:19
"""


import json
import requests


from conf.conf import ucenter_api_prefix

from common.logs import logging as log

# 验证用户名和密码, 返回: bool, token
def username_password_authentication(username, password):
    url_suffix = '/api/v1.0/ucenter/tokens'
    url = ucenter_api_prefix + url_suffix
    body = {"user_name": username, "password": password}
    headers = {'content-type': "application/json"}
    body = json.dumps(body)
    log.info('username_password_authentication post url: %s' % (url))
    ret = requests.post(url=url, data=body, headers=headers)

    if ret.json()['status'] == 0:
        log.info('username_password_authentication is ok token: %s' % (ret.json()['result']['user_token']))
        return True, ret.json()['result']['user_token']

    return False, ''

# 获取一个用户下的组织; {'team_name': 'team_uuid'}
def user_teams(token):
    url_suffix = '/api/v1.0/ucenter/teams'
    url = ucenter_api_prefix + url_suffix
    headers = {'content-type': "application/json",
               'token': token}

    ret = requests.get(url=url, headers=headers)

    log.info('user_teams-->: %s' % (ret.json()))
    if ret.json()['status'] == 0:
        tname_tuuid_dict = {x['team_name']: x['team_uuid'] for x in ret.json()['result']['team_list'] if x['status'] == 'enable'}
        return True, tname_tuuid_dict
    return False, ''


# 通过组织切换token
def change_token_by_team(token, team_uuid):
    url_suffix = '/api/v1.0/ucenter/tokens'
    url = ucenter_api_prefix + url_suffix
    headers = {'content-type': "application/json",
               'token': token}

    body = {"team_uuid": team_uuid}
    body = json.dumps(body)
    ret = requests.put(url=url, headers=headers, data=body)

    log.info('change_token_by_team token: %s, ret.json: %s' % (token, ret.json()))
    if ret.json()['status'] == 0:
        return True, ret.json()['result']['orga_token']
    return False, ''



# 得到一个用户对应组织下的token
def username_password_teams_token(username, password, team_name=None):
    retbool, token = username_password_authentication(username=username, password=password)

    if retbool is False:
        return retbool, token

    retbool, tname_tuuid_dict = user_teams(token=token)

    if team_name is None:
        team_name = username

    log.info('username_password_teams_token tname_tuuid_dict: %s' % (tname_tuuid_dict))

    if team_name not in tname_tuuid_dict:
        return False, None
    else:
        team_uuid = tname_tuuid_dict[team_name]

    retbool, orga_token = change_token_by_team(token=token, team_uuid=team_uuid)



    if retbool is False:
        return retbool, orga_token
    return retbool, orga_token



def teams_info(team_uuid, token):
    url_suffix = '/api/v1.0/ucenter/teams/' + str(team_uuid)
    url = ucenter_api_prefix + url_suffix
    log.info('teams_info url: %s' % (url))
    headers = {'content-type': "application/json",
               'token': token}

    ret = requests.get(url=url, headers=headers)
    return ret.json()


# 组织用户添加
def add_user_team(token, user_uuid, role_uuid):
    url_suffix = '/api/v1.0/ucenter/usersteams'
    url = ucenter_api_prefix + url_suffix
    log.info('add_user_team url: %s' % (url))
    headers = {'content-type': "application/json",
               'token': token}

    body = {"user_uuid": user_uuid, 'role_uuid': role_uuid}
    body = json.dumps(body)
    ret = requests.post(url=url, headers=headers, data=body)
    return ret.json()

# 通过组织名获取组织uuid
def get_team_uuid(token, team_name):
    url_suffix = '/api/v1.0/ucenter/teams?team_name=' + team_name + '&uuid_info=true'
    url = ucenter_api_prefix + url_suffix

    log.info('get_team_uuid url: %s' % (url))
    headers = {'content-type': "application/json",
               'token': token}

    ret = requests.get(url=url, headers=headers)
    if 0 == ret.json()['status']:
        return True, ret.json()['result']
    return False, None




if __name__ == '__main__':
    # retbool, token = username_password_authentication(username='liuzhangpei', password='QAZwsx123')
    #
    # print retbool, token

#     if retbool is False:
#         exit(-1)
#
#
#
#     teams_info(team_uuid='401ee13d-9524-44bc-b0c8-1f8a52facd4d', token=token)
#     teams_info(team_uuid='3405850e-134d-4d72-aa00-d70296eed084', token=token)
#
# # # boxlinker, password: QAZwsx123, team_name: sdsddsdsss
    retbool, token = username_password_teams_token(username='zhangsai', password='111111', team_name='zhangsan')
    print token
#
#     print retbool, token
#
#
#     add_user_team(token=token, user_uuid='c9b7decb-5726-42ac-9aac-b0b5911068e5', role_uuid='admin')
#
#     retbool, ret = get_team_uuid(token, 'liuzhangpei')
#     print ret
