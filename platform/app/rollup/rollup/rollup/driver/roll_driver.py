# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/28 下午3:16

from common.logs import logging as log
from db.roll_db import ServiceDB
from common.code import request_result
from conf import conf
import requests
import json
import os
from time import sleep
import re


class RollDriver(object):
    def __init__(self):
        with open(os.environ.get('TOKEN_PATH'), 'r') as f:
            token = f.read()
        auth_info = 'Bearer %s' % token
        self.HEADERS = {'Authorization': auth_info}
        self.host_address = 'https://kubernetes.default.svc:443/api/v1'
        self.roll_db = ServiceDB()

    @staticmethod
    def image_msg(tag, repository):
        n = 0
        try:
            for i in range(5):
                image_ret = requests.get('http://%s/api/v1.0/imagerepo/image/tagids/?repo_name=%s&repo_tag=%s' % (conf.IMAGE_S,
                                                                                                                  repository,
                                                                                                                  tag))
                image_ret = json.loads(image_ret.text)
                log.info('image result is: %s' % image_ret)
                if image_ret.get('status') != 0:
                    if n == 3:
                        raise Exception('get the image id error')
                    else:
                        n += 1
                        sleep(0.2)
                        continue
                else:
                    image_id = image_ret.get('result')
                    return image_id

        except Exception, e:
            log.error('get the image if by image name error, reason is: %s' % e)
            raise Exception('get the image if by image name error')

    def compare_to_db(self, image_id, image_name):
        ret = []
        try:
            db_ret = self.roll_db.compare_image_id(image_name)
        except Exception, e:
            log.error('get the image message from db error, reason is: %s' % e)
            raise Exception('get the image message from db error')
        try:
            if len(db_ret) == 0 or len(db_ret[0]) == 0:
                return
            else:
                for i in db_ret:
                    service_name = i[0]
                    project_uuid = i[1]
                    up_result = self.roll_db.update_image_id(image_id, service_name, project_uuid)
                    if up_result is not None:
                        log.error('update the database result is not None, is: %s' % up_result)
                        return
                    ret.append({'rc_name': service_name, 'namespace': project_uuid})
                return ret
        except Exception, e:
            log.error('explain the parameters from db error, reason is: %s' % e)
            raise Exception('explain the parameters from db error')

    def roll_up(self, dict_data):
        tag = dict_data.get('target').get('tag')
        repository = dict_data.get('target').get('repository')
        try:
            image_id = self.image_msg(tag, repository)
            log.info('change steps!!!')

            compare_ret = self.compare_to_db(image_id, 'index.boxlinker.com/'+repository)
            if compare_ret is None:
                return {}
            response = {'image': 'index.boxlinker.com/'+repository+':'+tag,
                        'replicationcontrollers': compare_ret}

        except Exception, e:
            log.error('get the image_id or compare to database error, reason is: %s' % e)
            return request_result(506)
        return request_result(0, response)

    def roll_boxlinker(self, dict_data):
        img = ''
        tag = dict_data.get('target').get('tag')
        repository = dict_data.get('target').get('repository')

        url = self.host_address+'/namespaces/boxlinker/replicationcontrollers'
        rc_msg = []
        try:
            rc_s = requests.get(url, headers=self.HEADERS, verify=False).text

            log.info('get the rcs result type is: %s' % type(rc_s))
            rc_s = json.loads(rc_s)
        except Exception, e:
            log.error('get  the replication controllers error, reason is: %s' % e)
            raise Exception('get the kubernetes resources error')
        try:
            rc_list = rc_s.get('items')
            image_check = 'index.boxlinker.com/'+repository
            for i in rc_list:
                rc_krud = i.get('metadata').get('labels').get('rc-krud')
                image = i.get('spec').get('template').get('spec').get('containers')
                for x in image:
                    img = x.get('image')
                log.info('from the replications get the image name is: %s' % img)
                image = img.split(':')[0]
                if rc_krud is not None and rc_krud != '' and rc_krud != 'null':
                    log.info('image_check from image_server  is: %s' % image_check)
                    if image == image_check:
                        rc_msg.append({'rc_name': i.get('metadata').get('name'),
                                       'namespace': i.get('metadata').get('namespace'),
                                       })
            to_roll = {'image': image_check+':'+tag,
                       'replicationcontrollers': rc_msg}
        except Exception, e:
            log.error('explain the boxlinker image update error, reason is: %s' % e)
            raise Exception('explain the boxlinker image update error')

        return to_roll



