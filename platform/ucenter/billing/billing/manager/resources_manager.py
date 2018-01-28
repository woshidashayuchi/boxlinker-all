# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from billing.db.billing_db import BillingDB


class ResourcesManager(object):

    def __init__(self):

        self.billing_db = BillingDB()

    def resource_create(self, resource_uuid, resource_name,
                        resource_type, resource_conf,
                        resource_status, user_uuid,
                        team_uuid, project_uuid):

        try:
            self.billing_db.resource_insert(
                            resource_uuid, resource_name,
                            resource_type, resource_conf,
                            resource_status, user_uuid,
                            team_uuid, project_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "resource_uuid": resource_uuid,
                     "resource_name": resource_name,
                     "resource_type": resource_type,
                     "resource_conf": resource_conf,
                     "resource_status": resource_status,
                     "user_uuid": user_uuid,
                     "team_uuid": team_uuid,
                     "project_uuid": project_uuid
                 }

        return request_result(0, result)

    def resource_delete(self, resource_uuid):

        try:
            self.billing_db.resource_delete(resource_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        return request_result(0)

    def resource_update(self, resource_uuid, resource_conf,
                        resource_status, user_uuid, team_uuid,
                        project_uuid):

        try:
            self.billing_db.resource_update(
                            resource_uuid, resource_conf,
                            resource_status, user_uuid,
                            team_uuid, project_uuid)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "resource_uuid": resource_uuid
                 }

        if resource_conf is not None:
            result['resource_conf'] = resource_conf
        if resource_status is not None:
            result['resource_status'] = resource_status
        if team_uuid is not None:
            result['team_uuid'] = team_uuid
        if project_uuid is not None:
            result['project_uuid'] = project_uuid
        if user_uuid is not None:
            result['user_uuid'] = user_uuid

        return request_result(0, result)

    def resource_list(self, team_uuid, page_size, page_num):

        try:
            resources_list_info = self.billing_db.resource_list(
                                       team_uuid, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        bill_resources_list = resources_list_info.get('resource_list')
        count = resources_list_info.get('count')

        resources_list = []
        for resources_info in bill_resources_list:
            resource_uuid = resources_info[0]
            resource_type = resources_info[1]
            team_uuid = resources_info[2]
            project_uuid = resources_info[3]
            user_uuid = resources_info[4]
            create_time = resources_info[5]
            update_time = resources_info[6]
            resource_name = resources_info[7]
            resource_conf = resources_info[8]
            resource_status = resources_info[9]

            v_resources_info = {
                                   "resource_uuid": resource_uuid,
                                   "resource_type": resource_type,
                                   "team_uuid": team_uuid,
                                   "project_uuid": project_uuid,
                                   "user_uuid": user_uuid,
                                   "resource_name": resource_name,
                                   "resource_conf": resource_conf,
                                   "resource_status": resource_status,
                                   "create_time": create_time,
                                   "update_time": update_time
                               }

            v_resources_info = json.dumps(v_resources_info, cls=CJsonEncoder)
            v_resources_info = json.loads(v_resources_info)
            resources_list.append(v_resources_info)

        result = {"count": count}
        result['resources_list'] = resources_list

        return request_result(0, result)

    def resource_check(self, add_list, delete_list, update_list):

        # 获取计费系统中24小时内新增资源列表
        # 获取计费系统中24小时内删除资源列表
        # 获取计费系统中24小时内更新资源列表

        if len(add_list) != 0:
            try:
                resources_add_info = self.billing_db.resources_add_list()
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))

            resources_list = []
            for resources_info in resources_add_info:
                resource_uuid = resources_info[0]
                resources_list.append(resource_uuid)

            try:
                for resources_add in add_list:
                    resource_uuid = resources_add['resource_uuid']
                    if resource_uuid not in resources_list:
                        # 获取新建资源信息并创建资源
                        resource_name = resources_add['resource_name']
                        resource_type = resources_add['resource_type']
                        resource_conf = resources_add['resource_conf']
                        resource_status = resources_add['resource_status']
                        user_uuid = resources_add['user_uuid']
                        team_uuid = resources_add['team_uuid']
                        project_uuid = resources_add['project_uuid']
                        self.resource_create(resource_uuid, resource_name,
                                             resource_type, resource_conf,
                                             resource_status, user_uuid,
                                             team_uuid, project_uuid)
            except Exception, e:
                log.error('resource add check error, resources_list=%s, '
                          'add_list=%s, reason=%s'
                          % (resources_list, add_list, e))
                return request_result(101)

        if len(delete_list) != 0:
            try:
                resources_delete_info = self.billing_db.resources_delete_list()
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))

            resources_list = []
            for resources_info in resources_delete_info:
                resource_uuid = resources_info[0]
                resources_list.append(resource_uuid)

            try:
                for resources_delete in delete_list:
                    resource_uuid = resources_delete['resource_uuid']
                    if resource_uuid not in resources_list:
                        self.resource_delete(resource_uuid)
            except Exception, e:
                log.error('resource delete check error, resources_list=%s, '
                          'delete_list=%s, reason=%s'
                          % (resources_list, delete_list, e))
                return request_result(101)

        if len(update_list) != 0:
            try:
                resources_update_info = self.billing_db.resources_update_list()
            except Exception, e:
                log.error('Database select error, reason=%s' % (e))

            resources_list = []
            resources_list_info = {}
            for resources_info in resources_update_info:
                resource_uuid = resources_info[0]
                resource_name = resources_info[1]
                resource_conf = resources_info[2]
                resource_status = resources_info[3]
                team_uuid = resources_info[4]
                project_uuid = resources_info[5]
                user_uuid = resources_info[6]

                resources_list.append(resource_uuid)
                resource_info = {
                                    "resource_name": resource_name,
                                    "resource_conf": resource_conf,
                                    "resource_status": resource_status,
                                    "team_uuid": team_uuid,
                                    "project_uuid": project_uuid,
                                    "user_uuid": user_uuid
                                }

                resources_list_info[resource_uuid] = resource_info

            try:
                for resources_update in update_list:
                    resource_uuid = resources_update['resource_uuid']
                    if resource_uuid not in resources_list:
                        resource_name = resources_update['resource_name']
                        resource_conf = resources_update['resource_conf']
                        resource_status = resources_update['resource_status']
                        user_uuid = resources_update['user_uuid']
                        team_uuid = resources_update['team_uuid']
                        project_uuid = resources_update['project_uuid']
                        self.resource_update(resource_uuid, resource_conf,
                                             resource_status, user_uuid,
                                             team_uuid, project_uuid)
                    else:
                        # 取出ucenter中存储的资源数据，逐项对比，不一致就执行更新
                        # 查询更新记录时一次性将数据取出，然后整理放入一个字典中，
                        # 字典的键为各资源id，字典的值为各资源配置。
                        u_resource_info = resources_list_info[resource_uuid]
                        u_resource_name = u_resource_info['resource_name']
                        u_resource_conf = u_resource_info['resource_conf']
                        u_resource_status = u_resource_info['resource_status']
                        u_team_uuid = u_resource_info['team_uuid']
                        u_project_uuid = u_resource_info['project_uuid']
                        u_user_uuid = u_resource_info['user_uuid']

                        resource_name = resources_update['resource_name']
                        resource_conf = resources_update['resource_conf']
                        resource_status = resources_update['resource_status']
                        user_uuid = resources_update['user_uuid']
                        team_uuid = resources_update['team_uuid']
                        project_uuid = resources_update['project_uuid']

                        if (u_resource_name != resource_name) \
                           or (u_resource_conf != resource_conf) \
                           or (u_resource_status != resource_status) \
                           or (u_team_uuid != team_uuid) \
                           or (u_project_uuid != project_uuid) \
                           or (u_user_uuid != user_uuid):

                            self.resource_update(resource_uuid, resource_conf,
                                                 resource_status, user_uuid,
                                                 team_uuid, project_uuid)
            except Exception, e:
                log.error('resource update check error, resources_list=%s, '
                          'update_list=%s, reason=%s'
                          % (resources_list, update_list, e))
                return request_result(101)

        return request_result(0)
