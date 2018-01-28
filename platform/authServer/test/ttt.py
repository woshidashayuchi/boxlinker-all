#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/2 11:07
@镜像库 notifications 接口
"""



import requests

from authServer.conf.conf import DEBUG, ROLLING_UPDATE

json = """
{'events': [{'target': {'repository': 'liuzhangpei/alpine', 'url': 'https://index.boxlinker.com/v2/liuzhangpei/alpine/manifests/sha256:49ffd3501f6cc281d9f0f9eeeeea31aa031ab4ef65b3a69be5f04edb3b33601e', 'mediaType': 'application/vnd.docker.distribution.manifest.v2+json', 'length': 735, 'tag': 'latest', 'digest': 'sha256:49ffd3501f6cc281d9f0f9eeeeea31aa031ab4ef65b3a69be5f04edb3b33601e', 'size': 735}, 'timestamp': '2017-01-11T16:34:52.142783938Z', 'request': {'method': 'GET', 'host': 'index.boxlinker.com', 'useragent': 'docker/1.12.3 go/go1.6.3 git-commit/6b644ec kernel/3.10.0-327.3.1.el7.x86_64 os/linux arch/amd64 UpstreamClient(Go-http-client/1.1)', 'id': '9fd64ed8-5f44-4319-8a97-9aef54b39f21', 'addr': '192.168.1.8'}, 'actor': {'name': 'boxlinker'}, 'source': {'instanceID': '4ae2480a-217b-489e-85a6-4d73379bee33', 'addr': '8b13b346c675:5000'}, 'action': 'pull', 'id': '9f1f20c4-7e3c-4d5f-b418-d68ff8efb5d5'}]}
"""



# 镜像库回调通知接口
def Notifications():
        # 通知滚动更新程序,进行服务更新操作

    try:
        # response = requests.post('http://krud.boxlinker.com', json=request.json)
        print "request.json : "
        print json

        response = requests.post(ROLLING_UPDATE, json=json)
        print response.status_code
        print response.reason
    except Exception as msg:
        print 'Notifications is error'
        print msg.message


if __name__ == '__main__':
    Notifications()