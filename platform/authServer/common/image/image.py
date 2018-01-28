#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/30 17:16
"""

# -*- coding: utf-8 -*-
#导入三个模块


import os
from PIL import Image, ImageDraw, ImageFont
import random
import math
import oss2

from authServer.pyTools.tools.codeString import request_result

from authServer.conf.conf import AccessKeyID, AccessKeySecret, Endpoint, BucketName, \
    RepositoryObject, FONTTTC, CONFPATH

def init(localfile):
    auth = oss2.Auth(AccessKeyID, AccessKeySecret)
    # service = oss2.Service(auth, Endpoint)

    bucket = oss2.Bucket(auth, Endpoint, BucketName)

    ret = bucket.put_object_from_file('repository/remote.txt', 'local.txt')

    if 200 == ret.status:
        print 'is osk'

        print ret.crc
        print ret.headers
        print ret.etag


def PutObjectFile(remoteName, localFile):
    """ localFile:本地文件名及路径; nameObject:Object文件名 """
    try:
        auth = oss2.Auth(AccessKeyID, AccessKeySecret)
        # service = oss2.Service(auth, Endpoint)

        bucket = oss2.Bucket(auth, Endpoint, BucketName)
        ret = bucket.put_object_from_file(remoteName, localFile)

        print 'logo PutObjectFile  ret.status = ' + str(ret.status)
        if 200 == ret.status:
            print ret.crc
            print ret.headers
            print ret.etag
            return True
    except Exception as msg:
        print 'logo CreateImagePut  savename if False'
        print 'logo CreateImagePut  savename if False' + str(msg.message)
        return False





def TwoWordCreateImage(fa, nd, savename):
    """ fa:第一个字母; nd:第二个字母 """
    width = 40  # 图片宽度
    height = 40  # 图片高度
    bgcolor = (0, 0, 0, 0)  # 背景颜色 透明

    fa = str(fa).upper()
    nd = str(nd).lower()

    image = Image.new('RGBA', (width, height), bgcolor)  # 生成背景图片

    font = ImageFont.truetype(FONTTTC, 50)  # 加载字体

    print 'sde'

    fontcolor = (32, 43, 0)  # 字体颜色

    draw = ImageDraw.Draw(image)  # 产生draw对象，draw是一些算法的集合

    draw.text((1, 0), fa, font=font, fill=fontcolor)  # 画字体,(0,0)是起始位置

    font_two = ImageFont.truetype(FONTTTC, 41)
    draw.text((23, 10), nd, font=font_two, fill=fontcolor)  # 画字体,(20, 5)是起始位置
    # 释放draw
    del draw
    # 保存原始版本

    print savename
    image.save(savename)



def CreateImagePut(fa, nd, savename, remoteName):
    try:

        print 'logo CreateImagePut remoteName:' + remoteName
        TwoWordCreateImage(fa, nd, savename=savename)
        print 'logo CreateImagePut remoteName:'
        if os.path.exists(savename) is False:
            print 'logo CreateImagePut  savename not exists'
            return False

        if PutObjectFile(remoteName, savename) is False:
            print 'logo CreateImagePut  savename if False'
            return False
        return True
    except Exception as msg:
        print msg.message
        return False


from authServer.pyTools.tools.timeControl import get_timestamp_13


def setRepoLogo(repositoryname):
    username, reponame = repositoryname.split('/')

    tt = str(get_timestamp_13()) + reponame

    savename = CONFPATH + os.path.sep + tt + '.png'
    remoteName = RepositoryObject + os.path.sep + tt + '.png'

    print 'logo setRepoLogo savename:' + savename
    print 'logo setRepoLogo remoteName:' + remoteName

    if CreateImagePut(reponame[0], reponame[1], savename, remoteName):
        if os.path.exists(savename):
            os.remove(savename)
        return remoteName

    print 'ser iserror'
    return False


def CreatePutRetUrl(src_str):
    if isinstance(src_str, str) is False:
        return request_result(706, ret='not is str')

    if len(src_str) <= 2:
        return request_result(706, ret='The string is too short')


    tt = str(get_timestamp_13()) + src_str

    savename = CONFPATH + os.path.sep + tt + '.png'
    remoteName = RepositoryObject + os.path.sep + tt + '.png'

    print 'logo setRepoLogo savename:' + savename
    print 'logo setRepoLogo remoteName:' + remoteName

    if CreateImagePut(src_str[0], src_str[1], savename, remoteName):
        if os.path.exists(savename):

            os.remove(savename)
        return remoteName

    return False


if __name__ == '__main__':
    # setRepoLogo('sss/ss')

    CreatePutRetUrl('sss')
    print 'ssssssssss'
    CreatePutRetUrl(12)