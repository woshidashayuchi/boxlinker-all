# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


import time
import inspect

from common.logs import logging as log
from common.code import request_result


def time_log(func):

    def __wrapper(*args, **kwargs):

        func_info = type(inspect.getcallargs(
                         func, *args, **kwargs).get('self'))
        log.critical('Method(%s.%s) start execute'
                     % (func_info, func.__name__))
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
        except Exception, e:
            log.error('Method(%s.%s) exec error, reason = %s'
                      % (func_info, func.__name__, e))
            return request_result(601)

        exec_time = time.time() - start_time
        log.critical('Method(%s.%s) end execute, execute_time = %f'
                     % (func_info, func.__name__, exec_time))

        return result

    return __wrapper


def func_time_log(func):

    def __wrapper(*args, **kwargs):

        log.critical('Function(%s) start execute' % (func.__name__))
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
        except Exception, e:
            log.error('Function(%s) exec error, reason = %s'
                      % (func.__name__, e))
            return request_result(601)

        exec_time = time.time() - start_time
        log.critical('Function(%s) end execute, execute_time = %f'
                     % (func.__name__, exec_time))

        return result

    return __wrapper
