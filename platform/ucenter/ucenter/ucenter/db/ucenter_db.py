# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>


from common.mysql_base import MysqlInit
from common.logs import logging as log


class UcenterDB(MysqlInit):

    def __init__(self):

        super(UcenterDB, self).__init__()

    def name_duplicate_check(self, user_name):

        sql = "select count(*) from \
               (select user_name from users where user_name='%s' \
               union all select team_name from teams where team_name='%s') t" \
               % (user_name, user_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def email_duplicate_check(self, email):

        sql = "select count(*) from users where email='%s'" \
               % (email)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_duplicate_check(self, team_name):

        sql = "select count(*) from teams where team_name='%s'" \
               % (team_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_duplicate_check(self, project_name, project_team):

        sql = "select count(*) from projects \
               where project_name='%s' and project_team='%s'" \
               % (project_name, project_team)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_register(self, user_uuid, user_name,
                      passwd, salt, email, mobile):

        sql = "insert into users_register(user_uuid, user_name, \
               password, salt, email, mobile, status, \
               create_time, update_time) \
               values('%s', '%s', '%s', '%s', '%s', '%s', \
               'unactive', now(), now())" \
              % (user_uuid, user_name, passwd, salt, email, mobile)

        return super(UcenterDB, self).exec_update_sql(sql)

    def register_info(self, user_uuid):

        sql = "select user_name, password, salt, email, mobile, \
               status, create_time, update_time \
               from users_register where user_uuid='%s'" \
               % (user_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def register_check(self, user_name):

        sql = "select status from users_register where user_name='%s'" \
               % (user_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_delete(self, user_uuid):

        sql_01 = "delete from users where user_uuid='%s'" \
                 % (user_uuid)

        sql_02 = "delete from resources_acl where resource_uuid='%s'" \
                 % (user_uuid)

        return super(UcenterDB, self).exec_update_sql(sql_01, sql_02)

    def user_info(self, user_uuid):

        sql = "select user_name, real_name, email, mobile, \
               status, sex, birth_date, create_time, update_time \
               from users where user_uuid='%s' and status!='delete'" \
               % (user_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_name_info(self, user_name):

        sql = "select user_uuid, password, salt, email \
               from users where user_name='%s' and status='enable'" \
               % (user_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_list(self, user_name):

        user_name = user_name + r'%'
        log.debug('user_name=%s' % (user_name))
        sql = "select user_uuid, user_name from users \
               where user_name like '%s' and status='enable' \
               limit 10" \
               % (user_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_list_email(self, email):

        email = r'%' + email + r'%'
        log.debug('email=%s' % (email))
        sql = "select user_uuid, user_name from users \
               where email like '%s' and status='enable' \
               limit 10" \
               % (email)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_update(self, user_uuid, real_name, mobile, sex, birth_date):

        sql = "update users set real_name='%s', mobile='%s', \
               sex='%s', birth_date='%s', update_time=now() \
               where user_uuid='%s'" \
               % (real_name or 'None', mobile or 'None', sex or 'None',
                  birth_date, user_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_activate(self, user_uuid, user_name, passwd, salt,
                      email, mobile, team_uuid, project_uuid, role_uuid):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'user', '%s', '0', '0', '%s', now(), now())" \
                  % (user_uuid, user_uuid, user_uuid)

        sql_02 = "insert into users(user_uuid, user_name, real_name, \
                  password, salt, email, mobile, status, sex, birth_date, \
                  create_time, update_time) \
                  values('%s', '%s', 'None', '%s', '%s', '%s', '%s', \
                  'enable', 'None', 0, now(), now())" \
                  % (user_uuid, user_name, passwd, salt, email, mobile)

        sql_03 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'team', '0', '0', '0', '%s', now(), now())" \
                  % (team_uuid, user_uuid)

        sql_04 = "insert into teams(team_uuid, team_name, team_owner, \
                  team_type, team_desc, status, create_time, update_time) \
                  values('%s', '%s', '%s', 'system', 'user default team', \
                  'enable', now(), now())" \
                  % (team_uuid, user_name, user_uuid)

        sql_05 = "insert into users_teams(user_uuid, team_uuid, \
                  team_role, status, create_time, update_time) \
                  values('%s', '%s', '%s', 'enable', now(), now())" \
                  % (user_uuid, team_uuid, role_uuid)

        sql_06 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'project', '0', '0', '0', '%s', now(), now())" \
                  % (project_uuid, user_uuid)

        sql_07 = "insert into projects(project_uuid, project_name, \
                  project_owner, project_team, project_type, project_desc, \
                  status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', 'system', \
                  'team default project', 'enable', now(), now())" \
                  % (project_uuid, user_name, user_uuid, team_uuid)

        sql_08 = "insert into users_projects(user_uuid, project_uuid, \
                  project_role, status, create_time, update_time) \
                  values('%s', '%s', '%s', 'enable', now(), now())" \
                  % (user_uuid, project_uuid, role_uuid)

        sql_09 = "update users_register set status='active' \
                  where user_uuid='%s'" \
                 % (user_uuid)

        return super(UcenterDB, self).exec_update_sql(
                                      sql_01, sql_02, sql_03,
                                      sql_04, sql_05, sql_06,
                                      sql_07, sql_08, sql_09)

    def user_status_update(self, user_uuid, status):

        sql = "update users set status='%s', update_time=now() \
               where user_uuid='%s'" \
               % (status, user_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def role_create(self, role_uuid, role_name,
                    role_priv, user_uuid, team_uuid):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'role', '0', '%s', '0', '%s', now(), now())" \
                  % (role_uuid, team_uuid, user_uuid)

        sql_02 = "insert into roles(role_uuid, role_name, role_priv, \
                  role_type, status, create_time, update_time) \
                  values('%s', '%s', '%s', 'user', 'enable', now(), now())" \
                  % (role_uuid, role_name, role_priv)

        return super(UcenterDB, self).exec_update_sql(sql_01, sql_02)

    def role_list(self, team_uuid):

        sql = "select a.role_uuid, a.role_name, a.role_priv, \
               a.role_type, a.status, a.create_time, a.update_time \
               from roles a join resources_acl b \
               where a.role_uuid=b.resource_uuid and a.status='enable' \
               and b.team_uuid in ('global', '%s')" \
               % (team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def role_type(self, role_uuid):

        sql = "select role_type from roles where role_uuid='%s'" \
               % (role_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def role_info(self, role_uuid):

        sql = "select role_name, role_priv, role_type, status, \
               create_time, update_time \
               from roles where role_uuid='%s' and status='enable'" \
               % (role_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def role_update(self, role_uuid, role_priv):

        sql = "update roles set role_priv='%s', update_time=now() \
               where role_uuid='%s'" \
               % (role_priv, role_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def role_delete(self, role_uuid):

        sql = "update roles set status='delete', update_time=now() \
               where role_uuid='%s'" \
               % (role_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def password_update(self, user_uuid, passwd, salt):

        sql = "update users set password='%s', salt='%s', update_time=now() \
               where user_uuid='%s'" \
               % (passwd, salt, user_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def email_user_name(self, email):

        sql = "select user_name from users where email='%s'" % (email)

        return super(UcenterDB, self).exec_select_sql(sql)

    def user_token_info(self, user_name):

        sql = "select a.user_uuid, a.password, a.salt, \
               b.team_uuid, c.project_uuid \
               from users a join teams b join projects c \
               where a.user_name='%s' and a.status='enable' \
               and b.team_name='%s' and b.team_owner=a.user_uuid \
               and c.project_name='%s' and c.project_owner=a.user_uuid" \
               % (user_name, user_name, user_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_priv(self, user_uuid, team_uuid):

        sql = "select a.role_priv from roles a join users_teams b \
               where a.role_uuid=b.team_role and b.user_uuid='%s' \
               and b.team_uuid='%s'" \
               % (user_uuid, team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def token_create(self, token, user_uuid, team_uuid, project_uuid):

        sql_01 = "insert into tokens(token, user_uuid, team_uuid, \
                  project_uuid, expiry_time, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', \
                  date_add(now(), interval 1 hour), now(), now())" \
                  % (token, user_uuid, team_uuid, project_uuid)

        sql_02 = "delete from tokens where expiry_time<now()"

        return super(UcenterDB, self).exec_update_sql(sql_01, sql_02)

    def token_check(self, token):

        sql = "select a.user_uuid, a.team_uuid, a.project_uuid, \
               b.user_name from tokens a left join users b \
               on a.user_uuid=b.user_uuid \
               where a.token='%s' and a.expiry_time>=now()" \
               % (token)

        return super(UcenterDB, self).exec_select_sql(sql)

    def token_update(self, token):

        sql = "update tokens set expiry_time=date_add(now(), interval 1 hour), \
               update_time=now() where token='%s'" \
               % (token)

        return super(UcenterDB, self).exec_update_sql(sql)

    def token_delete(self, token):

        sql = "delete from tokens where token='%s'" \
              % (token)

        return super(UcenterDB, self).exec_update_sql(sql)

    def team_create(self, team_uuid, team_name,
                    team_owner, team_desc, project_uuid):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'team', '0', '%s', '0', '%s', now(), now())" \
                  % (team_uuid, team_uuid, team_owner)

        sql_02 = "insert into teams(team_uuid, team_name, team_owner, \
                  team_type, team_desc, status, create_time, update_time) \
                  values('%s', '%s', '%s', 'private', '%s', \
                  'enable', now(), now())" \
                  % (team_uuid, team_name, team_owner, team_desc or 'None')

        sql_03 = "insert into users_teams(user_uuid, team_uuid, \
                  team_role, status, create_time, update_time) \
                  values('%s', '%s', 'owner', 'enable', now(), now())" \
                  % (team_owner, team_uuid)

        sql_04 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'project', '0', '%s', '%s', '%s', now(), now())" \
                  % (project_uuid, team_uuid, project_uuid, team_owner)

        sql_05 = "insert into projects(project_uuid, project_name, \
                  project_owner, project_team, project_type, project_desc, \
                  status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', 'system', \
                  'team default project', 'enable', now(), now())" \
                  % (project_uuid, team_name, team_owner, team_uuid)

        sql_06 = "insert into users_projects(user_uuid, project_uuid, \
                  project_role, status, create_time, update_time) \
                  values('%s', '%s', 'owner', 'enable', now(), now())" \
                  % (team_owner, project_uuid)

        return super(UcenterDB, self).exec_update_sql(
                                      sql_01, sql_02, sql_03,
                                      sql_04, sql_05, sql_06)

    def team_list(self, user_uuid):

        sql = "select a.team_uuid, a.team_name, a.team_owner, \
               a.team_type, a.team_desc, a.status, a.create_time, \
               a.update_time, c.role_name \
               from teams a join users_teams b join roles c \
               where a.team_uuid=b.team_uuid and a.status='enable' \
               and b.user_uuid='%s' and b.team_role=c.role_uuid" \
               % (user_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_type(self, team_uuid):

        sql = "select team_type from teams where team_uuid='%s'" \
               % (team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_info(self, team_uuid):

        sql = "select team_name, team_owner, team_type, team_desc, status, \
               create_time, update_time \
               from teams where team_uuid='%s' and status='enable'" \
               % (team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_info_uuid(self, team_name):

        sql = "select team_uuid, team_name, team_owner \
               from teams where team_name='%s' and status='enable'" \
               % (team_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_info_public(self, team_name):

        sql = "select team_uuid, team_name, team_owner, team_type, \
               team_desc, status, create_time, update_time \
               from teams where team_name='%s' and team_type='public' \
               and status='enable'" \
               % (team_name)

        return super(UcenterDB, self).exec_select_sql(sql)

    def team_update_owner(self, team_uuid, team_owner):

        sql_01 = "update teams set team_owner='%s', update_time=now() \
                  where team_uuid='%s'" \
                  % (team_owner, team_uuid)

        sql_02 = "update users_teams set team_role='user', update_time=now() \
                  where team_uuid='%s' and team_role='owner'" \
                  % (team_uuid)

        sql_03 = "update users_teams set team_role='owner', update_time=now() \
                  where user_uuid='%s' and team_uuid='%s'" \
                  % (team_owner, team_uuid)

        sql_04 = "update resources_acl set user_uuid='%s', update_time=now() \
                  where resource_uuid='%s' and resource_type='team'" \
                  % (team_owner, team_uuid)

        return super(UcenterDB, self).exec_update_sql(
                                      sql_01, sql_02, sql_03, sql_04)

    def team_update_type(self, team_uuid, team_type):

        sql = "update teams set team_type='%s', update_time=now() \
               where team_uuid='%s'" \
               % (team_type, team_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def team_update_desc(self, team_uuid, team_desc):

        sql = "update teams set team_desc='%s', update_time=now() \
               where team_uuid='%s'" \
               % (team_desc, team_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def team_check(self, team_uuid):

        sql = "select count(*) from users_teams where team_uuid='%s'" \
               % (team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)[0][0]

    def team_delete(self, team_uuid):

        sql_01 = "delete a from users_projects a join projects b \
                  using(project_uuid) where b.project_team='%s'" \
                 % (team_uuid)

        sql_02 = "delete from projects where project_team='%s'" \
                 % (team_uuid)

        sql_03 = "delete from users_teams where team_uuid='%s'" \
                 % (team_uuid)

        sql_04 = "delete from teams where team_uuid='%s'" \
                 % (team_uuid)

        sql_05 = "delete from resources_acl where resource_uuid='%s'" \
                 % (team_uuid)

        return super(UcenterDB, self).exec_update_sql(
                                      sql_01, sql_02, sql_03, sql_04, sql_05)

    def project_create(self, project_uuid, project_name,
                       project_owner, project_team, project_desc):

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'project', '0', '%s', '%s', '%s', now(), now())" \
                  % (project_uuid, project_team, project_uuid, project_owner)

        sql_02 = "insert into projects(project_uuid, project_name, \
                  project_owner, project_team, project_type, project_desc, \
                  status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', 'private', '%s', \
                  'enable', now(), now())" \
                  % (project_uuid, project_name, project_owner,
                     project_team, project_desc or 'None')

        sql_03 = "insert into users_projects(user_uuid, project_uuid, \
                  project_role, status, create_time, update_time) \
                  values('%s', '%s', 'owner', 'enable', now(), now())" \
                  % (project_owner, project_uuid)

        return super(UcenterDB, self).exec_update_sql(sql_01, sql_02, sql_03)

    def project_list(self, user_uuid, team_uuid):

        sql = "select a.project_uuid, a.project_name, a.project_owner, \
               a.project_team, a.project_type, a.project_desc, a.status, \
               a.create_time, a.update_time, c.role_name \
               from projects a join users_projects b join roles c \
               where a.project_uuid=b.project_uuid and a.project_team='%s' \
               and a.status='enable' and b.user_uuid='%s' \
               and b.project_role=c.role_uuid" \
               % (team_uuid, user_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_type(self, project_uuid):

        sql = "select project_type from projects where project_uuid='%s'" \
               % (project_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_default(self, team_uuid):

        sql = "select project_uuid from projects \
               where project_team='%s' and project_type='system'" \
               % (team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_info(self, project_uuid):

        sql = "select project_name, project_owner, project_team, \
               project_type, project_desc, status, create_time, update_time \
               from projects where project_uuid='%s' and status='enable'" \
               % (project_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_priv(self, user_uuid, project_uuid):

        sql = "select a.role_priv from roles a join users_projects b \
               where a.role_uuid=b.project_role and b.user_uuid='%s' \
               and b.project_uuid='%s'" \
               % (user_uuid, project_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_team_check(self, project_uuid, team_uuid):

        sql = "select count(*) from projects \
               where project_uuid='%s' and project_team='%s'" \
               % (project_uuid, team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)

    def project_update_owner(self, project_uuid, project_owner):

        sql_01 = "update projects set project_owner='%s', update_time=now() \
                  where project_uuid='%s'" \
                  % (project_owner, project_uuid)

        sql_02 = "update users_projects set project_role='user', update_time=now() \
                  where project_uuid='%s' and project_role='owner'" \
                  % (project_uuid)

        sql_03 = "update users_projects set project_role='owner', update_time=now() \
                  where user_uuid='%s' and project_uuid='%s'" \
                  % (project_owner, project_uuid)

        sql_04 = "insert into users_projects(user_uuid, project_uuid, \
                  project_role, status, create_time, update_time) \
                  values('%s', '%s', 'owner', 'enable', now(), now())" \
                  % (project_owner, project_uuid)

        sql_05 = "update resources_acl set user_uuid='%s', update_time=now() \
                  where resource_uuid='%s' and resource_type='project'" \
                  % (project_owner, project_uuid)

        if (self.user_project_check(project_owner, project_uuid) == 0):
            return super(UcenterDB, self).exec_update_sql(
                                          sql_01, sql_02, sql_04, sql_05)
        else:
            return super(UcenterDB, self).exec_update_sql(
                                          sql_01, sql_02, sql_03, sql_05)

    def project_update_desc(self, project_uuid, project_desc):

        sql = "update projects set project_desc='%s', update_time=now() \
               where project_uuid='%s'" \
               % (project_desc, project_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def project_check(self, project_uuid):

        sql = "select count(*) from users_projects where project_uuid='%s'" \
               % (project_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)[0][0]

    def project_delete(self, project_uuid):

        sql_01 = "delete from users_projects where project_uuid='%s'" \
                 % (project_uuid)

        sql_02 = "delete from projects where project_uuid='%s'" \
                 % (project_uuid)

        sql_03 = "delete from resources_acl where resource_uuid='%s'" \
                 % (project_uuid)

        return super(UcenterDB, self).exec_update_sql(
                                      sql_01, sql_02, sql_03)

    def user_team_check(self, user_uuid, team_uuid):

        sql = "select count(*) from users_teams \
               where user_uuid='%s' and team_uuid='%s'" \
               % (user_uuid, team_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)[0][0]

    def user_team_add(self, user_uuid, team_uuid, team_role):

        sql = "insert into users_teams(user_uuid, team_uuid, \
               team_role, status, create_time, update_time) \
               values('%s', '%s', '%s', 'enable', now(), now())" \
               % (user_uuid, team_uuid, team_role)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_team_list(self, team_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.user_uuid, b.user_name, c.role_name, \
                  a.create_time, a.update_time \
                  from users_teams a join users b join roles c \
                  where a.user_uuid=b.user_uuid \
                  and a.team_role=c.role_uuid \
                  and a.team_uuid='%s' \
                  limit %d,%d" \
                 % (team_uuid, start_position, page_size)

        sql_02 = "select count(*) from users_teams where team_uuid='%s'" \
                 % (team_uuid)

        team_user_list = super(UcenterDB, self).exec_select_sql(sql_01)
        count = super(UcenterDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "team_user_list": team_user_list,
                   "count": count
               }

    def user_team_del(self, user_uuid, team_uuid):

        sql = "delete from users_teams \
               where user_uuid='%s' and team_uuid='%s' \
               and team_role!='owner'" \
               % (user_uuid, team_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_team_activate(self, user_uuid, team_uuid):

        sql = "update users_teams set status='enable', update_time=now() \
               where user_uuid='%s' and team_uuid='%s'" \
               % (user_uuid, team_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_team_update(self, user_uuid, team_uuid, team_role):

        sql = "update users_teams set team_role='%s', update_time=now() \
               where user_uuid='%s' and team_uuid='%s' and team_role!='owner'" \
               % (team_role, user_uuid, team_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_project_check(self, user_uuid, project_uuid):

        sql = "select count(*) from users_projects \
               where user_uuid='%s' and project_uuid='%s'" \
               % (user_uuid, project_uuid)

        return super(UcenterDB, self).exec_select_sql(sql)[0][0]

    def user_project_add(self, user_uuid, project_uuid, project_role):

        sql = "insert into users_projects(user_uuid, project_uuid, \
               project_role, status, create_time, update_time) \
               values('%s', '%s', '%s', 'enable', now(), now())" \
               % (user_uuid, project_uuid, project_role)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_project_list(self, project_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.user_uuid, b.user_name, a.project_role, \
                  a.create_time, a.update_time \
                  from users_projects a join users b \
                  where a.user_uuid=b.user_uuid and a.project_uuid='%s' \
                  limit %d,%d" \
                  % (project_uuid, start_position, page_size)

        sql_02 = "select count(*) from users_projects where project_uuid='%s'" \
                 % (project_uuid)

        project_user_list = super(UcenterDB, self).exec_select_sql(sql_01)
        count = super(UcenterDB, self).exec_select_sql(sql_02)[0][0]

        return {
                   "project_user_list": project_user_list,
                   "count": count
               }

    def user_project_del(self, user_uuid, project_uuid):

        sql = "delete from users_projects \
               where user_uuid='%s' and project_uuid='%s' \
               and project_role!='owner'" \
               % (user_uuid, project_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)

    def user_project_update(self, user_uuid, project_uuid, project_role):

        sql = "update users_projects set project_role='%s', update_time=now() \
               where user_uuid='%s' and project_uuid='%s' and project_role!='owner'" \
               % (project_role, user_uuid, project_uuid)

        return super(UcenterDB, self).exec_update_sql(sql)
