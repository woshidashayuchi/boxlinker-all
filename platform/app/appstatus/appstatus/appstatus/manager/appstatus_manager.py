# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json
import time

from time import sleep

from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from appstatus.db import service_db
from appstatus.driver import status_driver
from appstatus.driver.events_driver import EventsDriver
from appstatus.driver.es_driver.to_es import post_es
from time import sleep


class AppStatusManager(object):

    def __init__(self):

        self.service_db = service_db.ServiceDB()
        self.k8s_driver = status_driver.K8sDriver()
        self.events = EventsDriver()

    def p_es(self, project_uuid, rc_name, msg):
        try:
            ret = self.service_db.get_user_uuid(project_uuid, rc_name)

            if len(ret) == 0 or len(ret[0]) == 0:
                return 'not_need'
            else:
                user_uuid = ret[0][0]
                message_es = {'user_uuid': user_uuid, 'project_uuid': project_uuid, 'service_name': rc_name}

                if msg != 'old service is stopped forced' and msg != 'waiting...':
                    events_message = self.events.app_events_es(project_uuid, rc_name)
                    if len(events_message) != 0:
                        events_message = list(set(events_message))
                    for i in events_message:
                        if 'pulled' in i:
                            post_es(message_es, i)

                sleep(1)
                post_es(message_es, msg)
        except Exception, e:
            log.error('get the user_uuid error, reason is: %s' % e)

    def rc_status_update(self, rc_status_cache):

        rc_status_info = self.k8s_driver.rc_status_info()
        status = rc_status_info['status']
        if status != 0:
            log.debug('Get pods status from k8s error')
            return rc_status_cache

        try:
            rc_status_info = json.loads(rc_status_info['result'])
            log.debug('rc_status_list_type=%s' % (type(rc_status_info)))
            rc_status_list = rc_status_info['items']
        except Exception, e:
            log.error('Get rc status list error, reason=%s' % (e))
            return rc_status_cache
        rc_status_new = {}

        for rc_info in rc_status_list:
            try:
                rc_name = rc_info['metadata']['labels'].get('component')
                project_uuid = rc_info.get('metadata').get('namespace')

                # rc_name_info = rc_info['metadata']['annotations'][
                #                       'kubernetes.io/created-by'
                #                       ]
                # rc_name = json.loads(rc_name_info)['reference']['name']
                rc_name = rc_name + '#' + project_uuid
                pod_name = rc_info['metadata']['name']
                pod_status_info = rc_info['status'][
                                  'containerStatuses'][0]['state']
                log.debug('rc_name=%s, project_uuid=%s, '
                          'pod_name=%s, pod_status_info=%s'
                          % (rc_name, project_uuid, pod_name,
                             pod_status_info))
            except Exception, e:
                log.warning('Get rc info error, reason=%s' % e)
                continue

            for k, v in pod_status_info.items():
                if k == 'waiting':
                    pod_status = v['reason']
                else:
                    pod_status = k

            # log.debug('rc_name=%s, pod_name=%s, status_result=%s'
            #           % (rc_name, pod_name, pod_status))

            if rc_name not in rc_status_new.keys():
                log.debug('Cached %s' % (rc_name))
                rc_status_new[rc_name] = {
                                             "pods_info": [
                                                 {
                                                     pod_name: pod_status
                                                 }
                                             ]
                                         }
            else:
                rc_status_new[rc_name]['pods_info'].append(
                    {pod_name: pod_status})

        rc_off_list = dict.fromkeys(
                      [x for x in rc_status_cache if x not in rc_status_new]
                      ).keys()
        for rc_off_name in rc_off_list:
            # self.k8s_driver.rc_status_update(rc_off_name, 'Stopping')
            self.service_db.update_status_anytime(
                 rc_off_name, 'Stopping')
            del rc_status_cache[rc_off_name]
            log.info('Update rc(%s) status off' % (rc_off_name))

            rc_name1 = rc_off_name.split('#')[0]
            project_uuid = rc_off_name.split('#')[1]
            self.p_es(project_uuid, rc_name1, 'old service is stopped forced')

        for rc_name, rc_info in rc_status_new.items():
            pods_info = rc_info['pods_info']
            for pod_info in pods_info:
                # log.debug('pod_info=%s, type=%s'
                #           % (pod_info, type(pod_info)))
                pod_status = pod_info.values()[0]
                if pod_status == 'running':
                    break
                else:
                    continue

            if (rc_name in rc_status_cache.keys()) \
                    and (pod_status == rc_status_cache[rc_name]):
                continue
            else:
                rc_status_cache[rc_name] = pod_status
                log.info('Update rc(%s) status(%s)' % (rc_name, pod_status))
                # self.k8s_driver.rc_status_update(rc_name, pod_status)
                self.service_db.update_status_anytime(
                     rc_name, pod_status)

                try:
                    rc_name1 = rc_name.split('#')[0]
                    project_uuid = rc_name.split('#')[1]
                    if pod_status.lower() == 'running':
                        self.p_es(project_uuid, rc_name1, 'service create successfully')
                    elif pod_status.lower() == 'containercreating' or pod_status.lower() == 'pending':
                        self.p_es(project_uuid, rc_name1, 'waiting...')
                    if 'err' in pod_status.lower() or 'error' in pod_status.lower():
                        self.p_es(project_uuid, rc_name1, 'service create failed')
                except Exception, e:
                    log.error('post to es error, reason is: %s' % e)

        return rc_status_cache

