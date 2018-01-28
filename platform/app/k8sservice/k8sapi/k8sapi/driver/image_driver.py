# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/20
import json
import requests
from conf import conf
from common.logs import logging as log


def images_message_get(dict_data):
    image_id = dict_data.get('image_id')
    image_server = conf.IMAGE_S

    url = 'http://%s/api/v1.0/imagerepo/image/tagid/%s' % (image_server, image_id)
    token = dict_data.get('token')
    headers = {'token': token}

    try:
        image_message = requests.get(url, headers=headers, timeout=5).text
        image_result = json.loads(image_message)
        log.info('the image message from image_id is: %s, type is: %s' % (image_message, type(image_message)))
        if image_result.get('status') != 0:
            return False

        image_name = conf.IMAGE_H + image_result.get('result').get('image_name')
        image_version = image_result.get('result').get('tag')
    except Exception, e:
        log.error('get the images message error, reason is: %s' % e)
        return False

    return image_name, image_version
