#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/6 13:38
"""

from Crypto.Cipher import DES3
from Crypto.Cipher import DES

import hashlib
import base64

from Crypto import Random
from Crypto.Util import Counter


def CreateKey(salt):
    r = hashlib.md5(salt).digest()
    return r + r[:8]


def AddPad(clear):
    """ 添加填充 """
    pad_num = len(clear) % 16
    if pad_num != 0:
        pad = 16 - pad_num
        clear += chr(pad) * pad
    return clear


def RemovePad(src_str):
    """ 去除填充 """
    pad = src_str[-1:]
    pad_num = ord(pad)
    if pad_num > 16:
        return src_str

    return src_str[0:len(src_str) - pad_num]


def desEncryption(clear, key):
    """ des 加密 """
    keys = CreateKey(key)
    clear_text = AddPad(clear)
    # clear_text = clear
    des3 = DES3.new(keys, DES3.MODE_ECB)
    rss = des3.encrypt(clear_text)
    return base64.urlsafe_b64encode(rss)


def desDecipher(decipher, key):
    """ des 解密 """
    keys = CreateKey(key)
    decipher_text = base64.urlsafe_b64decode(decipher)
    des3 = DES3.new(keys, DES3.MODE_ECB)
    clear = des3.decrypt(decipher_text)
    clear_decrypt = RemovePad(clear)
    return clear_decrypt





if __name__ == '__main__':

    from authServer.pyTools.token.token import GenerateRandomString
    import random

    for i in range(1, 2000):

        ranLe = random.randint(12, 66)
        clear = GenerateRandomString(randlen=ranLe)

        # 随机明文 做秘钥
        ret = desEncryption(clear=clear, key=clear)
        ciphertext = desDecipher(ret, key=clear)

        if clear != ciphertext:
            print 'is error'
            print clear
            print ciphertext


