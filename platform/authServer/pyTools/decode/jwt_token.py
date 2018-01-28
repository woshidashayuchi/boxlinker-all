#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/24 9:33
@from: git@github.com:tarunbhardwaj/docker-token-user.git
@node: modify by lzp
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

    algorithm = 'RS256'

	#issuer     = "RegistryWeb-token-issuer"
	#privateKey = "/etc/ui/private_key.pem"

    def __init__(self, account, service, scope, private_key):
        self.account = account
        self.service = service
        self.scope = scope
        self.private_key = open(private_key).read()   # key需要自定义

    def claim(self):
        issuer = "RegistryWeb-token-issuer"
        return {
            "iss": issuer,  # 需要自定义
            "sub": self.account,
            "aud": self.service,
            "exp": int(time.time()) + (10000 * 60),  # add lzp 过期时间
            "nbf": int(time.time()) - (10000 * 60),  # 镜像库的时间延迟了
            "iat": int(time.time()) - (10000*60),
            "jti": str(uuid.uuid4()),
            "access": self.scope and [
                {
                    "type": self.scope.type,  # add lzp   catalog操作是: RegistryWeb:catalog:*
                    "name": self.scope.image,
                    "actions": self.scope.actions

                }
            ]
        }


    def generate(self):
        """ Generate JWT token """
        # from jwt.jwk import JWKSet
        # keys = JWKSet()
        # #jjwt = JWT(keys=self.private_key)
        # jjwt = JWT(keys=keys)
        #payload = b64_decode(bytes(self.claim()))

        return jwt.encode(self.claim(), self.private_key, algorithm=self.algorithm, headers=self.headers())

        #return jjwt.encode(headerobj=self.headers(), payload=payload )




    def headers(self):
        """ JWT header """
        return {
            'typ': 'JWT',
            'alg': self.algorithm,
            'kid': self.jwt_kid()
        }

    def jwt_kid(self):
        """ Generates ID for signing key """
        key = RSA.importKey(self.private_key)
        der = key.publickey().exportKey("DER")
        payload = hashlib.sha256(der).digest()[:30]
        kid = base64.b32encode(payload)
        return ":".join([kid[i:i + 4] for i in range(0, len(kid), 4)])
