#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: livenowhy@hotmail.com
@time: 2016/7/12 14:05
"""

import os
import io
import base64
import random
import time
import json
import hmac
import hashlib, binascii

from datetime import datetime, timedelta
from authServer.pyTools.decode.ctools import random_str

from authServer.pyTools.tools.codeString import request_result
auth_code = {}
TIMEOUT = 60 * 60 * 100 #3600 * 2  # 过期时间




BIGMEGA = 10

BIGFILESIZE = 1024 * 1024 * BIGMEGA

def little_file_md5(filename):
    global ret, md5value
    try:
        m = hashlib.md5()
        fp = open(filename, "rb")  # 需要使用二进制格式读取文件内容
        m.update(fp.read())
        fp.close()
        md5value = m.hexdigest()
        ret = True
    except Exception:
        ret = False
        md5value = ""
    finally:
        return ret, md5value


# 大文件的md5
def big__file_md5(filename):
    m = hashlib.md5()
    fp = io.FileIO(filename, "r")
    bufmsg = fp.read(1024)
    while bufmsg != b"":
        m.update(bufmsg)
        bufmsg = fp.read(1024)
    fp.close()
    return m.hexdigest()


def get_file_md5(filename):
    if os.path.getsize(filename) > BIGFILESIZE:
        return big__file_md5(filename)
    else:
        return little_file_md5(filename)


# md5_str:需要计算的值;   isUpper:是否返回大写格式
def get_md5(md5_str, isUpper=True):
    m = hashlib.md5()
    m.update(md5_str.encode("utf-8"))
    # m.update(md5_str.encode("gbk"))
    if isUpper:
        return str(m.hexdigest()).upper()
    else:
        return str(m.hexdigest()).lower()

def ValueAndTimeMd5(md5_str):
    timev = time.time()
    value = md5_str + str(timev) + str(random.randint(1, 10000))
    return get_md5(value)



# 生成一个随机的key
def make_random_key():
    random_s = random_str(le=24, letter=False)
    return ValueAndTimeMd5(random_s)


def encode_token_bytes(data):  # base64编码
    return base64.urlsafe_b64encode(data)


def decode_token_bytes(data):  # base64解码
    return base64.urlsafe_b64decode(data)


def get_password_by_name_password_salt(name, password, salt):
    """
    通过用户名,密码,盐, 得到用户的转加密密码数据
    :param name: 用户名
    :param password: 用户密码
    :param salt: 一个种子
    """
    try:
        password_01 = hashlib.md5(password).hexdigest() + salt
        password_02 = hashlib.md5(password_01).hexdigest() + name
        save_password = hashlib.md5(password_02).hexdigest().upper()
    except Exception:
        return False
    return save_password


def _get_signature(key, value):
    """
    使用hmac为消息生成签名
    :param key: 用于签名的秘钥
    :param value: 需要签名的信息
    :return:  Calculate the HMAC signature for the given value.
    """
    return hmac.new(key=key, msg=value).digest()


def gen_token(key, data, timeout=TIMEOUT):
    """
    token 生成器
    :param key: 用于签名的秘钥
    :param data: dict type 一个字典类型的参数
    :param timeout: 超时时间
    :return: base64 str
    """
    data = data.copy()

    if 'salt' not in data:
        data['salt'] = unicode(random.random()).decode('ascii')

    # 到期时间点
    if 'expires' not in data:
        data['expires'] = time.time() + timeout

    payload = json.dumps(data).encode('utf-8')

    print len(payload)
    print payload
    sig = _get_signature(key, payload)  # 签名信息
    return encode_token_bytes(payload + sig)


def gen_auth_code(uri, user_id):
    """
    授权码生成器
    :param uri:
    :param user_id:
    """
    code = random.randint(0, 10000)
    auth_code[code] = [uri, user_id]
    return code


def verify_token(key, token):
    """
    token验证
    :param token: base64 str
    :return: dict type
    """
    retdict = dict()
    retdict['status_code'] = 0
    try:
        decoded_token = decode_token_bytes(str(token))
    except Exception as msg:
        return request_result(602, ret={"msg": str(msg)})

    payload = decoded_token[:-16]
    sig = decoded_token[-16:]

    # 生成签名
    expected_sig = _get_signature(key=key, value=payload)
    if sig != expected_sig:   # 伪造的签名
        return request_result(203)

    data = json.loads(payload.decode('utf8'))
    if data.get('expires') >= time.time():
        return request_result(0, ret={"msg": data})
    else:
        # 签名过期
        x = time.localtime(data.get('expires'))
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', x)
        return request_result(204, ret={"Expired_Time": time_str})


def get_payload(token):
    """
    由token得到原始的加密数据
    :return:
    """
    try:
        ret = dict()
        decoded_token = decode_token_bytes(str(token))
        result = dict()
        result['payload'] = decoded_token[:-16]
        ret = request_result(0, ret=result)
    except Exception as msg:
        print msg.message
        ret = request_result(602, ret={"msg": str(msg)})
    finally:
        return ret

def get_pwd(username, userpwd):
    """
    得到用户存储的密码
    :param username: 用户名
    :param userpwd:  密码
    """
    salt = userpwd + username
    return get_password_by_name_password_salt(name=username, password=userpwd, salt=salt)


def encrypy_pbkdf2(password, salt):
    """
    用于生产pbkdf2密码, 返回用于存储的密码
    :param password: 明文密码
    :param salt: 盐
    """
    try:
        from hashlib import pbkdf2_hmac
    except Exception:
        from authServer.pyTools.decode.myhashlib import pbkdf2_hmac
    # dk = hashlib.pbkdf2_hmac(hash_name='sha1', password=password, salt=salt, iterations=4096, dklen=16)
    # pbkdf2_hmac was only just added to hashlib in Python 2.7.8 低版本python 没有pbkdf2_hmac 函数
    dk = pbkdf2_hmac(hash_name='sha1', password=password, salt=salt, iterations=4096, dklen=16)

    return binascii.hexlify(dk)


def GenerateRandomString(randlen=32):
    """
    GenerateRandomString generates a random string
    :param randlen: 随机字符串的长度
    """
    randomstr = ''
    while len(randomstr) < randlen:
        randstr = str(time.time()).replace('.', '-') + str(random.random()).replace('.', '-')
        randomstr += hashlib.md5(randstr).hexdigest() + randstr
    return randomstr[0:randlen]
