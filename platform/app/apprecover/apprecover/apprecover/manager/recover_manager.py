# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/31 下午6:10

from common.logs import logging as log
from common.code import request_result, request_result_for_query
from common.limit import limit_check
from db.service_db import ServiceDB
from driver.recover_driver import RecoverDriver
from driver.billing_driver import BillingDriver
import requests


class RecoverManager(object):
    def __init__(self):
        self.recover_driver = RecoverDriver()
        self.service_db = ServiceDB()
        self.billing_driver = BillingDriver()

    def recover_manager(self):
        try:
            self.recover_driver.update_services()
        except Exception, e:
            log.error('recover error, reason is: %s' % e)

    def service_list(self, parameters):

        try:
            count = self.recover_driver.get_recycle_svc_count(parameters)
            ret = self.recover_driver.get_recycle_services(parameters)
            return request_result_for_query(0, count, ret)
        except Exception, e:
            log.error('get the recover services error, reason is: %s' % e)
            raise Exception(e)

    def elements_explain(self, context):
        log.info('apps data is: %s' % context)
        metal = []
        kuber = []
        try:
            db_data = self.service_db.service_regain(context)
            log.info(db_data)
        except Exception, e:
            log.error('get the service data from database error, reason is: %s' % e)
            raise Exception(e)
        try:
            if len(db_data) == 0 or len(db_data[0]) == 0:
                return request_result(0, 'ok')
            else:
                for i in db_data:
                    to_kube = {'service_name': i[1],
                               'description': i[0],
                               'service_uuid': i[2],
                               'pods_num': i[3],
                               'image_id': i[4],
                               'cm_format': i[5],
                               'container_cpu': i[6],
                               'container_memory': i[7],
                               'policy': i[8],
                               'auto_startup': i[9],
                               'command': i[10],
                               'container': [{'container_port': i[11], 'protocol': i[12], 'access_mode': i[13],
                                              'access_scope': i[14], 'tcp_port': i[15], 'private_domain': i[16],
                                              'identify': i[17]}],
                               'env': [{'env_key': i[18], 'env_value': i[19]}],
                               'volume': [{'volume_uuid': i[20], 'disk_path': i[21], 'readonly': i[22]}]
                               }

                    metal.append(to_kube)

                for x in metal:
                    if len(kuber) == 0:
                        kuber.append(x)
                    else:
                        for y in kuber:
                            if y.get('service_uuid') == x.get('service_uuid'):
                                kuber[kuber.index(y)]['env'] = y.get('env') + x.get('env')
                                kuber[kuber.index(y)]['volume'] = y.get('volume') + x.get('volume')
                            else:
                                kuber.append(x)

                for j in kuber:

                    for m in j.get('env'):
                        index_m = j.get('env').index(m)

                        if m.get('env_key') in ['null', 'NULL', 'None', ''] or m.get('env_key') is None:
                            del kuber[kuber.index(j)]['env'][index_m]

                        if len(j.get('env')) == 1 and (m.get('env_key') in ['null', 'NULL', 'None', ''] or m.get('env_key') is None):
                            kuber[kuber.index(j)]['env'] = ''

                    for n in j.get('volume'):
                        index_n = j.get('volume').index(n)

                        if n.get('volume_uuid') in ['null', 'NULL', 'None', ''] or n.get('volume_uuid') is None:
                            del kuber[kuber.index(j)]['volume'][index_n]

                        if len(j.get('volume')) == 1 and (n.get('volume_uuid') in ['null', 'NULL', 'None', ''] or n.get('volume_uuid')
                                                          is None):
                            kuber[kuber.index(j)]['volume'] = ''

                return kuber
        except Exception, e:
            log.error('explain the main data error, reason is: %s' % e)
            raise Exception('explain the main data error')

    def create_apps(self, token, con, context, cost):
        log.info('the inner recover data is: %s' % context)
        try:
            to_kuber = self.elements_explain(context)
        except Exception, e:
            log.error('use the elements_explain error, reason is: %s' % e)
            return request_result(404)
        try:
            costs = self.billing_driver.get_cost(token, context.get('service_uuid'))

        except Exception, e:
            log.error('get the billing cost error, reason is: %s' % e)
            return request_result(501)

        for i in to_kuber:
            i['token'] = token
            i['rtype'] = 'lifecycle'
            service_uuid = i.get('service_uuid')
            i['resource_uuid'] = service_uuid
            i.update(context)
            i['cost'] = costs

            log.info('iiiiiiiiiiii===%s' % i)
            try:

                self.recover_driver.create_service(con, i)
            except Exception, e:
                log.error('create services error, reason is: %s' % e)
                return request_result(501)

            try:
                db_ret = self.service_db.update_lifecycle(service_uuid)
                if db_ret is not None:
                    log.info('UPDATE THE DATABASE ERROR')
                    return request_result(403)
            except Exception, e:
                log.error('update the database error, reason is: %s' % e)
                return request_result(403)

        return request_result(0, {'resource_uuid': 'recovering...'})

    def physics_del(self, service_uuid):

        try:
            ret = self.recover_driver.delete_py(service_uuid)
        except Exception, e:
            log.error('delete the database error, reason is: %s' % e)
            return request_result(402)

        return ret

    def delete_in30_days(self):
        try:
            db_ret = self.service_db.delete_30days()
            if db_ret is not None:
                log.error('delete the db result is: %s' % db_ret)
                raise Exception('db result is not None')
        except Exception, e:
            log.error('delete the recover services in 30 days error, reason is: %s' % e)
            raise Exception('delete the recover services in 30 days error')
