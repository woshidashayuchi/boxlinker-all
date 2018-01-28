# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import time
import inspect

from common.logs import logging as log
from common.code import request_result
from common.local_cache import LocalCache
from common.token_ucenterauth import token_auth
from common.db import auth_db

caches = LocalCache(1000)


def role_check(action, privilege):

    try:
        if ((action == 'create') and ('C' in privilege)):
            return 0
        elif ((action == 'delete') and ('D' in privilege)):
            return 0
        elif ((action == 'update') and ('U' in privilege)):
            return 0
        elif ((action == 'read') and ('R' in privilege)):
            return 0
        else:
            return 1
    except Exception, e:
        log.warning('Role check error, reason=%s' % (e))
        return 1


class AuthManager(object):

    def __init__(self):

        self.auth_db = auth_db.AuthDB()

    def resource_acl_check(self, user_uuid,
                           team_uuid, team_priv,
                           project_uuid, project_priv,
                           resource_uuid, action):

        try:
            if (self.auth_db.user_acl_check(resource_uuid)
                    in ('global', user_uuid)):
                return 0
        except Exception:
            return 1

        if (role_check(action, project_priv) == 0):
            try:
                if (self.auth_db.project_acl_check(resource_uuid)
                        in ('global', project_uuid)):
                    return 0
            except Exception:
                return 1

        if (role_check(action, team_priv) == 0):
            try:
                if (self.auth_db.team_acl_check(resource_uuid)
                        in ('global', team_uuid)):
                    return 0
            except Exception:
                return 1

        if (user_uuid == 'sysadmin'):
            try:
                if (self.auth_db.admin_acl_check(resource_uuid)
                        in ('global', user_uuid)):
                    return 0
            except Exception:
                return 1

        return 1


def acl_check(func):

    def _aclauth(*args, **kwargs):

        func_args = inspect.getcallargs(func, *args, **kwargs)
        context = func_args.get('context')

        token = context['token']
        resource_uuid = context['resource_uuid']
        action = context['action']

        user_info = token_auth(token)['result']
        user_uuid = user_info['user_uuid']
        team_uuid = user_info['team_uuid']
        team_priv = user_info['team_priv']
        project_uuid = user_info['project_uuid']
        project_priv = user_info['project_priv']

        context = "%s%s%s%s%s%s%s" % (user_uuid, team_uuid, team_priv,
                                      project_uuid, project_priv,
                                      resource_uuid, action)

        log.debug('start ack check, context=%s' % (context))
        acl_info = caches.get(context)
        if (acl_info is LocalCache.notFound):
            log.debug('Cache acl not hit, context=%s' % (context))
            auth_manager = AuthManager()
            ret = auth_manager.resource_acl_check(
                               user_uuid, team_uuid, team_priv,
                               project_uuid, project_priv,
                               resource_uuid, action)
            expire = int(time.time()) + 300
            caches.set(context, {"acl_check": ret, "expire": expire})
            log.debug('Cached acl check, context=%s' % (context))
        else:
            log.debug('Cache acl hit, context=%s' % (context))
            ret = acl_info['acl_check']

        log.debug('ack check result=%s' % (ret))

        if ret == 0:
            try:
                return func(*args, **kwargs)
            except Exception, e:
                log.error('function(%s) exec error, reason = %s'
                          % (func.__name__, e))
                return request_result(601)
        else:
            log.warning('Resource acl auth denied: user_uuid = %s, \
                         team_uuid=%s, team_priv=%s, project_uuid=%s, \
                         project_priv=%s, resource_uuid=%s, action=%s'
                        % (user_uuid, team_uuid, team_priv,
                           project_uuid, project_priv,
                           resource_uuid, action))

            return request_result(202)

    try:
        return _aclauth
    except Exception, e:
        log.error('Acl check error, reason=%s' % (e))
        return request_result(202)
