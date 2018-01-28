# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import uuid
import json
import socket

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.limit import limit_check
from common.operation_record import operation_record

from storage.db import storage_db
from storage.driver import storage_driver


class CloudDiskManager(object):

    def __init__(self):

        self.billing_check = conf.billing
        self.storage_db = storage_db.StorageDB()
        self.storage_driver = storage_driver.StorageDriver()
        self.local_ip = socket.gethostbyname(socket.gethostname())

    @operation_record(resource_type='volume', action='create')
    @limit_check('volumes')
    def volume_create(self, team_uuid, project_uuid, user_uuid,
                      cluster_uuid, volume_name, volume_size,
                      volume_type, fs_type, cost,
                      token, source_ip, resource_name):

        try:
            disk_name_ch = self.storage_db.name_duplicate_check(
                                volume_name, project_uuid,
                                cluster_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if disk_name_ch != 0:
            log.warning('Volume name(%s) already exists' % (volume_name))
            return request_result(301)

        volume_uuid = str(uuid.uuid4())
        disk_name = volume_name + '-' + volume_uuid
        pool_name = 'pool_%s' % (volume_type)

        status_code = self.storage_driver.disk_create(
                           token, cluster_uuid, pool_name,
                           disk_name, volume_size)['status']
        if int(status_code) != 0:
            log.error('Create storage disk(%s) failure' % (volume_name))
            return request_result(status_code)

        try:
            self.storage_db.volume_create(
                         volume_uuid, cluster_uuid, pool_name,
                         volume_name, volume_size, volume_type,
                         disk_name, fs_type,
                         team_uuid, project_uuid, user_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        if self.billing_check is True:
            volume_conf = str(volume_size) + 'G'
            self.storage_driver.billing_create(
                 token, volume_uuid, volume_name, volume_conf)

        result = {
                     "volume_uuid": volume_uuid,
                     "cluster_uuid": cluster_uuid,
                     "volume_name": volume_name,
                     "pool_name": pool_name,
                     "image_name": disk_name,
                     "volume_size": volume_size,
                     "volume_type": volume_type,
                     "fs_type": fs_type,
                     "resource_uuid": volume_uuid
                 }

        return request_result(0, result)

    @operation_record(resource_type='volume', action='logical_delete')
    def volume_logical_delete(self, volume_uuid, token,
                              source_ip, resource_uuid):

        try:
            volume_name = self.storage_db.volume_name(
                               volume_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            self.storage_db.volume_logical_delete(volume_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        if self.billing_check is True:
            self.storage_driver.billing_delete(token, volume_uuid)

        result = {
                     "resource_name": volume_name
                 }

        return request_result(0, result)

    @operation_record(resource_type='volume', action='physical_delete')
    def volume_physical_delete(self, volume_uuid, token,
                               source_ip, resource_uuid):

        try:
            volume_info = self.storage_db.volume_info(volume_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        cluster_uuid = volume_info[0][0]
        pool_name = volume_info[0][1]
        volume_name = volume_info[0][2]
        volume_status = volume_info[0][5]
        disk_name = volume_info[0][6]

        if volume_status != 'delete':
            log.warning('Storage disk status not equal delete, '
                        'operation denied, volume_name=%s, '
                        'cluster_uuid=%s, pool_name=%s'
                        % (volume_name, cluster_uuid, pool_name))
            return request_result(202)

        status_code = self.storage_driver.disk_delete(
                           token, cluster_uuid, pool_name,
                           disk_name)['status']
        if int(status_code) != 0:
            log.error('Delete storage disk(%s) failure' % (disk_name))
            return request_result(status_code)

        try:
            self.storage_db.volume_physical_delete(volume_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        result = {
                     "resource_name": volume_name
                 }

        return request_result(0, result)

    def volume_resize(self, token, volume_uuid, volume_size):

        try:
            volume_info = self.storage_db.volume_info(volume_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        cluster_uuid = volume_info[0][0]
        pool_name = volume_info[0][1]
        volume_name = volume_info[0][2]
        disk_name = volume_info[0][6]
        fs_type = volume_info[0][7]

        status_code = self.storage_driver.disk_resize(
                           token, cluster_uuid, pool_name,
                           disk_name, volume_size)['status']
        if int(status_code) != 0:
            log.error('storage disk(%s) resize failure' % (disk_name))
            return request_result(status_code)

        self.storage_driver.disk_growfs(
             token, cluster_uuid, volume_name, fs_type)

        try:
            self.storage_db.volume_resize(volume_uuid, volume_size)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            volume_conf = str(volume_size) + 'G'
            self.storage_driver.billing_update(
                                token, volume_uuid,
                                volume_conf)

        result = {
                     "volume_uuid": volume_uuid,
                     "volume_name": volume_name,
                     "pool_name": pool_name,
                     "image_name": disk_name,
                     "volume_size": volume_size,
                     "resource_name": volume_name
                 }

        return request_result(0, result)

    def volume_status(self, volume_uuid, volume_status):

        try:
            volume_name = self.storage_db.volume_name(
                               volume_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            self.storage_db.volume_status(volume_uuid, volume_status)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "volume_uuid": volume_uuid,
                     "volume_status": volume_status,
                     "resource_name": volume_name
                 }

        return request_result(0, result)

    @operation_record(resource_type='volume', action='update')
    def volume_update(self, volume_uuid, update,
                      volume_size, volume_status,
                      token, source_ip, resource_uuid):

        if update == 'size':
            return self.volume_resize(
                        token, volume_uuid, volume_size)
        elif update == 'status':
            return self.volume_status(
                        volume_uuid, volume_status)

    def volume_info(self, volume_uuid):

        try:
            volume_info = self.storage_db.volume_info(volume_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        cluster_uuid = volume_info[0][0]
        pool_name = volume_info[0][1]
        volume_name = volume_info[0][2]
        volume_size = volume_info[0][3]
        volume_type = volume_info[0][4]
        volume_status = volume_info[0][5]
        image_name = volume_info[0][6]
        fs_type = volume_info[0][7]
        mount_point = volume_info[0][8]
        create_time = volume_info[0][9]
        update_time = volume_info[0][10]

        v_disk_info = {
                          "volume_uuid": volume_uuid,
                          "cluster_uuid": cluster_uuid,
                          "pool_name": pool_name,
                          "volume_name": volume_name,
                          "volume_size": volume_size,
                          "volume_type": volume_type,
                          "volume_status": volume_status,
                          "image_name": image_name,
                          "fs_type": fs_type,
                          "mount_point": mount_point,
                          "create_time": create_time,
                          "update_time": update_time
                      }

        volume_info = json.dumps(v_disk_info, cls=CJsonEncoder)

        result = json.loads(volume_info)

        return request_result(0, result)

    def volume_list(self, user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv, cluster_uuid,
                    page_size, page_num):

        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                volumes_list_info = self.storage_db.volume_list_project(
                                         team_uuid, project_uuid,
                                         cluster_uuid, page_size, page_num)
            else:
                volumes_list_info = self.storage_db.volume_list_user(
                                         team_uuid, project_uuid, user_uuid,
                                         cluster_uuid, page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_volumes_list = volumes_list_info.get('volumes_list')
        count = volumes_list_info.get('count')

        disk_list = []
        for volume_info in user_volumes_list:
            volume_uuid = volume_info[0]
            cluster_uuid = volume_info[1]
            pool_name = volume_info[2]
            volume_name = volume_info[3]
            volume_size = volume_info[4]
            volume_type = volume_info[5]
            volume_status = volume_info[6]
            image_name = volume_info[7]
            fs_type = volume_info[8]
            mount_point = volume_info[9]
            create_time = volume_info[10]
            update_time = volume_info[11]

            v_disk_info = {
                              "volume_uuid": volume_uuid,
                              "cluster_uuid": cluster_uuid,
                              "pool_name": pool_name,
                              "volume_name": volume_name,
                              "volume_size": volume_size,
                              "volume_type": volume_type,
                              "volume_status": volume_status,
                              "image_name": image_name,
                              "fs_type": fs_type,
                              "mount_point": mount_point,
                              "create_time": create_time,
                              "update_time": update_time
                          }

            v_disk_info = json.dumps(v_disk_info, cls=CJsonEncoder)
            v_disk_info = json.loads(v_disk_info)
            disk_list.append(v_disk_info)

        result = {"volume_list": disk_list}
        result['count'] = count

        return request_result(0, result)

    def volume_reclaim_check(self):

        balances_check = self.storage_driver.balances_check()
        if balances_check.get('status') != 0:
            log.error('Billing balances check error, '
                      'balances_check=%s' % (balances_check))
            return
        else:
            teams_list = balances_check.get('result').get('teams_list')

        for team_info in teams_list:
            try:
                team_uuid = team_info['team_uuid']
                balance = team_info['balance']
                if float(balance) <= 0:
                    # 获取该team下的所有存储资源列表，然后进行逻辑删除
                    volumes_list_info = self.storage_db.volume_list_team(
                                             team_uuid)
                    for volume_info in volumes_list_info:
                        volume_uuid = volume_info[0]
                        self.storage_db.volume_logical_delete(volume_uuid)
            except Exception, e:
                log.error('volume reclaim exec error, reason=%s' % (e))

    def volume_reclaim_list(self, user_uuid, team_uuid,
                            team_priv, project_uuid, project_priv,
                            page_size, page_num):

        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                volumes_list_info = self.storage_db.volume_reclaim_list_project(
                                         team_uuid, project_uuid,
                                         page_size, page_num)
            else:
                volumes_list_info = self.storage_db.volume_reclaim_list_user(
                                         team_uuid, project_uuid, user_uuid,
                                         page_size, page_num)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        user_volumes_list = volumes_list_info.get('volumes_list')
        count = volumes_list_info.get('count')

        disk_list = []
        for volume_info in user_volumes_list:
            volume_uuid = volume_info[0]
            cluster_uuid = volume_info[1]
            pool_name = volume_info[2]
            volume_name = volume_info[3]
            volume_size = volume_info[4]
            volume_type = volume_info[5]
            volume_status = volume_info[6]
            image_name = volume_info[7]
            fs_type = volume_info[8]
            mount_point = volume_info[9]
            create_time = volume_info[10]
            update_time = volume_info[11]
            cluster_name = volume_info[12]

            v_disk_info = {
                              "volume_uuid": volume_uuid,
                              "cluster_uuid": cluster_uuid,
                              "cluster_name": cluster_name,
                              "pool_name": pool_name,
                              "volume_name": volume_name,
                              "volume_size": volume_size,
                              "volume_type": volume_type,
                              "volume_status": volume_status,
                              "image_name": image_name,
                              "fs_type": fs_type,
                              "mount_point": mount_point,
                              "create_time": create_time,
                              "update_time": update_time
                          }

            v_disk_info = json.dumps(v_disk_info, cls=CJsonEncoder)
            v_disk_info = json.loads(v_disk_info)
            disk_list.append(v_disk_info)

        result = {"volume_list": disk_list}
        result['count'] = count

        return request_result(0, result)

    @operation_record(resource_type='volume', action='recovery')
    def volume_reclaim_recovery(self, volume_uuid, token,
                                source_ip, resource_uuid):

        if self.billing_check is True:
            # 获取并检查用户余额，只有当余额大于0时才允许执行恢复操作
            team_balance = self.storage_driver.team_balance(token)
            if team_balance.get('status') != 0:
                log.error('Get balance info error, '
                          'team_balance=%s' % (team_balance))
                return request_result(601)
            else:
                balance = team_balance.get('result').get('balance')
                if float(balance) <= 0:
                    return request_result(302)

        try:
            volume_name = self.storage_db.volume_name(
                               volume_uuid)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            self.storage_db.volume_recovery(volume_uuid)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            self.storage_driver.billing_update(
                                token, volume_uuid)

        result = {
                     "volume_uuid": volume_uuid,
                     "resource_name": volume_name
                 }

        return request_result(0, result)

    def volume_reclaim_delete(self):

        try:
            ret = self.storage_driver.service_token()
            if int(ret.get('status')) == 0:
                token = ret['result']['user_token']
            else:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

        try:
            volumes_list_info = self.storage_db.volume_list_dead()
            for volume_info in volumes_list_info:
                volume_uuid = volume_info[0]
                self.volume_physical_delete(
                     volume_uuid, token=token,
                     source_ip=self.local_ip,
                     resource_uuid=volume_uuid)
        except Exception, e:
            log.error('volume reclaim delete exec error, reason=%s' % (e))

    def volume_check(self):

        # 获取24小时内新增的存储卷

        try:
            volumes_add_info = self.storage_db.volume_add_list()
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        add_list = []
        for volume_info in volumes_add_info:
            volume_uuid = volume_info[0]
            volume_name = volume_info[1]
            volume_size = volume_info[2]
            volume_status = volume_info[3]
            resource_type = volume_info[4]
            team_uuid = volume_info[5]
            project_uuid = volume_info[6]
            user_uuid = volume_info[7]

            volume_conf = str(volume_size) + 'G'

            v_disk_info = {
                              "resource_uuid": volume_uuid,
                              "resource_name": volume_name,
                              "resource_type": resource_type,
                              "resource_conf": volume_conf,
                              "resource_status": "using",
                              "team_uuid": team_uuid,
                              "project_uuid": project_uuid,
                              "user_uuid": user_uuid
                          }

            add_list.append(v_disk_info)

        # 获取24小时内删除的存储卷

        try:
            volumes_delete_info = self.storage_db.volume_delete_list()
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        delete_list = []
        for volume_info in volumes_delete_info:
            volume_uuid = volume_info[0]

            v_disk_info = {
                              "resource_uuid": volume_uuid
                          }

            delete_list.append(v_disk_info)

        # 获取24小时内更新的存储卷

        try:
            volumes_update_info = self.storage_db.volume_update_list()
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        update_list = []
        for volume_info in volumes_update_info:
            volume_uuid = volume_info[0]
            volume_name = volume_info[1]
            volume_size = volume_info[2]
            volume_status = volume_info[3]
            resource_type = volume_info[4]
            team_uuid = volume_info[5]
            project_uuid = volume_info[6]
            user_uuid = volume_info[7]

            volume_conf = str(volume_size) + 'G'

            v_disk_info = {
                              "resource_uuid": volume_uuid,
                              "resource_name": volume_name,
                              "resource_type": resource_type,
                              "resource_conf": volume_conf,
                              "resource_status": "using",
                              "team_uuid": team_uuid,
                              "project_uuid": project_uuid,
                              "user_uuid": user_uuid
                          }

            update_list.append(v_disk_info)

        self.storage_driver.resources_check(
             add_list, delete_list, update_list)
