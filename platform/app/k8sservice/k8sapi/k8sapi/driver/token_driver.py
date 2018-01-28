# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/10
from common.logs import logging as log
from conf import conf
import requests
import json


class TokenDriver(object):

    def __init__(self):
        self.url = conf.TEAM_MSG
        self.url_project = conf.PEOJECT_MSG

    def gain_team_name(self, dict_data):
        headers = {'token': dict_data.get('token')}
        team_name = ''
        project_name = ''

        try:
            ret = requests.get(self.url, headers=headers, timeout=5)
            ret = json.loads(ret.text)

            ret_project = requests.get(self.url_project, headers=headers, timeout=5)
            ret_project = json.loads(ret_project.text)
        except Exception, e:
            log.error('gain the project message error, reason: %s' % e)
            return False
        log.info('get the project and team message is: %s,------%s' % (ret_project, ret))
        if ret.get('status') == 0 and ret_project.get('status') == 0:
            for i in ret.get('result').get('team_list'):
                if i.get('team_uuid') == dict_data.get('team_uuid'):
                    team_name = i.get('team_name')

            for j in ret_project.get('result').get('project_list'):
                if j.get('project_uuid') == dict_data.get('project_uuid'):
                    project_name = j.get('project_name')

            return team_name, project_name
        else:
            return False, False
