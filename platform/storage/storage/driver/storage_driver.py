#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os
import json
import requests

from conf import conf
from common.logs import logging as log
from common.code import request_result

from storage.ceph.ceph.rpcapi.ceph_rpcapi import CephRpcApi


requests.adapters.DEFAULT_RETRIES = 5


class StorageDriver(object):

    def __init__(self):

        self.ceph_api = CephRpcApi()
        self.ucenter_api = conf.ucenter_api
        self.billing_api = conf.billing_api

    def host_info(self, token, host_ip, password):

        context = {"token": token}

        parameters = {
                         "host_ip": host_ip,
                         "password": password
                     }

        return self.ceph_api.host_info(context, parameters)

    def cephmon_init(self, token, cluster_info,
                     mon01_hostip, mon01_rootpwd, mon01_snic,
                     mon02_hostip, mon02_rootpwd, mon02_snic):

        context = {"token": token}

        parameters = {
                         "cluster_info": cluster_info,
                         "mon01_hostip": mon01_hostip,
                         "mon01_rootpwd": mon01_rootpwd,
                         "mon01_snic": mon01_snic,
                         "mon02_hostip": mon02_hostip,
                         "mon02_rootpwd": mon02_rootpwd,
                         "mon02_snic": mon02_snic
                     }

        return self.ceph_api.cephmon_init(context, parameters)

    def cephmon_add(self, token, cluster_info, mon_id,
                    host_ip, rootpwd, storage_nic, mon_list):

        context = {"token": token}

        parameters = {
                         "cluster_info": cluster_info,
                         "mon_id": mon_id,
                         "host_ip": host_ip,
                         "rootpwd": rootpwd,
                         "storage_nic": storage_nic,
                         "mon_list": mon_list
                     }

        return self.ceph_api.cephmon_add(context, parameters)

    def cephcluster_mount(self, token, cluster_uuid,
                          cluster_info, mon_list,
                          host_ip, rootpwd, host_type):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "cluster_info": cluster_info,
                         "mon_list": mon_list,
                         "host_ip": host_ip,
                         "rootpwd": rootpwd,
                         "host_type": host_type
                     }

        return self.ceph_api.cephcluster_mount(context, parameters)

    def cephosd_add(self, token, cluster_uuid, cluster_info,
                    mon_list, host_ip, rootpwd, storage_nic,
                    jour_disk, data_disk, disk_type, weight):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "cluster_info": cluster_info,
                         "mon_list": mon_list,
                         "host_ip": host_ip,
                         "rootpwd": rootpwd,
                         "storage_nic": storage_nic,
                         "jour_disk": jour_disk,
                         "data_disk": data_disk,
                         "disk_type": disk_type,
                         "weight": weight
                     }

        return self.ceph_api.cephosd_add(context, parameters)

    def cephosd_delete(self, token, cluster_uuid,
                       osd_id, host_ip, rootpwd):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "osd_id": osd_id,
                         "host_ip": host_ip,
                         "rootpwd": rootpwd
                     }

        return self.ceph_api.cephosd_delete(context, parameters)

    def cephosd_reweight(self, token, cluster_uuid,
                         osd_id, weight):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "osd_id": osd_id,
                         "weight": weight
                     }

        return self.ceph_api.cephosd_reweight(context, parameters)

    def cephpool_create(self, token, cluster_uuid, pool_type, pool_name):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "pool_type": pool_type,
                         "pool_name": pool_name
                     }

        return self.ceph_api.cephpool_create(context, parameters)

    def cephpool_info(self, token, cluster_uuid):

        context = {"token": token, "queue": cluster_uuid}

        return self.ceph_api.cephpool_info(context)

    def disk_create(self, token, cluster_uuid,
                    pool_name, disk_name, disk_size):

        context = {"token": token, "queue": cluster_uuid}

        disk_size = int(disk_size) * 1024
        parameters = {
                         "pool_name": pool_name,
                         "disk_name": disk_name,
                         "disk_size": disk_size
                     }

        return self.ceph_api.rbd_create(context, parameters)

    def disk_delete(self, token, cluster_uuid,
                    pool_name, disk_name):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "pool_name": pool_name,
                         "disk_name": disk_name
                     }

        return self.ceph_api.rbd_delete(context, parameters)

    def disk_resize(self, token, cluster_uuid,
                    pool_name, disk_name, disk_size):

        context = {"token": token, "queue": cluster_uuid}

        disk_size = int(disk_size) * 1024
        parameters = {
                         "pool_name": pool_name,
                         "disk_name": disk_name,
                         "disk_size": disk_size
                     }

        return self.ceph_api.rbd_resize(context, parameters)

    def disk_growfs(self, token, cluster_uuid,
                    image_name, fs_type):

        context = {"token": token, "queue": cluster_uuid}

        parameters = {
                         "image_name": image_name,
                         "fs_type": fs_type
                     }

        return self.ceph_api.rbd_growfs(context, parameters)

    def billing_create(self, token, volume_uuid,
                       volume_name, volume_conf):

        try:
            url = '%s/api/v1.0/billing/resources' % (self.billing_api)
            headers = {'token': token}
            body = {
                       "resource_uuid": volume_uuid,
                       "resource_name": volume_name,
                       "resource_type": "volume",
                       "resource_conf": volume_conf,
                       "resource_status": "using"
                   }

            status = requests.post(url, headers=headers,
                                   data=json.dumps(body),
                                   timeout=5).json()['status']
            if int(status) != 0:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Billing resource create error: reason=%s' % (e))
            return request_result(601)

        return request_result(0)

    def billing_delete(self, token, volume_uuid):

        try:
            url = '%s/api/v1.0/billing/resources/%s' \
                  % (self.billing_api, volume_uuid)
            headers = {'token': token}

            status = requests.delete(url, headers=headers,
                                     timeout=5).json()['status']
            if int(status) != 0:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Billing info delete error: reason=%s' % (e))
            return request_result(601)

        return request_result(0)

    def billing_update(self, token, volume_uuid,
                       volume_conf=None, team_uuid=None,
                       project_uuid=None, user_uuid=None):

        try:
            url = '%s/api/v1.0/billing/resources/%s' \
                  % (self.billing_api, volume_uuid)
            headers = {'token': token}
            body = {
                       "resource_conf": volume_conf,
                       "resource_status": "using",
                       "team_uuid": team_uuid,
                       "project_uuid": project_uuid,
                       "user_uuid": user_uuid
                   }

            status = requests.put(url, headers=headers,
                                  data=json.dumps(body),
                                  timeout=5).json()['status']
            if int(status) != 0:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Billing info update error: reason=%s' % (e))
            return request_result(601)

        return request_result(0)

    def team_balance(self, token):

        try:
            url = '%s/api/v1.0/billing/balances' \
                  % (self.billing_api)
            headers = {'token': token}

            return requests.get(url, headers=headers,
                                timeout=5).json()
        except Exception, e:
            log.error('Billing get balance error: reason=%s' % (e))
            return request_result(601)

    def service_token(self):

        try:
            url = '%s/api/v1.0/ucenter/tokens' % (self.ucenter_api)
            body = {
                       "user_name": "service",
                       "password": "service@2017"
                   }

            return requests.post(url, data=json.dumps(body),
                                 timeout=5).json()
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

    def resources_check(self, add_list=[],
                        delete_list=[], update_list=[]):

        try:
            ret = self.service_token()
            if int(ret.get('status')) == 0:
                token = ret['result']['user_token']
            else:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

        try:
            url = '%s/api/v1.0/billing/resources' \
                  % (self.billing_api)
            headers = {'token': token}
            body = {
                       "add_list": add_list,
                       "delete_list": delete_list,
                       "update_list": update_list
                   }

            status = requests.put(url, headers=headers,
                                  data=json.dumps(body),
                                  timeout=15).json()['status']
            if int(status) != 0:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Billing resources check error: reason=%s' % (e))
            return request_result(601)

        return request_result(0)

    def balances_check(self):

        try:
            ret = self.service_token()
            if int(ret.get('status')) == 0:
                token = ret['result']['user_token']
            else:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

        try:
            url = '%s/api/v1.0/billing/balances?balance_check=true' \
                  % (self.billing_api)
            headers = {'token': token}
            log.debug('balances_check_url=%s, headers=%s' % (url, headers))

            return requests.get(url, headers=headers,
                                timeout=10).json()
        except Exception, e:
            log.error('Billing balances check error: reason=%s' % (e))
            return request_result(601)
