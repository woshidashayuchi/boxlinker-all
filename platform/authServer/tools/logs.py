#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/29 下午3:40
"""

from authServer.conf.conf import LOG_DEBUG

if LOG_DEBUG:
    import logging
else:
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        filename='.cloud.log',
        format='%(asctime)s [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a'
        )