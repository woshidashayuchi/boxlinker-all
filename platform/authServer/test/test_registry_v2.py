#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/1 下午5:11
"""

from authServer.pyTools.docker.registry.docker_registry import *


def main():

    url = 'http://index.boxlinker.com'
    url = 'http://192.168.211.189'
    username = 'boxlinker'
    password = 'QAZwsx123'


    reg = Registry(url=url,
                   username=username,
                   password=password,
                   verify_ssl=False)

    try:
        reg.get_tags('libary/nginx')
        #reg.get_catalog()
        #reg.get_manifest('boxlinker/ubuntu', 'python_05')
    except AuthenticationError:
        print('Authentication error')
        sys.exit(2)



if __name__ == '__main__':
    main()

