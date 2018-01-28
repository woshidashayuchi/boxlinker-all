#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/13 13:34
"""


import oss2
from common.logs import logging as log

class AliOss(object):
    def __init__(self, access_key_id, access_key_secret, endpoint, bucker_name):
        self.AccessKeyID = access_key_id
        self.AccessKeySecret = access_key_secret
        self.Endpoint = endpoint
        self.BucketName = bucker_name

        try:
            self.auth = oss2.Auth(self.AccessKeyID, self.AccessKeySecret)
            self.bucket = oss2.Bucket(self.auth, self.Endpoint, self.BucketName)
        except Exception as msg:
            log.error("AliOss init is error " + msg.message)
            raise Exception("AliOss init is error ")

    def PutObjectFromFile(self, remoteName, localFile):
        """ localFile:本地文件名及路径; nameObject:Object文件名 """
        try:
            ret = self.bucket.put_object_from_file(remoteName, localFile)
            log.info('PutObjectFromFile remoteName:%s  localFile:%s', remoteName, localFile)
            if 200 == ret.status:
                # print ret.crc
                # print ret.headers
                # print ret.etag
                return True
        except Exception as msg:
            log.error('PutObjectFromFile is error:' + str(msg.message))
            return False