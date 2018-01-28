#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/17 14:43
"""


class AlipayException(Exception):
    '''Base Alipay Exception'''


class MissingParameter(AlipayException):
    """Raised when the create payment url process is missing some
    parameters needed to continue"""


class ParameterValueError(AlipayException):
    """Raised when parameter value is incorrect"""


class TokenAuthorizationError(AlipayException):
    '''The error occurred when getting token '''