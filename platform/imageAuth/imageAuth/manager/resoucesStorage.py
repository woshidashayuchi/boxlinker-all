#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/16 10:31
"""

import requests

from common.logs import logging as log


image_repo_prefix = 'http://101.200.45.76:8765'
def GetFileByLocation(team_uuid, resource_type, resource_uuid, resource_domain):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/' + team_uuid + '/' + resource_type + '/' + resource_uuid + '/' + resource_domain
    url = image_repo_prefix + url_suffix
    # headers = {'token': token}
    ret = requests.get(url, timeout=5, verify=True)

    if ret.json()['status'] != 0:
        log.info("ret.json()['status'] != 0")
        return False, None

    if len(ret.json()['result']) == 0:
        log.info("len(ret.json()['result']) == 0")
        return False, None

    try:
        storage_url = ret.json()['result'][0]['storage_url']
        return True, storage_url
    except Exception:
        return False, None

def SetFileUrlSave(team_uuid, resource_type, resource_uuid, resource_domain, file_url):
    """ 镜像名得到镜像id """
    url_suffix = '/api/v1.0/files/' + team_uuid + '/' + resource_type + '/' + resource_uuid + '/' + resource_domain
    url = image_repo_prefix + url_suffix
    data = """
    {
        "file_url": "$FILEURL"
    }
    """
    data = data.replace("$FILEURL", file_url)
    ret = requests.post(url, data=data, timeout=5, verify=True)
    log.info(str(ret.json()))


if __name__ == '__main__':
    retbool, image_dir = GetFileByLocation(team_uuid="2e8e7b37-a957-4770-9075-aaa67eaa49ce", resource_type="ImageAvatars",
                      resource_uuid="bf1f9123-d5c9-31c5-988a-d417bfb37915", resource_domain="boxlinker")

    if retbool:
        print image_dir