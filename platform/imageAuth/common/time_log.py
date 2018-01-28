# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


import time
import inspect

from common.logs import logging as log
from common.code import request_result


def time_log(func):

    def __wrapper(*args, **kwargs):

        func_info = inspect.getcallargs(func, *args, **kwargs)
        log.info('function(%s.%s) start execute' % (func_info, func.__name__))

        start_time = time.time()

        try:
            result = func(*args, **kwargs)
        except Exception, e:
            log.error('function(%s.%s) exec error, reason = %s'
                      % (func_info, func.__name__, e))
            return request_result(601)

        end_time = time.time()
        exec_time = end_time - start_time
        log.info('function(%s.%s) end execute, execute_time = %d'
                 % (func_info, func.__name__, exec_time))

        return result

    return __wrapper
