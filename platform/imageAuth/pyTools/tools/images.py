#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/13 13:29
"""



import os
from PIL import Image, ImageDraw, ImageFont

import random
import math
import oss2

from common.logs import logging as log

from pyTools.tools.timeControl import get_timestamp_13



def TwoWordCreateImage(fonttype, fa, nd, savename):
    """ font: 字体文件, fa:第一个字母; nd:第二个字母 """
    width = 40  # 图片宽度
    height = 40  # 图片高度
    bgcolor = (0, 0, 0, 0)  # 背景颜色 透明

    fa = str(fa).upper()
    nd = str(nd).lower()

    image = Image.new('RGBA', (width, height), bgcolor)  # 生成背景图片
    font = ImageFont.truetype(fonttype, 50)  # 加载字体
    fontcolor = (32, 43, 0)  # 字体颜色

    draw = ImageDraw.Draw(image)  # 产生draw对象，draw是一些算法的集合

    draw.text((1, 0), fa, font=font, fill=fontcolor)  # 画字体,(0,0)是起始位置

    font_two = ImageFont.truetype(fonttype, 41)
    draw.text((23, 10), nd, font=font_two, fill=fontcolor)  # 画字体,(20, 5)是起始位置
    # 释放draw
    del draw

    # 保存原始版本
    image.save(savename)


def CreateImagePut(fonttype, fa, nd, savename, remoteName, access_key_id, access_key_secret, endpoint, bucker_name):
    try:

        log.info('CreateImagePut remoteName: %s, savename: %s' % (remoteName, savename))
        TwoWordCreateImage(fonttype, fa, nd, savename=savename)

        if os.path.exists(savename) is False:
            log.error('logo CreateImagePut  savename not exists')
            return False

        from pyTools.aliyu.oss import AliOss
        alioss = AliOss(access_key_id, access_key_secret, endpoint, bucker_name)
        if alioss.PutObjectFromFile(remoteName, savename) is False:
            log.error('CreateImagePut is False')
            return False
        return True
    except Exception, e:
        log.error('CreateImagePut is error: %s' % (e))
        return False

def setRepoLogo(repositoryname, fonttype, localpath, remopath, access_key_id, access_key_secret, endpoint, bucker_name):
    username, reponame = repositoryname.split('/')

    tt = str(get_timestamp_13()) + reponame

    savename = localpath + os.path.sep + tt + '.png'
    remoteName = remopath + os.path.sep + tt + '.png'

    if CreateImagePut(fonttype, reponame[0], reponame[1], savename, remoteName, access_key_id, access_key_secret, endpoint, bucker_name):
        if os.path.exists(savename):
            os.remove(savename)
        return remoteName

    return False


def CreatePutRetUrl(src_str, localpath, remopath, fonttype, access_key_id, access_key_secret, endpoint, bucker_name):
    if isinstance(src_str, str) is False:
        return False, 'not is str'

    if len(src_str) <= 2:
        return False, 'The string is too short'
    tt = str(get_timestamp_13()) + src_str

    savename = localpath + os.path.sep + tt + '.png'
    remoteName = remopath + os.path.sep + tt + '.png'
    if CreateImagePut(fonttype, src_str[0], src_str[1], savename, remoteName, access_key_id, access_key_secret, endpoint, bucker_name):

        # fonttype, fa, nd, savename, remoteName, access_key_id, access_key_secret, endpoint, bucker_name
        if os.path.exists(savename):
            os.remove(savename)
        return True, remoteName

    return False, ''


if __name__ == '__main__':
    import conf.conf as CONF

#     dd = setRepoLogo('sdsdsd/ssss', fonttype=CONF.FONTTYPE, localpath=CONF.LOCAL_PATH,
#                      remopath=CONF.RepositoryObject, access_key_id=CONF.AccessKeyID,
#                      access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
#                      bucker_name=CONF.BucketName)
#
# #    print dd

    # src_str, localpath, remopath, fonttype, access_key_id, access_key_secret, endpoint, bucker_name
    reb, dd = CreatePutRetUrl('sss', localpath=CONF.LOCAL_PATH, remopath=CONF.RepositoryObject,
                         fonttype=CONF.FONTTYPE, access_key_id=CONF.AccessKeyID, access_key_secret=CONF.AccessKeySecret, endpoint=CONF.Endpoint,
                     bucker_name=CONF.BucketName)
    print dd
    # print 'ssssssssss'
    # CreatePutRetUrl(12)