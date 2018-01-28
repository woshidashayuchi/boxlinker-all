#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
p_path = sys.path[0] + '/../..'
sys.path.insert(1, p_path)

from time import sleep

from common.logs import logging as log
from billing.manager.costs_manager import CostsManager
from billing.manager.bills_manager import BillsManager


def billing_service():

    costs_manager = CostsManager()
    bills_manager = BillsManager()

    log.critical('Starting Billing Service')
    while True:
        sleep(3600)
        try:
            log.info('Start billing')
            costs_manager.billing_statistics()
            bills_manager.bills_merge()
            log.info('Finish billing')
        except Exception, e:
            log.error('Billing Service running error, reason=%s'
                      % (e))


if __name__ == "__main__":

    billing_service()
