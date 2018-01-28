#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/17 上午10:01
"""


import requests
import json
import time


from authServer.pyTools.decode.ctools import random_str


url = 'http://0.0.0.0:8081'
# url = 'http://auth.boxlinker.com'


# 用户注册
def test_signup(username, password, email):
    urltag = url + '/user/signup'
    data = {
        'username': username,
        'password': password,
        'email': email
    }
    response = requests.request('POST', url=urltag, data=data)
    return response.text.decode('utf-8').encode('utf-8')

def auto_test_signup(num=100):
    """ 自动注册 测试"""
    index = 0
    while index < num:
        name = random_str(le=10, letter=False)
        print test_signup(username=name, password=name, email=name + '@126all.com')
        index += 1

def test_login(username, password):
    payload = {
        'user_name': username,
        'password': password
    }
    urltag = url + '/user/login'
    response = requests.request('POST', url=urltag, data=payload)

    print response.text
    return response.text.decode('utf-8').encode('utf-8')

    # ss = json.loads(response.text.decode('utf-8').encode('utf-8'))
    # print ss['token']

def test_check_token(tokenid, token):
    payload = {
        'tokenid': tokenid,
        'token': token
    }
    urltag = url + '/user/check_token'
    response = requests.request('POST', url=urltag, data=payload)
    return response.text.decode('utf-8').encode('utf-8')

def test_flush_token(tokenid, token):
    payload = {
        'tokenid': tokenid,
        'token': token
    }
    urltag = url + '/user/flush_token'
    response = requests.request('POST', url=urltag, data=payload)
    return response.text.decode('utf-8').encode('utf-8')


def test_log_out(tokenid, token):
    payload = {
        'tokenid': tokenid,
        'token': token
    }
    urltag = url + '/user/log_out'
    response = requests.request('POST', url=urltag, data=payload)
    return response.text.decode('utf-8').encode('utf-8')


def test_log_in_out():
    retstr = test_login()
    retdict = json.loads(retstr)
    print retdict['token']
    print retdict['tokenid']

    print test_check_token(tokenid=retdict['tokenid'], token=retdict['token'])


    for i in range(0, 5):
        time.sleep(1)
        retstr = test_flush_token(tokenid=retdict['tokenid'], token=retdict['token'])
        retdict = json.loads(retstr)
        print retdict

    print test_log_out(tokenid=retdict['tokenid'], token=retdict['token'])
    print test_log_out(tokenid=retdict['tokenid'], token=retdict['token'])

def test_login_checktoken():
    retstr = test_login()
    retdict = json.loads(retstr)
    print retdict['token']
    print retdict['tokenid']

    print test_check_token(tokenid=retdict['tokenid'] , token=retdict['token'])

    token = 'eyJ1c2VybmFtZSI6ICIyMjMyIiwgImV4cGlyZXMiOiAxNDcxNDE4Mjg5LjQyNDIxNywgInNhbHQiOiAiMjBhZDQxMWQ2MDdiMjUyMDEwZTI1NDY3IiwgImVtYWlsIjogInd3ZXN3d3czc0AyMjN3MjN3Mi5jb20iLCAidWlkIjogMX0isH2TmSVT3EgLuMGgTRrw'
    tokenid = 'c1374c6a90c1307bf65dbb07'

    print test_check_token(tokenid=tokenid , token=token)



def test_check_token_only(token):

    url_temp = url + '/user/check_token_get'
    #headers = {'token': token}

    r = requests.get(url_temp)#, headers=headers)

    print r.text


if __name__ == '__main__':
    print test_login(username='admin', password='123456')

    exit(-1)


    print test_signup(username='admin', password='123456', email='it-111@all-reach.com')
    exit(-1)
    auto_test_signup(num=100)
    exit(-1)

    test_check_token_only('swewewews')
    exit(-1)
    test_login_checktoken()

