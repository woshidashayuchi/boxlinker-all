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

'''
def rc_data(context):

    log.info("create rc json, the based dict data is: %s" % context)

    namespace = context.get('project_uuid')
    image_name = context.get('image_name')
    image_version = context.get('image_version')
    service_name = context.get('service_name')
    pods_num = context.get('pods_num')
    policy = context.get('policy')
    container = context.get('container')
    env = context.get('env')
    auto_startup = context.get('auto_startup')
    command = context.get('command')

    if int(auto_startup) != 1:
        pods_num = 0
    if int(policy) == 1:
        rc_krud = image_name[20:].replace('/', '_').replace(':', '_')
        pull_policy = 'Always'
    else:
        rc_krud = None
        pull_policy = 'IfNotPresent'

    add_rc = {
               "kind": "ReplicationController", "apiVersion": "v1",
               "metadata": {
                  "namespace": namespace, "name": service_name,
                  "labels": {
                     "component": service_name, "rc-krud": rc_krud, "name": service_name
                  }
               },
               "spec": {
                  "replicas": pods_num,
                  "selector": {"name": service_name},
                  "template": {
                     "metadata": {
                        "labels": {
                           "component": service_name, "name": service_name, "logs": service_name
                        }
                     },
                     "spec": {
                        "nodeSelector": {"role": "user"},
                        "containers": [
                           {
                                "name": service_name, "image": image_name+":"+image_version,
                                "imagePullPolicy": pull_policy, "command": command,
                                "ports": ArrayIterator.container(container), "env": ArrayIterator.env(env),
                                "volumeMounts": volume.fill_containerfor_volume(context)
                           }
                        ],
                        "volumes": volumes
                     }
                  }
               },
            }

    return add_rc
'''


def parameter_check(parameter, ptype='pstr', exist='yes'):

    if (parameter is None) and (exist == 'no'):
        return parameter
    elif (parameter is None) and (exist == 'yes'):
        raise(Exception('Parameter is not allowed to be None'))

    para_format = {
        "pstr": "[A-Za-z0-9-_]{1,60}$",
        "pnam": "[A-Za-z]{1,30}[A-Za-z0-9-_]{0,10}$",
        "pint": "-{0,1}[0-9]{1,16}$",
        "pflt": "-{0,1}[0-9]{1,15}[.]{0,1}[0-9]{1,6}$",
        "peml": ("[A-Za-z]{1,1}[A-Za-z0-9-_]{2,30}"
                 "@[A-Za-z0-9]{1,1}[A-Za-z0-9-_.]{1,20}"
                 "[.]{1,1}[A-Za-z]{1,5}$"),
        "ppwd": ".{5,60}"
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
