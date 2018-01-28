# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
import hashlib


def md5_encrypt(encrypt_str):

    m = hashlib.md5()
    m.update(encrypt_str)

    return m.hexdigest()


if __name__ == "__main__":

    parameter = sys.argv[1]

    try:
        m = md5_encrypt(parameter)
        print('parameter(%s) encrypt success, result=%s' % (parameter, m))
    except Exception, e:
        print('parameter(%s) encrypt error, reason=%s' % (parameter, e))
