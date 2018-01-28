# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/25 下午3:19

from common.logs import logging as log
from conf import conf
from db.service_db import ServiceDB
import requests
from common.code import request_result
import json


class BillingDriver(object):

    def __init__(self):
        self.billing = conf.billing_api
        self.service_db = ServiceDB()

    def get_cost(self, token, service_uuid):
            cost = 0
            billing_url = self.billing+'/api/v1.0/billing/costs'
            header = {'token': token}

            try:
                db_ret = self.service_db.get_cost_use(service_uuid)
                for i in db_ret:
                    pods_num = int(i[0])
                    cm = int(i[1][:-1])
                    cost_in = pods_num*cm
                    cost += cost_in
                cost = str(cost) + 'X'
            except Exception, e:
                log.error('get the service uses for cost error, reason is: %s' % e)
                raise Exception('get the service uses for cost error')

            to_billing = {'resource_type': 'app',
                          'resource_conf': cost,
                          'resource_status': 'on',
                          'hours': 1}

            try:
                bill_ret = requests.post(billing_url, headers=header, data=json.dumps(to_billing), timeout=5)
                log.info('get the cost message\'s result is: %s, type is: %s' % (bill_ret.text, type(bill_ret)))
                bill_ret = json.loads(bill_ret.text)
                if bill_ret.get('status') != 0:
                    raise Exception('from billing get cost, the result code is not 0')

                cost = bill_ret.get('result').get('resource_cost')
            except Exception, e:
                log.error('get the cost message error, reason is: %s' % e)
                raise Exception('get the cost message error')

            return cost
