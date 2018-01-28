#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/8/9
# Author:wang-xf

from es_json import create_esjson
import requests
import json
from common.logs import logging as log


def post_es(json_list, log_info):
    headers = {"token": json_list.get("token")}
    msg_json, es_url = create_esjson(json_list, log_info)
    log.info('post the messages to es, the struct base data is: %s' % msg_json)
    try:
        ret = requests.post(url=es_url, headers=headers, data=json.dumps(msg_json), timeout=3)
        log.info('post to es result is: %s' % ret.text)
    except Exception, e:
        log.error("es data give error,reason=%s" % e)
