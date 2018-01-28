# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.mysql_base import MysqlInit
from common.logs import logging as log


class SecurityDB(MysqlInit):

    def __init__(self):

        super(SecurityDB, self).__init__()

    def operation_create(self, record_uuid, user_uuid,
                         user_name, source_ip, resource_uuid,
                         resource_name, resource_type, action):

        sql = "insert into operation_records(record_uuid, user_uuid, \
               user_name, source_ip, resource_uuid, resource_name, \
               resource_type, action, return_code, return_msg, \
               start_time, end_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
               999, 'executing', now(), now())" \
              % (record_uuid, user_uuid, user_name, source_ip,
                 resource_uuid, resource_name, resource_type,
                 action)

        return super(SecurityDB, self).exec_update_sql(sql)

    def operation_list(self, start_time, end_time, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select user_uuid, user_name, source_ip, \
                  resource_uuid, resource_name, resource_type, \
                  action, return_code, return_msg, \
                  start_time, end_time \
                  from operation_records \
                  where start_time between '%s' and '%s' \
                  order by start_time desc \
                  limit %d,%d" \
                 % (start_time, end_time,
                    start_position, page_size)

        sql_02 = "select count(*) from operation_records \
                  where start_time between '%s' and '%s'" \
                 % (start_time, end_time)

        operations_list = super(SecurityDB, self).exec_select_sql(sql_01)
        count = super(SecurityDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "operations_list": operations_list,
                   "count": count
               }

    def operation_info(self, user_uuid, start_time, end_time):

        sql = "select user_name, source_ip, \
               resource_uuid, resource_name, resource_type, \
               action, return_code, return_msg, \
               start_time, end_time \
               from operation_records \
               where user_uuid='%s' \
               and start_time between '%s' and '%s' \
               order by start_time asc" \
              % (user_uuid, start_time, end_time)

        return super(SecurityDB, self).exec_select_sql(sql)

    def operation_update(self, record_uuid,
                         return_code, return_msg,
                         resource_uuid, resource_name):

        if resource_uuid:
            sql = "update operation_records set resource_uuid='%s', \
                   return_code=%d, return_msg='%s', end_time=now() \
                   where record_uuid='%s'" \
                  % (resource_uuid, return_code,
                     return_msg, record_uuid)
        elif resource_name:
            sql = "update operation_records set resource_name='%s', \
                   return_code=%d, return_msg='%s', end_time=now() \
                   where record_uuid='%s'" \
                  % (resource_name, return_code,
                     return_msg, record_uuid)
        else:
            sql = "update operation_records set return_code=%d, \
                   return_msg='%s', end_time=now() \
                   where record_uuid='%s'" \
                  % (return_code, return_msg, record_uuid)

        return super(SecurityDB, self).exec_update_sql(sql)
