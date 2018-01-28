# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/24 下午4:16

from common.logs import logging as log
from status_driver import K8sDriver
import json


class EventsDriver(object):
    def __init__(self):
        self.k8s_driver = K8sDriver()

    def app_events_es(self, project_uuid, rc_name):
        event = []
        try:

            ns_events_info = self.k8s_driver.app_events_info(project_uuid)
            if ns_events_info.get('status') != 0:
                log.debug('Get events from k8s error')
            events_info = json.loads(ns_events_info['result'])
            events_list = events_info['items']
        except Exception, e:
            log.error('get the events error, reason is: %s' % e)
            raise Exception('get the events error')

        for i in events_list:
            if i.get('involvedObject').get('kind') == 'ReplicationController' and i.get('involvedObject').get('name') == rc_name:
                log.info('will post to es is: %s' % i.get('message'))
                event.append(i.get('message'))

            if i.get('involvedObject').get('kind') == 'Pod' and (rc_name in i.get('involvedObject').get('name')[:-6]):
                log.info('will post to es is: %s' % i.get('message'))
                event.append(i.get('message'))

        return event
