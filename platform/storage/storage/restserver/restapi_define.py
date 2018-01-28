#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from flask import request
from flask_restful import Resource

from common.logs import logging as log
from common.code import request_result
from common.time_log import time_log
from common.parameters import context_data
from common.token_ucenterauth import token_auth

from storage.rpcapi import rpc_api as storage_rpcapi


class CephClustersApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.cephcluster_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephcluster_list(context)


class CephClusterApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self, cluster_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"cluster_uuid": cluster_uuid}

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephcluster_info(context, parameters)

    @time_log
    def put(self, cluster_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
            parameters['cluster_uuid'] = cluster_uuid
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "update", source_ip)

        return self.storage_api.cephcluster_mount(context, parameters)


class CephHostsApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.host_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.host_list(context, parameters)


class CephHostApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self, host_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"host_uuid": host_uuid}

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.host_info(context, parameters)

    @time_log
    def delete(self, host_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"host_uuid": host_uuid}

        context = context_data(token, "stg_stg_adm_com", "delete", source_ip)

        return self.storage_api.host_delete(context, parameters)


class CephMonsApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.cephmon_init(context, parameters)

    @time_log
    def put(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.cephmon_add(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            cluster_uuid = request.args.get('cluster_uuid')
            parameters = {"cluster_uuid": cluster_uuid}
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephmon_list(context, parameters)


class CephMonApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self, mon_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"mon_uuid": mon_uuid}

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephmon_info(context, parameters)


class CephOsdsApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.cephosd_add(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            cluster_uuid = request.args.get('cluster_uuid')
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "cluster_uuid": cluster_uuid,
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephosd_list(context, parameters)


class CephOsdApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def put(self, osd_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
            parameters['osd_uuid'] = osd_uuid
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "update", source_ip)

        return self.storage_api.cephosd_reweight(context, parameters)

    @time_log
    def get(self, osd_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"osd_uuid": osd_uuid}

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephosd_info(context, parameters)

    @time_log
    def delete(self, osd_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            cluster_uuid = request.args.get('cluster_uuid')
            rootpwd = request.args.get('rootpwd')
            parameters = {
                             "osd_uuid": osd_uuid,
                             "cluster_uuid": cluster_uuid,
                             "rootpwd": rootpwd
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "delete", source_ip)

        return self.storage_api.cephosd_delete(context, parameters)


class CephPoolsApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "create", source_ip)

        return self.storage_api.cephpool_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            cluster_uuid = request.args.get('cluster_uuid')
            parameters = {"cluster_uuid": cluster_uuid}
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephpool_list(context, parameters)


class CephPoolApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self, pool_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        parameters = {"pool_uuid": pool_uuid}

        context = context_data(token, "stg_stg_adm_com", "read")

        return self.storage_api.cephpool_info(context, parameters)


class VolumesApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "stg_ceh_dsk_add", "create", source_ip)

        return self.storage_api.disk_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            cluster_uuid = request.args.get('cluster_uuid')
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "cluster_uuid": cluster_uuid,
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_ceh_dsk_lst", "read")

        return self.storage_api.disk_list(context, parameters)


class VolumeApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self, volume_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, volume_uuid, "read")

        return self.storage_api.disk_info(context)

    @time_log
    def put(self, volume_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
            update = request.args.get('update')
            parameters['update'] = update
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, volume_uuid, "update", source_ip)

        return self.storage_api.disk_update(context, parameters)

    @time_log
    def delete(self, volume_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, volume_uuid, "delete", source_ip)

        return self.storage_api.disk_delete(context)


class VolumesReclaimsApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "stg_ceh_dsk_lst", "read")

        return self.storage_api.disk_reclaim_list(context, parameters)


class VolumeReclaimApi(Resource):

    def __init__(self):

        self.storage_api = storage_rpcapi.StorageRpcApi()

    @time_log
    def put(self, volume_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, volume_uuid, "create", source_ip)

        return self.storage_api.disk_reclaim_recovery(context)
