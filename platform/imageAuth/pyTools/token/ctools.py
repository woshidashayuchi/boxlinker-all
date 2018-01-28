#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/22 13:36
@func: 字符串操作函数
"""

from random import randint


def random_str(le=8, letter=True):
    """ 随机生成字符, le长度, letter 标示是否全是字母 """
    if letter:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    else:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

    length = len(chars) - 1
    str = ''
    for i in range(le):
        str += chars[randint(0, length)]
    return str
