#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/23 2:40
"""

import requests


from authServer.conf.conf import private_key

from authServer.pyTools.decode.jwt_token import JwtToken

from collections import namedtuple
Scope = namedtuple('Scope', ['type', 'image', 'actions'])

def get_jwt_token(account, service, scopes):

    if scopes == '':
        scope = None
    else:
        print scopes
        type_, image, actions = scopes.split(':')
        actionlist = actions.split(',')
        scope = Scope(type_, image, actionlist)

    token = JwtToken(account='asassssss', service='aaaaaaaaaasasas', scope=scope, private_key=private_key).generate()
    res = {"token": token}
    print token

if __name__ == '__main__':
    print 'ss'
    response = requests.get(url='http://verify-code.boxlinker.com/check_code/c3f32490-95c0-11e6-8982-6fd924e66fdf?code=oyp8',
                            timeout=4)
    if response.json()['status'] == 1:
        print 'sss'

