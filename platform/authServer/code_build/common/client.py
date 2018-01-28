#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from authServer.conf.conf import queue_name, exchange_name
from authServer.pyTools.tools.codeString import request_result
from rabbitmq_client import RabbitmqClient


class Send_Build_Msg(object):
    def __init__(self):
        self.rmq_client = RabbitmqClient()
        self.queue_name = queue_name
        self.timeout = 60
        self.exchange_name = exchange_name

    def send_msg(self, dict_data):
        try:
            json_data = json.dumps(dict_data)

            # ret = self.rmq_client.rpc_cast_client(self.queue_name, json_data)
            ret = self.rmq_client.broadcast_client(self.exchange_name, json_data)  # 广播

            print ret
            return ret
        except Exception, e:
            print e.message
            print e.args
            return request_result(598)


if __name__ == '__main__':
    sbm = Send_Build_Msg()

    while True:

        response_d = dict()

        response_d['id'] = '6070423'

        response_d['git_uid'] = '6070423'
        response_d['repo_id'] = '67769637'
        response_d['repo_name'] = 'webhook_test'
        response_d['repo_branch'] = 'master'
        response_d['repo_hook_token'] = 'B3AD25911454EEE0AD5CA7AC7B3B18DE'
        response_d['is_hook'] = '1'
        response_d['images_name'] = 'webhook_test_test'
        response_d['dockerfile_path'] = '/docker'
        response_d['dockerfile_name'] = 'Dockerfile'
        response_d['auto_build'] = '1'
        response_d['image_tag'] = 'auto_yr'
        response_d['src_type'] = 'github'

        response_d['git_name'] = 'liuzhangpei'  # github 用户名
        response_d['user_name'] = 'boxlinker'  # 系统平台name


        sbm.send_msg(response_d)
        import time
        time.sleep(2)