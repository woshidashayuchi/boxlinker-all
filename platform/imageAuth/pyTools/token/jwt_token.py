#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@from: git@github.com:tarunbhardwaj/docker-token-user.git modify by lzp
"""

import os
import base64
import time
import uuid
import hashlib
import jwt
from Crypto.PublicKey import RSA


class JwtToken():
    """ Generate Token """
    def __init__(self, account, service, scope, issuer, private_key, algorithm='RS256'):
        self.account = account
        self.service = service
        self.scope = scope
        self.private_key = open(private_key).read()   # key需要自定义
        self.algorithm = algorithm  # 加密方式
        self.issuer = issuer        # 需要和registry中config配置一样

    # 声明
    def claim(self):
        token = {
            'iss': self.issuer,  # 需要自定义
            'sub': self.account,
            'aud': self.service,
            'exp': int(time.time()) + (10000 * 60),  # add lzp 过期时间
            'nbf': int(time.time()) - (10000 * 60),  # 镜像库的时间延迟了
            'iat': int(time.time()) - (10000*60),
            'jti': str(uuid.uuid4()),
            'access': self.scope and [
                {
                    'type': self.scope.type, # add lzp   catalog操作是: RegistryWeb:catalog:*
                    'name': self.scope.image,
                    'actions': self.scope.actions
                }
            ]
        }
        return token

    def jwt_kid(self):
        """ Generates ID for signing key """
        key = RSA.importKey(self.private_key)
        der = key.publickey().exportKey("DER")
        payload = hashlib.sha256(der).digest()[:30]
        kid = base64.b32encode(payload)
        return ":".join([kid[i:i + 4] for i in range(0, len(kid), 4)])

    def headers(self):
        """ JWT header """
        print
        return {
            'typ': 'JWT',
            'alg': self.algorithm,
            'kid': self.jwt_kid()
        }

    def generate(self):
        """ Generate JWT token """
        return jwt.encode(self.claim(), self.private_key, algorithm=self.algorithm, headers=self.headers())


    # from jwt.jwk import JWKSet
    # keys = JWKSet()
    # #jjwt = JWT(keys=self.private_key)
    # jjwt = JWT(keys=keys)
    # payload = b64_decode(bytes(self.claim()))

    # return jjwt.encode(headerobj=self.headers(), payload=payload )


def safe_JwtToken(account, service, scope, issuer, private_key):
    """
    解决: self._backend._lib.RSA_R_DIGEST_TOO_BIG_FOR_RSA_KEY 报错问题, 问题导致原因是采用了Apache架构
    """
    safe_num = 3
    while safe_num > 0:
        try:
            token = JwtToken(account=account, service=service, scope=scope, issuer=issuer, private_key=private_key).generate()
            return token
        except Exception as msg:
            return None
    return None