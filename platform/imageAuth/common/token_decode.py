#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import base64

from common.token_auth import token_check


def decode_token_bytes(data):

    return base64.urlsafe_b64decode(data)


@token_check
def get_userinfo(token):
    """
    由token得到原始的加密数据
    :return:
    """
    retdict = dict()
    retdict['status_code'] = 0
    try:
        decoded_token = decode_token_bytes(str(token))
        retdict['msg'] = 'is ok'
        retdict['user_info'] = decoded_token[:-16]
        retdict['sig'] = decoded_token[-16:]
    except Exception as msg:
        retdict['status_code'] = 1
        retdict['msg'] = str(msg)
    finally:
        return retdict

if __name__ == "__main__":

    token = sys.argv[1]

    user_info = get_userinfo(token)
