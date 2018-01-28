#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from billing.driver import billing_driver


def test_weixinpay_precreate(recharge_uuid, amount):

    weixinpay_driver = billing_driver.BillingDriver()

    return weixinpay_driver.weixin_pay_precreate(
                            recharge_uuid, amount)


def test_weixinpay_query(recharge_uuid):

    weixinpay_driver = billing_driver.BillingDriver()

    return weixinpay_driver.weixin_pay_check(
                            recharge_uuid)


def test_weixinpay_cancel(recharge_uuid):

    weixinpay_driver = billing_driver.BillingDriver()

    return weixinpay_driver.weixin_pay_cancel(
                            recharge_uuid)

def test_weixinpay_getkey():

    weixinpay_driver = billing_driver.BillingDriver()

    return weixinpay_driver.weixin_pay_get_sandbox_key()


if __name__ == '__main__':

    parameter = sys.argv[1]

    recharge_uuid = '20160320010101001'
    amount = 1

    if parameter == 'precreate':

        print test_weixinpay_precreate(recharge_uuid, amount)

    elif parameter == 'check':

        print test_weixinpay_query(recharge_uuid)

    elif parameter == 'cancel':

        print test_weixinpay_cancel(recharge_uuid)

    elif parameter == 'getkey':

        print test_weixinpay_getkey()
