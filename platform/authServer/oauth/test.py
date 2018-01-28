#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/6 下午2:32
"""

import requests




def test():
    headers = {
        'authorization': 'token 53948684a2429ec2b553ff29fabe7929500717b4'
    }


    response = requests.get(url='https://api.github.com/repos/liuzhangpei/webhook_test', headers=headers)
    # response = requests.get(url='https://api.github.com/livenowhy/teams?access_token=c76e1b9018f9bef93be8618c0883ed1716c813c2', headers=headers)
    print response.json()
    print response.status_code
    print response.text
    for kk in response.headers:
        print kk
        print response.headers[kk]
    print 'ssss'


def user_info():
    headers = {
        'authorization': 'token 53948684a2429ec2b553ff29fabe7929500717b4'
    }


    github_repos_url = 'https://api.github.com/users/liuzhangpei/repos'
    try:
        r = requests.get(github_repos_url, headers=headers, timeout=1)
        print r.json()
        print r.status_code

    except Exception as msg:
        print msg.message





def get_user():

    headers = {
        'authorization': 'token 53948684a2429ec2b553ff29fabe7929500717b4'
    }

    response = requests.get('https://api.github.com/user', headers=headers)

    rjson = response.json()
    email = rjson['email']
    login = rjson['login']
    id = rjson['id']
    print id
    print email
    print login
    print rjson

def test_hook():
    headers = {
        'authorization': 'token f03f8205d36933adbbb2a8ab00b29c086ac57cf6'
    }

    url = "https://api.github.com/users/liuzhangpei/repos"
    url = "https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks"
    response = requests.get(url=url, headers=headers)

    rjson = response.json()
    print rjson

    # https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10242277
