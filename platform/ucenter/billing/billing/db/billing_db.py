# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


from common.mysql_base import MysqlInit
from common.logs import logging as log


class BillingDB(MysqlInit):

    def __init__(self):

        super(BillingDB, self).__init__()

    def resource_insert(self, resource_uuid, resource_name,
                        resource_type, resource_conf, resource_status,
                        user_uuid, team_uuid, project_uuid):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', '%s', '0', '%s', '%s', '%s', now(), now())" \
                  % (resource_uuid, resource_type,
                     team_uuid, project_uuid, user_uuid)

        sql_02 = "insert into resources(resource_uuid, resource_name, \
                  resource_conf, resource_status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', now(), now())" \
                  % (resource_uuid, resource_name,
                     resource_conf, resource_status)

        return super(BillingDB, self).exec_update_sql(sql_01, sql_02)

    def resource_delete(self, resource_uuid):

        sql = "update resources set resource_status='delete', update_time=now() \
               where resource_uuid='%s'" \
              % (resource_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def resource_update(self, resource_uuid, resource_conf=None,
                        resource_status=None, user_uuid=None,
                        team_uuid=None, project_uuid=None):

        sql_01 = "update resources set resource_conf='%s', update_time=now() \
                  where resource_uuid='%s'" \
                  % (resource_conf, resource_uuid)

        sql_02 = "update resources set resource_status='%s', update_time=now() \
                  where resource_uuid='%s'" \
                  % (resource_status, resource_uuid)

        sql_03 = "update resources_acl set team_uuid='%s', update_time=now() \
                  where resource_uuid='%s'" \
                  % (team_uuid, resource_uuid)

        sql_04 = "update resources_acl set project_uuid='%s', update_time=now() \
                  where resource_uuid='%s'" \
                  % (project_uuid, resource_uuid)

        sql_05 = "update resources_acl set user_uuid='%s', update_time=now() \
                  where resource_uuid='%s'" \
                  % (user_uuid, resource_uuid)

        if resource_conf is not None:
            super(BillingDB, self).exec_update_sql(sql_01)

        if resource_status is not None:
            super(BillingDB, self).exec_update_sql(sql_02)

        if team_uuid is not None:
            super(BillingDB, self).exec_update_sql(sql_03)

        if project_uuid is not None:
            super(BillingDB, self).exec_update_sql(sql_04)

        if user_uuid is not None:
            super(BillingDB, self).exec_update_sql(sql_05)

        return

    def resource_list(self, team_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.resource_uuid, a.resource_type, \
                  a.team_uuid, a.project_uuid, a.user_uuid, \
                  a.create_time, a.update_time, \
                  b.resource_name, b.resource_conf, b.resource_status \
                  from resources_acl a join resources b \
                  where a.resource_uuid=b.resource_uuid \
                  and a.team_uuid='%s' and b.resource_status!='delete' \
                  limit %d,%d" \
                 % (team_uuid, start_position, page_size)

        sql_02 = "select count(*) from resources_acl a join resources b \
                  where a.resource_uuid=b.resource_uuid \
                  and a.team_uuid='%s' and b.resource_status!='delete'" \
                 % (team_uuid)

        db_resource_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "resource_list": db_resource_list,
                   "count": count
               }

    def resources_add_list(self):

        sql = "select resource_uuid from resources \
               where create_time>=date_sub(now(), interval 24 hour)"

        return super(BillingDB, self).exec_select_sql(sql)

    def resources_delete_list(self):

        sql = "select resource_uuid from resources \
               where resource_status='delete' \
               and update_time>=date_sub(now(), interval 24 hour)"

        return super(BillingDB, self).exec_select_sql(sql)

    def resources_update_list(self):

        sql = "select a.resource_uuid, a.resource_name, \
               a.resource_conf, a.resource_status, \
               b.team_uuid, b.project_uuid, b.user_uuid \
               from resources a join resources_acl b \
               where a.resource_uuid=b.resource_uuid \
               and a.resource_status!='delete' \
               and a.update_time>=date_sub(now(), interval 24 hour)"

        return super(BillingDB, self).exec_select_sql(sql)

    def resources_list(self):

        sql = "select a.resource_uuid, a.resource_type, \
               a.team_uuid, a.project_uuid, a.user_uuid, \
               b.resource_conf, b.resource_status \
               from resources_acl a join resources b \
               where a.resource_uuid=b.resource_uuid \
               and b.resource_status!='delete'"

        return super(BillingDB, self).exec_select_sql(sql)

    def voucher_insert(self, voucher_uuid, user_uuid,
                       denomination, invalid_time):

        denomination = int(denomination)
        sql = "insert into vouchers(vouchers_uuid, createuser_uuid, \
               denomination, balance, active_time, invalid_time, \
               status, create_time, update_time) \
               values('%s', '%s', '%d', '%d', 0, '%s', 'unused', now(), now())" \
               % (voucher_uuid, user_uuid, denomination,
                  denomination, invalid_time)

        return super(BillingDB, self).exec_update_sql(sql)

    def voucher_uuid_check(self, voucher_uuid):

        sql = "select count(*) from vouchers \
               where vouchers_uuid='%s' and status='unactive'" \
              % (voucher_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def voucher_active(self, voucher_uuid, user_uuid,
                       team_uuid, project_uuid, activator):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'voucher', '0', '%s', '%s', '%s', now(), now())" \
                  % (voucher_uuid, team_uuid, project_uuid, user_uuid)

        sql_02 = "update vouchers set active_time=now(), status='active', \
                  activator='%s' where vouchers_uuid='%s'" \
                  % (activator, voucher_uuid)

        return super(BillingDB, self).exec_update_sql(sql_01, sql_02)

    def voucher_check(self, team_uuid, amount):

        amount = float(amount)
        sql = "select a.vouchers_uuid from vouchers a join resources_acl b \
               where a.vouchers_uuid=b.resource_uuid  \
               and a.status='active' and a.invalid_time >= now() \
               and a.balance >= %f \
               and b.team_uuid='%s' \
               order by a.invalid_time asc limit 1" \
               % (amount, team_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def voucher_distribute(self, voucher_uuid, accepter):

        sql = "update vouchers set status='unactive', accepter='%s' \
               where vouchers_uuid='%s' and status='unused'" \
              % (accepter, voucher_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def voucher_update(self, voucher_uuid, amount):

        amount = float(amount)
        sql = "update vouchers set balance=balance - %f, update_time=now() \
               where vouchers_uuid='%s' \
               and \
               (create_time=update_time \
                or update_time<=date_sub(now(), interval 1 hour))" \
              % (amount, voucher_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def voucher_status(self, voucher_uuid):

        sql = "select status from vouchers where vouchers_uuid='%s'" \
              % (voucher_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def voucher_status_update(self):

        sql = "update vouchers set status='expired' \
               where invalid_time < now() and status!='expired'"

        return super(BillingDB, self).exec_update_sql(sql)

    def voucher_list_admin(self, user_uuid,
                           start_time, end_time,
                           page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.vouchers_uuid, a.denomination, a.balance, \
                  a.active_time, a.invalid_time, a.status, \
                  a.accepter, a.activator, a.create_time, \
                  a.update_time, b.team_uuid \
                  from vouchers a left join resources_acl b \
                  on a.vouchers_uuid=b.resource_uuid \
                  where a.createuser_uuid='%s' \
                  and a.create_time between '%s' and '%s' \
                  limit %d,%d" \
                 % (user_uuid, start_time, end_time,
                    start_position, page_size)

        sql_02 = "select count(*) from vouchers where createuser_uuid='%s' \
                  and create_time between '%s' and '%s'" \
                 % (user_uuid, start_time, end_time)

        vouchers_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "vouchers_list": vouchers_list,
                   "count": count
               }

    def voucher_list_user(self, team_uuid,
                          start_time, end_time,
                          page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.resource_uuid, a.user_uuid, \
                  b.denomination, b.balance, b.active_time, \
                  b.invalid_time, b.status \
                  from resources_acl a join vouchers b \
                  where a.resource_uuid=b.vouchers_uuid \
                  and a.team_uuid='%s' \
                  and b.create_time between '%s' and '%s' \
                  limit %d,%d" \
                 % (team_uuid, start_time, end_time,
                    start_position, page_size)

        sql_02 = "select count(*) from resources_acl a join vouchers b \
                  where a.resource_uuid=b.vouchers_uuid \
                  and a.team_uuid='%s' \
                  and b.create_time between '%s' and '%s'" \
                 % (team_uuid, start_time, end_time)

        vouchers_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "vouchers_list": vouchers_list,
                   "count": count
               }

    def voucher_list_accept(self, user_name, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select vouchers_uuid, denomination, \
                  invalid_time, status \
                  from vouchers where accepter='%s' \
                  and invalid_time >= now() \
                  limit %d,%d" \
                 % (user_name, start_position, page_size)

        sql_02 = "select count(*) from vouchers where accepter='%s' \
                  and invalid_time >= now()" \
                 % (user_name)

        vouchers_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "vouchers_list": vouchers_list,
                   "count": count
               }

    def level_init(self, team_uuid):

        sql = "insert into levels(team_uuid, level, \
               experience, up_required, create_time, update_time) \
               values('%s', 1, 0, 100, now(), now())" \
               % (team_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def level_info(self, team_uuid):

        sql = "select level, experience, up_required, \
               create_time, update_time \
               from levels where team_uuid='%s'" \
               % (team_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def level_update(self, team_uuid, level,
                     experience, up_required):

        sql = "update levels set level=%d, experience=%d, \
               up_required=%d, update_time=now() \
               where team_uuid='%s'" \
               % (level, experience, up_required, team_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def balance_init(self, team_uuid, balance):

        sql = "insert into balances(team_uuid, total, balance, \
               create_time, update_time) \
               values('%s', 0, %d, now(), now())" \
               % (team_uuid, int(balance))

        return super(BillingDB, self).exec_update_sql(sql)

    def balance_update(self, team_uuid, amount):

        sql_01 = "update balances set total=total + %d, balance=balance + %f \
                  where team_uuid='%s'" \
                 % (int(amount), float(amount), team_uuid)

        sql_02 = "update balances set balance=balance + %f, update_time=now() \
                  where team_uuid='%s' \
                  and \
                  (create_time=update_time \
                   or update_time<=date_sub(now(), interval 1 hour))" \
                 % (float(amount), team_uuid)

        if float(amount) >= 0:
            return super(BillingDB, self).exec_update_sql(sql_01)
        else:
            return super(BillingDB, self).exec_update_sql(sql_02)

    def balance_info(self, team_uuid):

        sql = "select balance, update_time \
               from balances where team_uuid='%s'" \
               % (team_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def balance_check(self):

        sql = "select team_uuid, balance from balances \
               where balance<=0 \
               and update_time>=date_sub(now(), interval 24 hour)"

        return super(BillingDB, self).exec_select_sql(sql)

    def recharge_create(self, recharge_uuid, recharge_amount,
                        recharge_type, team_uuid, recharge_user):

        sql = "insert into recharge_records(recharge_uuid, recharge_amount, \
               recharge_type, team_uuid, user_name, create_time) \
               values('%s', %d, '%s', '%s', '%s', now())" \
               % (recharge_uuid, int(recharge_amount), recharge_type,
                  team_uuid, recharge_user)

        return super(BillingDB, self).exec_update_sql(sql)

    def recharge_info(self, recharge_uuid, team_uuid):

        sql = "select recharge_amount, recharge_type, \
               user_name, create_time from recharge_records \
               where recharge_uuid='%s' and team_uuid='%s'" \
              % (recharge_uuid, team_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def recharge_list(self, team_uuid,
                      start_time, end_time,
                      page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select recharge_uuid, recharge_amount, \
                  recharge_type, user_name, create_time \
                  from recharge_records where team_uuid='%s' \
                  and create_time between '%s' and '%s' \
                  limit %d,%d" \
                 % (team_uuid, start_time, end_time,
                    start_position, page_size)

        sql_02 = "select count(*) from recharge_records \
                  where team_uuid='%s' \
                  and create_time between '%s' and '%s'" \
                 % (team_uuid, start_time, end_time)

        db_recharge_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "recharge_list": db_recharge_list,
                   "count": count
               }

    def recharge_check_list(self, recharge_type,
                            start_time, end_time,
                            page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        if recharge_type == 'all':
            sql_01 = "select recharge_uuid, recharge_amount, \
                      recharge_type, team_uuid, user_name, create_time \
                      from recharge_records \
                      where create_time between '%s' and '%s' \
                      limit %d,%d" \
                     % (start_time, end_time,
                        start_position, page_size)

            sql_02 = "select count(*) from recharge_records \
                      where create_time between '%s' and '%s'" \
                     % (start_time, end_time)
        else:
            sql_01 = "select recharge_uuid, recharge_amount, \
                      recharge_type, team_uuid, user_name, create_time \
                      from recharge_records where recharge_type='%s' \
                      and create_time between '%s' and '%s' \
                      limit %d,%d" \
                     % (recharge_type, start_time, end_time,
                        start_position, page_size)

            sql_02 = "select count(*) from recharge_records \
                      where recharge_type='%s' \
                      and create_time between '%s' and '%s'" \
                     % (recharge_type, start_time, end_time)

        db_recharge_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "recharge_list": db_recharge_list,
                   "count": count
               }

    def recharge_check_total(self, recharge_type,
                             start_time, end_time):

        if recharge_type == 'all':
            sql = "select sum(recharge_amount) from recharge_records \
                   where create_time between '%s' and '%s'" \
                  % (start_time, end_time)
        else:
            sql = "select sum(recharge_amount) from recharge_records \
                   where recharge_type='%s' \
                   and create_time between '%s' and '%s'" \
                  % (recharge_type, start_time, end_time)

        return super(BillingDB, self).exec_select_sql(sql)

    def limit_info(self, team_uuid, resource_type):

        sql = "select a.%s from limits a join levels b \
               where a.team_level=b.level and b.team_uuid='%s'" \
               % (resource_type, team_uuid)

        return super(BillingDB, self).exec_select_sql(sql)

    def limit_list(self, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select team_level, teams, teamusers, \
                  projects, projectusers, roles, images, \
                  services, volumes, create_time, update_time \
                  from limits \
                  limit %d,%d" \
                 % (start_position, page_size)

        sql_02 = "select count(*) from limits"

        db_limit_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "limits_list": db_limit_list,
                   "count": count
               }

    def limit_update(self, team_level, resource_type, limit):

        sql = "update limits set %s=%d, update_time=now() \
               where team_level='%s'" \
               % (resource_type, int(limit), team_level)

        return super(BillingDB, self).exec_update_sql(sql)

    def bill_insert(self, user_uuid, team_uuid, project_uuid,
                    resource_uuid, resource_cost, voucher_cost):

        # sql = "insert into bills(resource_uuid, resource_cost, voucher_cost, \
        #       team_uuid, project_uuid, user_uuid, insert_time) \
        #       values('%s', '%f', '%f', '%s', '%s', '%s', now())" \
        #       % (resource_uuid, float(resource_cost), float(voucher_cost),
        #          team_uuid, project_uuid, user_uuid)

        sql = "INSERT into bills \
               SELECT NULL, '%s', '%f', '%f', '%s', '%s', '%s', now() \
               FROM dual WHERE NOT EXISTS \
               (SELECT resource_uuid FROM bills \
                WHERE resource_uuid='%s' \
                and insert_time>date_sub(now(), interval 1 hour))" \
              % (resource_uuid, float(resource_cost), float(voucher_cost),
                 team_uuid, project_uuid, user_uuid, resource_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def bill_list(self, team_uuid,
                  start_time, end_time,
                  page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        # sql_01 = "select a.resource_uuid, a.resource_name, \
        #          a.resource_conf, a.resource_status, \
        #          b.resource_type, b.team_uuid, b.project_uuid, b.user_uuid, \
        #          round(sum(c.resource_cost), 2), round(sum(c.voucher_cost), 2) \
        #          from resources a join resources_acl b join bills_days c \
        #          where a.resource_uuid=b.resource_uuid \
        #          and b.resource_uuid = c.resource_uuid \
        #          and c.team_uuid='%s' \
        #          and c.insert_time between '%s' and '%s' \
        #          group by a.resource_uuid \
        #          limit %d,%d" \
        #         % (team_uuid, start_time, end_time,
        #            start_position, page_size)

        sql_01 = "select t.resource_uuid, t.resource_name, \
                  t.resource_conf, t.resource_status, \
                  t.resource_type, t.team_uuid, t.project_uuid, t.user_uuid, \
                  sum(t.resource_cost), sum(t.voucher_cost) \
                  from(select a.resource_uuid resource_uuid, \
                       a.resource_name resource_name, \
                       a.resource_conf resource_conf, \
                       a.resource_status resource_status, \
                       b.resource_type resource_type, \
                       b.team_uuid team_uuid, b.project_uuid \
                       project_uuid, b.user_uuid user_uuid, \
                       c.resource_cost resource_cost, \
                       c.voucher_cost voucher_cost \
                       from resources a join resources_acl b join bills_days c \
                       where a.resource_uuid=b.resource_uuid \
                       and b.resource_uuid = c.resource_uuid \
                       and c.team_uuid='%s' \
                       and c.insert_time between '%s' and '%s' \
                       union all \
                       select a.resource_uuid resource_uuid, \
                       a.resource_name resource_name, \
                       a.resource_conf resource_conf, \
                       a.resource_status resource_status, \
                       b.resource_type resource_type, \
                       b.team_uuid team_uuid, b.project_uuid \
                       project_uuid, b.user_uuid user_uuid, \
                       c.resource_cost resource_cost, c.voucher_cost voucher_cost \
                       from resources a join resources_acl b join bills c \
                       where a.resource_uuid=b.resource_uuid \
                       and b.resource_uuid = c.resource_uuid \
                       and c.team_uuid='%s' \
                       and c.insert_time between '%s' and '%s' \
                  ) t group by t.resource_uuid limit %d,%d" \
                 % (team_uuid, start_time, end_time,
                    team_uuid, start_time, end_time,
                    start_position, page_size)

        # sql_02 = "select count(*) from (select * from bills_days where team_uuid='%s' \
        #          and insert_time between '%s' and '%s' group by resource_uuid) t" \
        #         % (team_uuid, start_time, end_time)

        sql_02 = "select count(*) from ( \
                      select t.resource_uuid \
                      from(select resource_uuid from bills_days where team_uuid='%s' \
                           and insert_time between '%s' and '%s' \
                           union all \
                           select resource_uuid from bills where team_uuid='%s' \
                           and insert_time between '%s' and '%s' \
                          ) t group by t.resource_uuid \
                      ) t" \
                 % (team_uuid, start_time, end_time,
                    team_uuid, start_time, end_time)

        db_bills_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "bills_list": db_bills_list,
                   "count": count
               }

    def bill_total(self, team_uuid, start_time, end_time):

        # sql = "select round(sum(resource_cost), 2), round(sum(voucher_cost), 2) \
        #        from bills_days where team_uuid='%s' \
        #        and insert_time between '%s' and '%s'" \
        #       % (team_uuid, start_time, end_time)

        sql = "select sum(t.resource_cost), sum(t.voucher_cost) \
               from( \
               select sum(a.resource_cost) resource_cost, \
               sum(a.voucher_cost) voucher_cost \
               from bills_days a \
               where a.team_uuid='%s' \
               and a.insert_time between '%s' and '%s' \
               union all \
               select sum(b.resource_cost) , sum(b.voucher_cost) \
               from bills b \
               where b.team_uuid='%s' \
               and b.insert_time between '%s' and '%s' \
               ) t" \
              % (team_uuid, start_time, end_time,
                 team_uuid, start_time, end_time)

        return super(BillingDB, self).exec_select_sql(sql)

    def bill_resource(self, start_time, end_time):

        sql = "select distinct(resource_uuid) from bills \
               where insert_time between '%s' and '%s'" \
              % (start_time, end_time)

        return super(BillingDB, self).exec_select_sql(sql)

    def bills_merge(self, resource_uuid, start_time, end_time):

        # "查询插入, 插入时间等于当前时间减去24小时"
        sql_01 = "insert into bills_days(resource_uuid, resource_cost, \
                  voucher_cost, team_uuid, project_uuid, user_uuid, insert_time) \
                  select resource_uuid, round(sum(resource_cost), 2), \
                  round(sum(voucher_cost), 2), team_uuid, project_uuid, \
                  user_uuid, insert_time from bills where resource_uuid='%s' \
                  and insert_time between '%s' and '%s'" \
                 % (resource_uuid, start_time, end_time)

        sql_02 = "delete from bills where resource_uuid='%s' \
                  and insert_time between '%s' and '%s'" \
                 % (resource_uuid, start_time, end_time)

        return super(BillingDB, self).exec_update_sql(sql_01, sql_02)

    def bills_cost(self):

        sql = "select team_uuid, round(sum(resource_cost), 5) \
               from bills where insert_time>date_sub(now(), interval 1 hour) \
               group by team_uuid"

        return super(BillingDB, self).exec_select_sql(sql)

    def order_insert(self, user_uuid, team_uuid, project_uuid,
                     order_uuid, resource_uuid, cost, status):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'order', '0', '%s', '%s', '%s', now(), now())" \
                  % (order_uuid, team_uuid, project_uuid, user_uuid)

        sql_02 = "insert into orders(orders_uuid, resource_uuid, \
                  cost, status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', now(), now())" \
                  % (order_uuid, resource_uuid, cost, status)

        return super(BillingDB, self).exec_update_sql(sql_01, sql_02)

    def order_update_cost(self, order_uuid, cost):

        sql = "update orders set cost='%s', update_time=now() \
               where orders_uuid='%s'" \
               % (cost, order_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def order_update_status(self, order_uuid, status):

        sql = "update orders set status='%s', update_time=now() \
               where orders_uuid='%s'" \
               % (status, order_uuid)

        return super(BillingDB, self).exec_update_sql(sql)

    def order_list(self, team_uuid,
                   start_time, end_time,
                   page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.team_uuid, a.project_uuid, a.user_uuid, \
                  b.orders_uuid, b.resource_uuid, b.cost, b.status, \
                  b.create_time, b.update_time \
                  from resources_acl a join orders b \
                  where a.resource_uuid=b.orders_uuid \
                  and a.team_uuid='%s' and b.create_time between '%s' and '%s' \
                  limit %d,%d" \
                 % (team_uuid, start_time, end_time,
                    start_position, page_size)

        sql_02 = "select count(*) from resources_acl a join orders b \
                  where a.resource_uuid=b.orders_uuid \
                  and a.team_uuid='%s' and b.create_time between '%s' and '%s'" \
                 % (team_uuid, start_time, end_time)

        user_orders_list = super(BillingDB, self).exec_select_sql(sql_01)
        count = super(BillingDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "orders_list": user_orders_list,
                   "count": count
               }
