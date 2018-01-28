# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.parameters import rpc_data
from common.rabbitmq_client import RabbitmqClient


class StorageRpcApi(object):

    def __init__(self):

        self.rbtmq = RabbitmqClient()
        self.queue = conf.storage_call_queue
        self.timeout = 60

    def cephcluster_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_cls_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephcluster_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_cls_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephcluster_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_cls_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephcluster_mount(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_cls_mnt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def host_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_hst_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def host_delete(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_hst_del", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def host_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_hst_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def host_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_hst_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephmon_init(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_mon_int", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephmon_add(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_mon_add", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephmon_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_mon_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephmon_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_mon_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephosd_add(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_osd_add", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephosd_delete(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_osd_del", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephosd_reweight(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_osd_rwt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephosd_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_osd_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephosd_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_osd_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephpool_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_pol_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephpool_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_pol_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def cephpool_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_pol_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_create(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_crt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_info(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_inf", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_update(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_udt", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_delete(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_dsk_del", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_reclaim_list(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_rcm_lst", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)

    def disk_reclaim_recovery(self, context, parameters=None):

        try:
            rpc_body = rpc_data("stg_ceh_rcm_rcv", context, parameters)
            return self.rbtmq.rpc_call_client(
                        self.queue, self.timeout, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % (e))
            return request_result(598)
