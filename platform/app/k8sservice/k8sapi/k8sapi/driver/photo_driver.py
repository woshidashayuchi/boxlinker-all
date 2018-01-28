# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/7 下午1:54
import json
import requests
from conf import conf
from common.logs import logging as log


def photo_dir(dict_data):
    photo_url = 'http://%s/api/v1.0/pictures' % conf.IMAGE_S
    file_url = 'http://101.201.56.57:8765/api/v1.0/files/%s/ServiceAvatars/%s/boxlinker' % (dict_data.get('team_uuid'),
                                                                                          dict_data.get('service_uuid'))
    service_name = dict_data.get('service_name')
    token = dict_data.get('token')

    photo_data = {'name': service_name}
    header = {'token': token}

    try:
        photo_ret = requests.post(photo_url, json.dumps(photo_data), headers=header, timeout=5).text
        log.info('make the photo,url is: %s result is: %s, type is: %s' % (photo_url, photo_ret, type(photo_ret)))
        photo_ret = json.loads(photo_ret)
        if photo_ret.get('status') == 0:
            image_dir = photo_ret.get('result').get('image_url')
        else:
            raise Exception('make the photo error')
    except Exception, e:
        log.error('make the photo error, reason is: %s' % e)
        raise Exception('request the photo url error')

    try:
        to_avatars = {'file_url': image_dir}
        ret = requests.post(file_url, json.dumps(to_avatars), headers=header, timeout=5).text
        log.info('take the service Avatars result is: %s' % ret)
    except Exception, e:
        log.error('take the service Avatars error, reason is: %s' % e)
        raise Exception('take the service Avatars error')


def parameters_to_avatars(dict_data):
    to_avatars = {'queryparameter': []}
    team_uuid = dict_data.get('team_uuid')
    # 传入dict_data需要携带team_uuid与avatars_uuid的列表
    avatars_uuid = dict_data.get('avatars_uuid')
    if len(avatars_uuid) != 0:
        for i in avatars_uuid:
            middle_para = {'team_uuid': team_uuid, 'resource_type': 'ServiceAvatars', 'resource_uuid': i,
                           'resource_domain': 'boxlinker'}

            to_avatars['queryparameter'].append(middle_para)

    return to_avatars


def get_services_photos(dict_data):
    response = []
    header = {'token': dict_data.get('token')}
    avatars_url = 'http://101.201.56.57:8765/api/v1.0/files/team_uuid'
    try:
        to_avatars = parameters_to_avatars(dict_data)
    except Exception, e:
        log.error('struct the parameters to avatars error, reason is: %s' % e)
        raise Exception('struct the parameters to avatars error')

    try:
        ret = requests.post(avatars_url, json.dumps(to_avatars), headers=header, timeout=5)
        log.info('post the avatars ,url is: %s ,result is: %s, type is: %s' % (avatars_url, ret, type(ret)))
        ret = json.loads(ret.text)
        if ret.get('status') != 0:
            raise Exception('can not get the serviceAvatars')
        for i in ret.get('result'):
            response.append({'service_uuid': i.get('resource_uuid'), "image_dir": i.get('storage_url')})

        return response
    except Exception, e:
        log.error('get the serviceAvatars exception, reason is: %s' % e)
        raise Exception('get the serviceAvatars exception')
