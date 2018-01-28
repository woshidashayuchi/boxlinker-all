# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/28 下午3:26

from common.logs import logging as log
from common.code import request_result
from driver.roll_driver import RollDriver
from rolling_client import RollingUpdate


class RollManager(object):
    def __init__(self):
        self.roll_driver = RollDriver()
        self.roll_p = RollingUpdate()

    def roll_manager(self, context):
        inner_to_roll = []
        inner_data = context.get('events')
        for dict_data in inner_data:
            log.info('explain the manager data, dict_date is: %s' % dict_data)
            try:
                action = dict_data.get('action')
            except Exception, e:
                log.error('event parameters error, parameters=%s, reason=%s' % (action, e))
                return request_result(101)

            if 'push' == action:
                target_media = dict_data.get('target').get('mediaType')
                if target_media == 'application/vnd.docker.distribution.manifest.v2+json':
                    ret = self.roll_driver.roll_up(dict_data)
                    log.info('rrrrrrrrrrrr==%s' % ret)

                    try:
                        to_roll_box = self.roll_driver.roll_boxlinker(dict_data)
                        log.info('boxlinker update json is: %s' % to_roll_box)
                        if len(to_roll_box.get('replicationcontrollers')) == 0 and ret.get('status') is None:
                            return ret
                        else:
                            self.roll_p.rolling_update(to_roll_box)
                    except Exception, e:
                        log.error('rolling update the boxlinker error, reason is: %s' % e)
                        return request_result(506)
                    if ret.get('status') != 0 or ret.get('status') is None:
                        return ret
                    else:
                        log.info('give rolling update data is: %s' % ret)
                        try:
                            for i in ret.get('result').get('replicationcontrollers'):
                                inner_to_roll.append({'namespace': i.get('namespace'),
                                                      'rc_name': i.get('rc_name').replace('_', '-')})

                            to_roll = {'image': ret.get('result').get('image'),
                                       'replicationcontrollers': inner_to_roll}
                            self.roll_p.rolling_update(to_roll)
                        except Exception, e:
                            log.error('rolling update to end error, reason is: %s' % e)
                            return request_result(506)

        return request_result(0)
