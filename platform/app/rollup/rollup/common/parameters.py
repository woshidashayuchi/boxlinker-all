# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import sys
import re
from common.logs import logging as log


def context_data(token=None, resource_uuid=None, action=None):

    return {
               "token": token,
               "resource_uuid": resource_uuid,
               "action": action
           }


def rpc_data(api, context, parameters):

    return {
               "api": api,
               "context": context,
               "parameters": parameters
           }


def parameter_check(parameter, ptype='pstr', exist='yes'):

    if (parameter is None or parameter == '') and (exist == 'no'):
        return parameter
    elif (parameter is None or parameter == '') and (exist == 'yes'):
        raise(Exception('Parameter is not allowed to be None'))

    para_format = {
        "pstr": "[A-Za-z0-9-_]{1,60}$",
        "pnam": "[A-Za-z]{1}[A-Za-z0-9-_]{4,19}$",
        "pint": "-{0,1}[0-9]{1,16}$",
        "pflt": "-{0,1}[0-9]{1,15}[.]{0,1}[0-9]{1,6}$",
        "peml": ("[A-Za-z1-9]{1,1}[A-Za-z0-9-_]{2,30}"
                 "@[A-Za-z0-9]{1,1}[A-Za-z0-9-_.]{1,20}"
                 "[.]{1,1}[A-Za-z]{1,5}$"),
        "puid": ("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-"
                 "[a-z0-9]{4}-[a-z0-9]{12}$"),
        "ppwd": ".{6,60}",
        "pimgid": "^[0-9]*$",
        "choice": "^[01]$",
        "pod_num": "^([0-9]|10)$",
        "command": "^[A-Za-z]{1}[A-Za-z0-9-_@,& ]{1,130}[A-Za-z0-9]{1}$",
        "container_port": "^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
        "domain": "^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)?"
    }
    m = re.match(para_format[ptype], str(parameter))
    if m is None:
        log.warning('Parameter format error, parameter=%s, ptype=%s, exist=%s'
                    % (str(parameter), ptype, exist))
        raise(Exception('Parameter format error'))

    return parameter

if __name__ == "__main__":

    parameter = sys.argv[1]
    ptype = sys.argv[2]
    exist = sys.argv[3]

    try:
        parameter = parameter_check(parameter, ptype, exist)
        print('parameter check success, parameter=%s' % (parameter))
    except Exception, e:
        print('parameter error, reason=%s' % (e))
