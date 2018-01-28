# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from billing.db.billing_db import BillingDB


class LevelsManager(object):

    def __init__(self):

        self.billing_db = BillingDB()
        self.level_up_exp = conf.level_up_exp

    def level_init(self, team_uuid):

        try:
            self.billing_db.level_init(team_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            return request_result(401)

        result = {
                     "team_uuid": team_uuid
                 }

        return request_result(0, result)

    def level_up(self, level, now_exp, up_exp, add_exp):

        now_exp = int(now_exp)
        up_exp = int(up_exp)
        add_exp = int(add_exp)

        if add_exp >= up_exp:
            add_exp = add_exp - up_exp
            level += 1
            level_up_exp = self.level_up_exp.get(level)
            if add_exp < level_up_exp:
                now_exp = add_exp
                up_exp = level_up_exp - now_exp
            else:
                now_exp = level_up_exp
                up_exp = 0
                add_exp = add_exp - level_up_exp
                return self.level_up(level, now_exp,
                                     up_exp, add_exp)
        else:
            up_exp = up_exp - add_exp
            now_exp = now_exp + add_exp

        return (level, now_exp, up_exp)

    def level_update(self, team_uuid, add_exp):

        try:
            level_info = self.billing_db.level_info(team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)


        level = level_info[0][0]
        now_exp = level_info[0][1]
        up_exp = level_info[0][2]

        level_up_result = self.level_up(level, now_exp,
                                        up_exp, add_exp)
        level = level_up_result[0]
        now_exp = level_up_result[1]
        up_exp = level_up_result[2]

        try:
            self.billing_db.level_update(
                 team_uuid, level, now_exp, up_exp)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "team_uuid": team_uuid,
                     "level": level,
                     "now_exp": now_exp,
                     "up_exp": up_exp
                 }

        return request_result(0, result)

    def level_info(self, team_uuid):

        try:
            level_info = self.billing_db.level_info(team_uuid)
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        level = level_info[0][0]
        experience = level_info[0][1]
        up_required = level_info[0][2]
        create_time = level_info[0][3]
        update_time = level_info[0][4]

        result = {
                     "team_uuid": team_uuid,
                     "level": level,
                     "experience": experience,
                     "up_required": up_required,
                     "create_time": create_time,
                     "update_time": update_time
                 }

        result = json.dumps(result, cls=CJsonEncoder)
        result = json.loads(result)

        return request_result(0, result)
