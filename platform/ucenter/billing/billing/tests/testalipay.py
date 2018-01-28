#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from billing.driver import billing_driver


def test_alipay_precreate(recharge_uuid, amount):

    alipay_driver = billing_driver.BillingDriver()

    return alipay_driver.ali_precreate(
                         recharge_uuid, amount)


def test_alipay_query(recharge_uuid):

    alipay_driver = billing_driver.BillingDriver()

    return alipay_driver.ali_pay_check(recharge_uuid)


def test_alipay_cancel(recharge_uuid):

    alipay_driver = billing_driver.BillingDriver()

    return alipay_driver.ali_pay_cancel(recharge_uuid)


if __name__ == '__main__':

    parameter = sys.argv[1]

    recharge_uuid = '20160320010101001'
    amount = 10

    if parameter == 'precreate':

        print test_alipay_precreate(recharge_uuid, amount)

    elif parameter == 'check':

        print test_alipay_query(recharge_uuid)

    elif parameter == 'cancel':

        print test_alipay_cancel(recharge_uuid)
