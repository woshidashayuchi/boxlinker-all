# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import os
import time
import inspect
import requests

from conf import conf
from common.logs import logging as log
from common.local_cache import LocalCache
from common.code import request_result


requests.adapters.DEFAULT_RETRIES = 5
caches = LocalCache(100)
token_auth_url = '%s%s' % (conf.ucenter_api, '/api/v1.0/ucenter/tokens')


def token_auth(token):

    log.debug('start token check, token=%s' % (token))
    token_info = caches.get(token)
    if (token_info is LocalCache.notFound):
        log.debug('Cache token auth not hit, token=%s' % (token))
        try:
            headers = {'token': token}
            ret = requests.get(token_auth_url,
                               headers=headers, timeout=5).json()
            status = ret['status']
            if status != 0:
                raise(Exception('Token auth denied'))
        except Exception, e:
            log.warning('Token ucenter auth error: reason=%s' % (e))
            raise(Exception('Token auth error'))

        expire = int(time.time()) + 300
        caches.set(token, {"token_info": ret, "expire": expire})
    else:
        log.debug('Cache token auth hit, token=%s' % (token))
        ret = token_info['token_info']

    log.debug('token_info = %s' % (ret))

    return ret


def token_check(func):

    def _tokenauth(*args, **kwargs):

        try:
            func_args = inspect.getcallargs(func, *args, **kwargs)
            token = func_args.get('token')
            if token is None:
                context = func_args.get('context')
                if context is None:
                    for context in func_args.get('args'):
                        if isinstance(context, dict):
                            break

            token = context.get('token')
            log.debug('token=%s' % (token))

            userinfo_auth = token_auth(token)['status']
            if userinfo_auth == 0:
                try:
                    result = func(*args, **kwargs)
                except Exception, e:
                    log.error('function(%s) exec error, reason = %s'
                              % (func.__name__, e))
                    return request_result(601)
            else:
                log.warning('User token auth denied: token = %s' % (token))
                raise

            return result
        except Exception, e:
            log.error('Token auth error, reason=%s' % (e))
            return request_result(201)

    return _tokenauth
