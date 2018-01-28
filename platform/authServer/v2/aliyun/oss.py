#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/11/17 09:55
"""


from flask import Response, request, Request
from flask_restful import Resource

import socket
import httplib
import base64
import md5
import urllib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from M2Crypto import RSA
from M2Crypto import BIO

class OssCallBack(Resource):
    def post(self):

        retResponse = Response()
        retResponse.status_code = 400
        #get public key
        pub_key_url = ''
        try:
            pub_key_url_base64 = request.headers.get('x-oss-pub-key-url', default='').decode('utf-8').encode('utf-8')
            pub_key_url = pub_key_url_base64.decode('base64')
            url_reader = urllib2.urlopen(pub_key_url)
            pub_key = url_reader.read()
        except:
            print 'pub_key_url : ' + pub_key_url
            print 'Get pub key failed!'


            return retResponse

        #get authorization
        authorization_base64 = request.headers.get('authorization', default='').decode('utf-8').encode('utf-8')
        authorization = authorization_base64.decode('base64')

        #get callback body
        content_length = request.headers.get('content-length', default='').decode('utf-8').encode('utf-8')
        callback_body = request.data
        # callback_body = self.rfile.read(int(content_length))

        #compose authorization string
        auth_str = ''
        path = request.path
        pos = path.find('?')

        pos = request.url
        if -1 == pos:
            auth_str = path + '\n' + callback_body
        else:
            auth_str = urllib2.unquote(path[0:pos]) + path[pos:] + '\n' + callback_body
        print auth_str

        #verify authorization
        auth_md5 = md5.new(auth_str).digest()
        bio = BIO.MemoryBuffer(pub_key)
        rsa_pub = RSA.load_pub_key_bio(bio)
        try:
            result = rsa_pub.verify(auth_md5, authorization, 'md5')
        except Exception as msg:
            result = False
            print msg.message

        if not result:
            print 'Authorization verify failed!'
            print 'Public key : %s' % (pub_key)
            print 'Auth string : %s' % (auth_str)

            retResponse.status_code = 400

            return retResponse

        #do something accoding to callback_body

        #response to OSS
        resp_body = '{"Status":"OK"}'

        retResponse.status_code = 200
        retResponse.headers.set('Content-Type', 'application/json')
        retResponse.headers.set('Content-Length', str(len(resp_body)))

        retResponse.set_data(resp_body)
        return retResponse