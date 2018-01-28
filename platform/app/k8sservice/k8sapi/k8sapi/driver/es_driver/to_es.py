#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/8/9
# Author:wang-xf

from es_json import create_esjson
import requests
import json
from common.logs import logging as log


def post_es(dict_data, log_info):
    headers = {"token": dict_data.get("token")}
    msg_json, es_url = create_esjson(dict_data, log_info)
    try:
        log.info('post the message to es, the data is: %s, es_url is: %s' % (msg_json, es_url))
        requests.post(url=es_url, headers=headers, data=json.dumps(msg_json)+"\n", timeout=1)
    except Exception, e:
        log.error("es data give error,reason=%s" % e)
