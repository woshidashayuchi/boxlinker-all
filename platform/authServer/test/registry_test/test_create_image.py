#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/9/28 17:25
"""

import requests
import json
import time

from authServer.pyTools.token.token import get_md5

url = 'http://0.0.0.0:8080'
# url = 'http://auth.boxlinker.com'

token = "eyJ1aWQiOiAzLCAidXNlcl9vcmFnIjogImJveGxpbmtlciIsICJ0b2tlbmlkIjogIjJhYTRkOTVlN2RhNzkzMmYzODE3MDdhZSIsICJ1c2VyX25hbWUiOiAiYm94bGlua2VyIiwgImV4cGlyZXMiOiAxNDc2MDc3NTEwLjk3MTc2NiwgInVzZXJfcm9sZSI6ICIxIiwgInVzZXJfaXAiOiAiMTI3LjAuMC4xIiwgInNhbHQiOiAiZTMzNjM2MzZlODdlYTgxZjc0OWVmOTZmIiwgImVtYWlsIjogImxpdmVub3doeUAxMjYuY29tIn1WSjYmT81bEGCwIraTbE-X"



# 用户注册
def test_imaget_project(is_public, detail, name, repositories):

    urltag = url + '/registry/create'
    data = {
        "is_public": "1",
        "detail": detail,
        "repositories": repositories
    }

    headers = {
        'token': token,
        'content-type': "application/json",
    }




    response = requests.request('POST', url=urltag, data=json.dumps(data), headers=headers)
    return response.text.decode('utf-8').encode('utf-8')


def insert_data():
    image_l = ["boxlinker/0928",
      "boxlinker/alpine",
      "boxlinker/boxl-notification",
      "boxlinker/centos",
      "boxlinker/centos-base",
      "boxlinker/centos-k8sapi",
      "boxlinker/centos-k8sapis",
      "boxlinker/centos-logs",
      "boxlinker/centos-logtest",
      "boxlinker/centos-mariadb",
      "boxlinker/centos-monitor",
      "boxlinker/centos-rabbitmq",
      "boxlinker/centos-storage",
      "boxlinker/centos7-base",
      "boxlinker/centos7-k8sapi",
      "boxlinker/chat-demo",
      "boxlinker/ci-api",
      "boxlinker/docker-elasticsearch-kubernetes",
      "boxlinker/docker-tes",
      "boxlinker/fluentd-kubernetes",
      "boxlinker/heapster",
      "boxlinker/heapster_grafana",
      "boxlinker/heapster_influxdb",
      "boxlinker/kibana",
      "boxlinker/krud",
      "boxlinker/mariadb-base",
      "boxlinker/nginx-apidoc",
      "boxlinker/nginx-k8sapidoc",
      "boxlinker/python",
      "boxlinker/servicelb",
      "boxlinker/test",
      "boxlinker/test-k8sapi",
      "boxlinker/test-k8sapi.1.0.0",
      "boxlinker/test-k8sapis",
      "boxlinker/tttt-k8sapi",
      "boxlinker/ubuntu",
      "boxlinker/web",
      "boxlinker/webhook_test_test",
      "boxlinker/zss",
      "cabernety/aaaaaa",
      "cabernety/building-test",
      "cabernety/chat-demo",
      "cabernety/chattest",
      "cabernety/demo3",
      "cabernety/nginx",
      "google_containers/busybox",
      "google_containers/etcd",
      "google_containers/kube2sky",
      "google_containers/pause",
      "google_containers/skydns",
      "library/alpine-node",
      "library/building-test",
      "library/mysql",
      "library/nginx",
      "liuzhangpei/alpine",
      "liuzhangpei/nginx",
      "liuzhangpei/python",
      "liuzhangpei/pythontest",
      "liuzhangpei/pythontest2",
      "lxf/centos-k8test",
      "phpmyadmin/phpmyadmin",
      "wangjian/acc",
      "wangjian/admin",
      "zs/react_me"]


    for node in image_l:
        uname, i_name = str(node).split('/')
        print 'sssssss'
        print uname
        print i_name
        print node
        detail = get_md5(node)
        print detail
        print test_imaget_project('1', detail, i_name, node)


if __name__ == '__main__':
    insert_data()


