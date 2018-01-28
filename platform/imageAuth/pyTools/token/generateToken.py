#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/6 11:04
"""

from authServer.pyTools.tools.codeString import request_result
import authServer.pyTools.token.token as TK

from authServer.pyTools.token.des import desEncryption





def GenerateConfirmToken(kwargs, secret_key):
    """ 生成邮箱认证确认连接 """

    if 'email' not in kwargs:
        return request_result(707, ret='no email')

    if 'timeout' not in kwargs:
        kwargs['timeout'] = 60 * 60 * 24  # 一天

    if isinstance(kwargs['timeout'], (int, float)) is False:
        return request_result(707, 'timeout not is int or float')

    kwargs['salt'] = TK.GenerateRandomString(randlen=8)

    token = TK.gen_token(key=secret_key, data=kwargs, timeout=kwargs['timeout'])


    print "toekn"
    print token

    return request_result(0, ret={'token': token})


def GenerateConfirmUrl(email, secret_key, timeout=None):
    """
    根据邮箱和url前缀生成邮箱确认连接
    :param host_prefix:
    :param email:
    :param secret_key:
    :param timeout:
    :return:
    """

    dk = dict()

    print 'emis'
    print email

    dk['email'] = email

    if timeout is not None and isinstance(timeout, (int, float)) is False:
        return request_result(707, 'timeout not is int or float')

    retToken = GenerateConfirmToken(dk, secret_key=secret_key)

    if 'status' in retToken and 0 == retToken['status']:
        confirmUrl = retToken['result']['token']
        return request_result(0, ret=confirmUrl)

    return request_result(100, ret='is eoor')


def GenerateConfirmUrlDes(email, secret_key, timeout=None):
    confirmUrl = GenerateConfirmUrl(email, secret_key, timeout=None)
    if 'status' in confirmUrl and 0 != confirmUrl['status']:
        return confirmUrl


    print "confirmUrl['result']"
    print confirmUrl['result']

    des_url = desEncryption(confirmUrl['result'], secret_key)

    print des_url
    return request_result(0, ret=des_url)





if __name__ == '__main__':

    print 'ss'

    url = GenerateConfirmUrl(url_prefix='http://boxlinker.com/url',
                       email='liuzhangpei@126.com',
                       secret_key='ssss')


    print url
