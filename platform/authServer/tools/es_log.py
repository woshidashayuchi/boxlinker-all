#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/18 16:43
@func: es 日志处理
"""

import json
import time
import requests
from authServer.pyTools.tools.timeControl import get_now_time_ymd, get_now_time, get_now_time_ss_z, get_timestamp_13

HOST = 'http://es.boxlinker.com'
TYPE = 'fluentd'


log_dict = {
    'time': None,
    'level': 'ERROR',
    'log': {
        'userid': None,
        'log_info': None
    }
}

msg_json = {
    "log": "{\"time\": \"2016-09-19 02:59:27\", \"level\": \"INFO\", \"file\": \"TestLog.py_auto_build\", \"log\": {\"userid\": \"boxlinker\", \"log_info\": \"log testpy_auto_build\"}}\n",
    "kubernetes":
        {
            "namespace_name": "github_py_auto_build",
            "pod_id": "b8021644-78db-11e6-github_py_auto_build",
            "pod_name": "github_py_auto_build_pod_name",
            "container_name": "log-py_auto_build",
            "labels":
                {
                    # "logs": "auto_build-UserName-ProId"
                    "logs": "auto_build-boxlinker-webhooks-test"

                },
        },
    "@timestamp": "2016-09-19T02:59:27.716980211Z",
    #"fields": {'time': [1474358223165]}
}
#
# HOST = 'http://es.boxlinker.com'
# TYPE = 'fluentd'
def get_index():
    return 'logstash-' + get_now_time_ymd(part='.')

# http://es.boxlinker.com/logstash-2016.09.18/eeeee?pretty
# curl -<REST Verb> <Node>:<Port>/<Index>/<Type><ID>




# 没有索引进行数据添加
def no_id_post(payload):
    global HOST, TYPE
    index = get_index()
    url = HOST + '/' + index + '/' + TYPE + '?pretty'
    print 'post log data .....'

    querystring = {'pretty': ''}
    print url

    print payload

    try:
        response = requests.request(method='POST', url=url, data=payload, params=querystring, timeout=3)

        if response.status_code != 200:
            print url, ' is status code 200'
            return True

        json_t = json.loads(response.text.decode('utf-8').encode('utf-8'))

        if 'created' in json_t and json_t['created']:
            print ' send msg is ok '
        else:
            print ' send msg is ok error '
    except Exception as msg:
        print 'post log data have Exception'
        print msg.message
        print msg.args


def send_msg_to_es(log_info, labels_logs):
    print 'send_msg_to_es----begin'
    print log_info
    print labels_logs

    log_msg = msg_json
    log_msg['@timestamp'] = str(get_now_time_ss_z())
    log_msg['log'] = str(log_info)

    log_msg['kubernetes']['labels']['logs'] = str(labels_logs)

    log_msg_str = json.dumps(log_msg)

    print type(log_msg_str)


    print 'send_msg_to_es'
    no_id_post(log_msg_str)


def send_msg_to_es_test():
    log_msg = msg_json
    log_msg['@timestamp'] = str(get_now_time_ss_z())

    log_msg_str = json.dumps(log_msg)

    log_msg_str = json.dumps(msg_json)
    print log_msg_str + '\n'
    no_id_post(log_msg_str)


# def send_log(log_info, user_name, labels_logs):
def send_log(kwargs):

    log_d = log_dict
    # log_d['time'] = get_now_time()
    log_d['time'] = get_timestamp_13()
    log_d['log']['log_info'] = kwargs['log_info']
    log_d['log']['userid'] = kwargs['user_name']

    log_msg_str = json.dumps(log_d)

    send_msg_to_es(log_info=log_msg_str, labels_logs=kwargs['labels_logs'])


if __name__ == '__main__':

    di = dict()

    di['log_info'] = 'log_info'
    di['user_name'] = 'boxlinker'
    di['labels_logs'] = 'auto_build-boxlinker-12'


    while True:
        send_log(di)
        #send_log(log_info='test----', user_name='boxlinker', labels_logs='auto_build-boxlinker-webhooks-test')
        time.sleep(5)
