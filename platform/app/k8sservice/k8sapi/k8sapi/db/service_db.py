# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/07
import re
import uuid
from common.mysql_base import MysqlInit
from common.logs import logging as log
from unit_element import font_infix_element, rc_infix_element, container_element, env_element, volume_element,\
    normal_call, uuid_ele
from common.db_operate import DbOperate
from common.time_log import func_time_log
from conf import conf


class ServiceDB(MysqlInit):

    def __init__(self):
        super(ServiceDB, self).__init__()
        self.operate = DbOperate()
        self.conf = conf

    def init_insert(self):

        sql_create_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                         "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                         "'%s')" % ('service_create', 'api', 'global', 'global', 'global', '0')

        sql_list_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                       "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                       "'%s')" % ('service_list', 'api', 'global', 'global', 'global', 'global')

        sql_create_certify_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                                 "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                                 "'%s')" % ('certify_create', 'api', 'global', 'global', 'global', '0')

        sql_list_certify_api = "insert into resources_acl(resource_uuid, resource_type, admin_uuid, " \
                               "team_uuid, project_uuid, user_uuid) VALUES('%s', '%s', '%s', '%s', '%s'," \
                               "'%s')" % ('certify_list', 'api', 'global', 'global', 'global', 'global')

        # sql_alarm_init = "insert into alarming(uuid,wise,cpu_unit,cpu_value,memory_unit,memory_value," \
        #                  "network_unit,network_value,storage_unit,storage_value,time_span,alarm_time) " \
        #                  "values('default',10,'%',80,'%',80,'M',10,'%',80,'1h','12~15')"

        return super(ServiceDB, self).exec_update_sql(sql_create_api, sql_list_api, sql_create_certify_api,
                                                      sql_list_certify_api)

    def name_if_used_check(self, dict_data):

        project_uuid = dict_data.get("project_uuid")

        sql = "select service_name from font_service where " \
              "project_uuid = '%s'" % project_uuid

        return super(ServiceDB, self).exec_select_sql(sql)

    def infix_db(self, dict_data):

        font_uuid, rc_uuid, service_uuid, user_uuid, team_uuid, project_uuid, service_name, \
            image_dir, description, certify = font_infix_element(dict_data)

        pods_num, image_id, cm_format, container_cpu, container_memory, policy, auto_startup, \
            command, image_name = rc_infix_element(dict_data)

        sql_font = "insert into font_service(uuid, rc_uuid, service_uuid, user_uuid, " \
                   "team_uuid, project_uuid, service_name,service_status, description, certify) VALUES('%s', '%s', '%s', " \
                   "'%s','%s', '%s', '%s', '%s','%s','%s')" % (font_uuid, rc_uuid, service_uuid, user_uuid, team_uuid,
                                                               project_uuid, service_name, 'pending', description, certify)

        sql_rc = "insert into replicationcontrollers(uuid, labels_name, pods_num, " \
                 "image_id, cm_format, container_cpu, container_memory, policy, auto_startup, command, image_name) " \
                 "VALUES ('%s', '%s', %d, '%s', '%s', '%s', '%s', %d, %d," \
                 "'%s', '%s')" % (rc_uuid, service_name.replace('_', '-')+project_uuid, pods_num, image_id, cm_format,
                                  container_cpu, container_memory, policy, auto_startup, command, image_name)

        sql_acl = "insert into resources_acl(resource_uuid,resource_type,admin_uuid,team_uuid,project_uuid," \
                  "user_uuid) VALUES ('%s','%s','%s','%s','%s'," \
                  "'%s')" % (font_uuid, 'service', 'global', dict_data.get('team_uuid'),
                             dict_data.get('project_uuid'), dict_data.get('user_uuid'))

        # sql_alarm_rules = "insert into alarm_service_rules(uuid,alarm_uuid,service_uuid) values " \
        #                   "('%s', 'default', '%s')" % (alarm_uuid, font_uuid)

        # sql_alarm_rules = "insert into alarm_service_rules(uuid,alarm_uuid,service_uuid,email,phone) values " \
        #                   "('%s', 'default', '%s',%s,%s)" % (alarm_uuid, font_uuid, email, phone)

        return super(ServiceDB, self).exec_update_sql(sql_font, sql_rc, sql_acl)

    def get_service_uuid(self, dict_data):
        sql = "select uuid from font_service WHERE service_name='%s' and \
               project_uuid='%s'" % (dict_data.get('service_name'), dict_data.get('project_uuid'))

        ret = super(ServiceDB, self).exec_select_sql(sql)

        return ret[0][0]

    def get_rc_uuid(self, dict_data):

        project_uuid = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')

        sql = "select rc_uuid from font_service where service_name='%s' and project_uuid='%s'" % (service_name,
                                                                                                  project_uuid)

        ret = super(ServiceDB, self).exec_select_sql(sql)
        return ret[0][0]

    def container_infix_db(self, dict_data):

        container_uuid, rc_uuid, container_port, protocol, access_mode, access_scope, tcp_port, http_domain, \
            tcp_domain = container_element(dict_data)

        sql = "insert into containers(uuid,rc_uuid,container_port,protocol,access_mode,access_scope," \
              "tcp_port,http_domain,cname,tcp_domain) VALUES('%s','%s', %d, '%s', '%s', '%s', '%s', '%s'," \
              "'%s','%s')" % (container_uuid, rc_uuid, container_port, protocol, access_mode, access_scope,
                              tcp_port, http_domain, http_domain, tcp_domain)

        return super(ServiceDB, self).exec_update_sql(sql)

    def env_infix_db(self, dict_data):
        env_uuid, rc_uuid, env_key, env_value = env_element(dict_data)
        sql = "insert into env(uuid,rc_uuid,env_key,env_value) VALUES ('%s','%s','%s','%s')" % (env_uuid, rc_uuid,
                                                                                                env_key, env_value)
        return super(ServiceDB, self).exec_update_sql(sql)

    def volume_infix_db(self, dict_data):
        v_uuid, rc_uuid, volume_uuid, disk_path, readonly = volume_element(dict_data)
        sql = "insert into volume(uuid, rc_uuid, volume_uuid, disk_path, readonly) VALUES ('%s','%s','%s','%s'," \
              "'%s')" % (v_uuid, rc_uuid, volume_uuid, disk_path, readonly)

        return super(ServiceDB, self).exec_update_sql(sql)

    def max_used_port(self):

        sql = 'select max(CAST(tcp_port AS SIGNED)) tcp_port from containers'

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_using_port(self, tcp_port, project_uuid, service_name):

        sql = "update containers set tcp_port='%s' WHERE rc_uuid=(SELECT rc_uuid from font_service WHERE " \
              "service_name='%s' AND project_uuid='%s') and access_mode IN ('HTTP', 'HTTPS')" % (tcp_port,
                                                                                                 service_name,
                                                                                                 project_uuid)

        return super(ServiceDB, self).exec_update_sql(sql)

    def create_svcaccount_or_not(self, dict_data):

        sql = "select uuid from font_service where project_uuid='%s'" % dict_data.get('project_uuid')

        return super(ServiceDB, self).exec_select_sql(sql)

    @func_time_log
    def service_list(self, dict_data):

        project_uuid, service_name = normal_call(dict_data)
        page_size = int(dict_data.get('page_size'))
        page_num = int(dict_data.get('page_num'))
        start_position = (page_num - 1) * page_size

        sql = "SELECT a.uuid service_uuid, a.service_name, b.http_domain, b.tcp_domain, b.container_port, \
               a.service_status, a.image_dir, a.service_create_time ltime, a.description,b.private_domain domain," \
              "b.identify,b.access_mode FROM font_service a join \
               containers b \
               WHERE (a.rc_uuid = b.rc_uuid AND a.project_uuid='%s' AND ((b.http_domain is not \
               NULL and b.http_domain != 'None' and b.http_domain != '') OR (b.tcp_domain is not NULL AND \
               b.tcp_domain != 'None' and b.tcp_domain != ''))) and (a.lifecycle is NULL \
               OR lifecycle='') ORDER BY ltime DESC \
               limit %d, %d" % (project_uuid, start_position, page_size)

        # sql = "SELECT a.uuid service_uuid, a.service_name, b.http_domain, b.tcp_domain, b.container_port, \
        #        a.service_status, a.image_dir, a.service_create_time ltime, a.description,b.private_domain domain," \
        #       "b.identify,b.access_mode FROM font_service a join \
        #        containers b \
        #        WHERE (a.rc_uuid = b.rc_uuid AND a.project_uuid='%s') and (a.lifecycle is NULL \
        #        OR lifecycle='') ORDER BY ltime DESC \
        #        limit %d, %d" % (project_uuid, start_position, page_size)

        log.info('get the service_list sql is: %s' % sql)

        # sql_count = "select count(*) from font_service a where a.project_uuid='%s'" % project_uuid

        return super(ServiceDB, self).exec_select_sql(sql)

    def service_list_count(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        sql = "select count(*) from font_service a where a.project_uuid='%s' AND " \
              "(lifecycle is NULL OR lifecycle='')" % project_uuid
        return super(ServiceDB, self).exec_select_sql(sql)

    def service_list_user(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        user_uuid = dict_data.get('project_uuid')
        page_size = int(dict_data.get('page_size'))
        page_num = int(dict_data.get('page_num'))
        start_position = (page_num - 1) * page_size

        sql = "SELECT a.uuid service_uuid, a.service_name, b.http_domain, b.tcp_domain, b.container_port, \
               a.service_status, a.image_dir, a.service_create_time ltime, a.description, b.private_domain domain, \
               b.identify,b.access_mode FROM font_service a join  \
               containers b \
               WHERE (a.rc_uuid = b.rc_uuid AND a.project_uuid='%s' AND a.user_uuid='%s' \
               AND ((b.http_domain is not NULL and b.http_domain != '' AND b.http_domain != 'None') \
               OR (b.tcp_domain is not NULL AND b.tcp_domain != 'None' AND b.tcp_domain != '') \
               )) and (a.lifecycle is NULL or a.lifecycle='') ORDER BY ltime DESC  \
               limit %d, %d" % (project_uuid, user_uuid, start_position, page_size)
        # sql = "SELECT a.uuid service_uuid, a.service_name, b.http_domain, b.tcp_domain, b.container_port, \
        #        a.service_status, a.image_dir, a.service_create_time ltime, a.description, b.private_domain domain," \
        #       "b.identify,b.access_mode \
        #        FROM font_service a join  \
        #        containers b \
        #        WHERE (a.rc_uuid = b.rc_uuid AND a.project_uuid='%s' AND a.user_uuid='%s' \
        #        ) and (a.lifecycle is NULL or a.lifecycle='') ORDER BY ltime DESC  \
        #        limit %d, %d" % (project_uuid, user_uuid, start_position, page_size)

        log.info('get the service_list for user sql is: %s' % sql)

        # sql_count = "select count(*) from font_service a where a.project_uuid='%s' AND " \
        #             "a.user_uuid='%s'" % (project_uuid, user_uuid)

        return super(ServiceDB, self).exec_select_sql(sql)

    def service_list_user_count(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        user_uuid = dict_data.get('user_uuid')
        sql_count = "select count(*) from font_service a where a.project_uuid='%s' AND " \
                    "a.user_uuid='%s' and (a.lifecycle IS NULL OR a.lifecycle='')" % (project_uuid, user_uuid)
        return super(ServiceDB, self).exec_select_sql(sql_count)

    def service_detail(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        project_uuid = dict_data.get('project_uuid')

        sql_rc = "select a.labels_name,a.pods_num,a.image_id,a.cm_format,a.container_cpu,a.container_memory,a.policy, \
                  a.auto_startup,a.command,a.rc_create_time,a.rc_update_time, b.uuid service_uuid, b.service_name, \
                  b.service_status, b.description from \
                  replicationcontrollers a,font_service b \
                  where a.uuid = (select rc_uuid from font_service where \
                  project_uuid='%s' and uuid='%s') and b.uuid='%s'" % (project_uuid, service_uuid, service_uuid)

        sql_container = "select container_port, protocol, access_mode,access_scope,tcp_port,http_domain,tcp_domain," \
                        "private_domain,identify,cname from containers where rc_uuid = (select rc_uuid from " \
                        "font_service where project_uuid='%s' and uuid='%s') ORDER BY container_port" % (project_uuid,
                                                                                                         service_uuid)

        sql_env = "select env_key,env_value from env where rc_uuid = (select rc_uuid from font_service where \
                   project_uuid='%s' and uuid='%s') ORDER BY env_key" % (project_uuid, service_uuid)

        sql_volume = "select volume_uuid,disk_path,readonly from volume where rc_uuid = (select rc_uuid from " \
                     "font_service where project_uuid='%s' and uuid='%s') ORDER BY disk_path " % (project_uuid,
                                                                                                  service_uuid)

        rc_ret = super(ServiceDB, self).exec_select_sql(sql_rc)

        containers_ret = super(ServiceDB, self).exec_select_sql(sql_container)

        env_ret = super(ServiceDB, self).exec_select_sql(sql_env)

        volume_ret = super(ServiceDB, self).exec_select_sql(sql_volume)

        return rc_ret, containers_ret, env_ret, volume_ret

    def get_container_msg(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')
        sql = "select container_port,protocol,access_mode,access_scope from containers WHERE " \
              "rc_uuid=(select rc_uuid from font_service WHERE project_uuid='%s' AND " \
              "service_name='%s')" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_select_sql(sql)

    def get_service_name(self, dict_data):

        sql = "select service_name from font_service where uuid='%s'" % dict_data.get('service_uuid')

        ret = super(ServiceDB, self).exec_select_sql(sql)
        log.info('************%s' % ret)
        dict_data.update({'service_name': ret[0][0]})

        return dict_data

    def get_using_port(self, dict_data):
        sql = "select tcp_port from containers WHERE rc_uuid=(select rc_uuid from font_service " \
              "WHERE project_uuid='%s' AND service_name='%s' and tcp_port is not NULL AND " \
              "tcp_port != 'None' and tcp_port !='')" % (dict_data.get('project_uuid'), dict_data.get('service_name'))

        return super(ServiceDB, self).exec_select_sql(sql)

    def get_using_volume(self, dict_data):
        volume_ret = []
        sql = "select volume_uuid,disk_path,readonly from volume where " \
              "rc_uuid=(SELECT rc_uuid from font_service where " \
              "service_name='%s' and project_uuid='%s')" % (dict_data.get('service_name'),
                                                            dict_data.get('project_uuid'))

        ret = super(ServiceDB, self).exec_select_sql(sql)
        if len(ret) == 0 or len(ret[0]) == 0:
            return []
        else:
            for i in ret:
                volume_ret.append({'volume_uuid': i[0], 'disk_path': i[1], 'readonly': i[2]})

        return volume_ret

    def delete_all(self, dict_data):

        service_name = dict_data.get('service_name')
        project_uuid = dict_data.get('project_uuid')
        #
        # del_volume = "delete from volume where rc_uuid=(select rc_uuid from font_service " \
        #              "where service_name='%s' and project_uuid='%s')" % (service_name, project_uuid)
        #
        # del_container = "delete from containers where rc_uuid=(select rc_uuid from font_service " \
        #                 "where service_name='%s' and project_uuid='%s')" % (service_name, project_uuid)
        #
        # del_env = "delete from env where rc_uuid=(select rc_uuid from font_service " \
        #           "where service_name='%s' and project_uuid='%s')" % (service_name, project_uuid)
        #
        # del_rc = "delete from replicationcontrollers where uuid=(select rc_uuid from font_service " \
        #          "where service_name='%s' and project_uuid='%s')" % (service_name, project_uuid)
        #
        # del_alarm = "delete from alarming WHERE uuid=(SELECT alarm_uuid from alarm_service_rules WHERE " \
        #             "service_uuid=(SELECT uuid FROM font_service WHERE service_name='%s' AND project_uuid='%s')) " \
        #             "AND uuid != 'default'" % (service_name, project_uuid)
        #
        # del_rules = "delete from alarm_service_rules WHERE service_uuid=(select uuid from font_service WHERE " \
        #             "service_name='%s' AND project_uuid='%s')" % (service_name, project_uuid)
        #
        # del_font = "delete from font_service where project_uuid='%s' and service_name='%s'" % (project_uuid,
        #                                                                                        service_name)
        #
        # def_acl = "delete from resources_acl where resource_uuid='%s'" % (dict_data.get('service_uuid'))
        #
        # return super(ServiceDB, self).exec_update_sql(del_volume, del_container, del_env, del_rc,
        #                                               del_alarm, del_rules, del_font, def_acl)

        del_logic = "update font_service set lifecycle='stop' WHERE " \
                    "service_name='%s' AND project_uuid='%s'" % (service_name, project_uuid)

        log.info('logic delete the resource, sql is: %s' % del_logic)

        return super(ServiceDB, self).exec_update_sql(del_logic)

    def update_container(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        container = dict_data.get('container')

        sql_delete = "delete from containers where rc_uuid=(select rc_uuid from font_service where " \
                     "project_uuid='%s' and service_name='%s')" % (project_uuid, service_name)
        super(ServiceDB, self).exec_update_sql(sql_delete)

        for i in container:
            uuid_c = uuid_ele()
            container_uuid, rc_uuid, container_port, protocol, access_mode, access_scope, tcp_port, http_domain, \
                tcp_domain = container_element(i)

            sql_insert = "insert into containers(uuid, rc_uuid, container_port, protocol, access_mode," \
                         "access_scope,tcp_port,http_domain,cname,tcp_domain,private_domain,identify) VALUES " \
                         "('%s',(select rc_uuid from font_service where service_name='%s' " \
                         "and project_uuid='%s'),%d,'%s','%s','%s','%s','%s','%s','%s','%s'," \
                         "'%s')" % (uuid_c, service_name, project_uuid, int(container_port), protocol, access_mode,
                                    access_scope, tcp_port, http_domain, http_domain, tcp_domain, i.get('domain'),
                                    i.get('identify'))
            log.info('update the container sql is: %s' % sql_insert)
            super(ServiceDB, self).exec_update_sql(sql_insert)

        sql_update_time = "update font_service SET service_update_time=now() WHERE rc_uuid='%s'" % rc_uuid
        super(ServiceDB, self).exec_update_sql(sql_update_time)

    def http_to_tcp_container(self, project_uuid, service_name, container):
        container_port = container.get('container_port')
        protocol = container.get('protocol')
        access_mode = container.get('access_mode')
        access_scope = container.get('access_scope')
        tcp_port = container.get('tcp_port')
        tcp_domain = self.conf.lb+str(tcp_port)
        uuid_c = str(uuid.uuid4())

        sql = "insert into containers(uuid, rc_uuid, container_port, protocol, access_mode," \
              "access_scope,tcp_port, tcp_domain) VALUES ('%s', (select rc_uuid from font_service where " \
              "service_name='%s' and project_uuid='%s'),%d,'%s','%s','%s','%s','%s')" % (uuid_c, service_name,
                                                                                         project_uuid,
                                                                                         int(container_port),
                                                                                         protocol,
                                                                                         access_mode,
                                                                                         access_scope, tcp_port,
                                                                                         tcp_domain)
        log.info('http service change to tcp service...insert the tcp_port sql is: %s' % sql)
        return super(ServiceDB, self).exec_update_sql(sql)

    def get_svc_port(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)

        sql = "select tcp_port from containers WHERE rc_uuid=(SELECT rc_uuid from font_service WHERE " \
              "project_uuid='%s' AND service_name='%s') AND tcp_domain != '' AND tcp_domain != 'None' " \
              "AND tcp_domain is not NULL" % (project_uuid, service_name)

        log.info('获取正在使用的port的sql为:%s' % sql)

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_env(self, dict_data):
        env = dict_data.get('env')
        project_uuid, service_name = normal_call(dict_data)

        sql_delete = "delete from env where rc_uuid=(select rc_uuid from font_service where " \
                     "project_uuid='%s' and service_name='%s')" % (project_uuid, service_name)

        try:
            del_result = super(ServiceDB, self).exec_update_sql(sql_delete)
            if del_result is not None:
                return False
        except Exception, e:
            log.error('database delete(env) error, reason=%s' % e)
            return False

        for i in env:
            uuid_e = uuid_ele()
            sql_insert = "insert INTO env(uuid,rc_uuid,env_key,env_value) VALUES ('%s'," \
                         "((select rc_uuid from font_service where service_name='%s' " \
                         "and project_uuid='%s')),'%s','%s')" % (uuid_e, service_name, project_uuid,
                                                                 i.get('env_key'), i.get('env_value'))
            try:
                if super(ServiceDB, self).exec_update_sql(sql_insert) is not None:
                    return False
            except Exception, e:
                log.error('database update(env) error, reason=%s' % e)
                return False

        try:
            sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                              "and service_name='%s'" % (project_uuid, service_name)
            super(ServiceDB, self).exec_update_sql(sql_update_time)
        except Exception, e:
            log.error('database update(font_service) error, reason=%s' % e)
            return False

        return True

    def update_volume(self, dict_data):
        volume = dict_data.get('volume')
        project_uuid, service_name = normal_call(dict_data)

        sql_delete = "delete from volume where rc_uuid=(SELECT rc_uuid from font_service WHERE " \
                     "project_uuid='%s' and service_name='%s')" % (project_uuid, service_name)

        try:
            del_result = super(ServiceDB, self).exec_update_sql(sql_delete)
            if del_result is not None:
                return False
        except Exception, e:
            log.error('database delete(volume) error, reason=%s' % e)
            return False

        for i in volume:
            uuid_v = uuid_ele()
            sql_insert = "insert into volume(uuid,rc_uuid,volume_uuid,disk_path,readonly) VALUES " \
                         "('%s',(select rc_uuid from font_service where service_name='%s' and " \
                         "project_uuid='%s'),'%s','%s','%s')" % (uuid_v, service_name, project_uuid,
                                                                 i.get('volume_uuid'), i.get('disk_path'),
                                                                 i.get('readonly'))

            try:
                if super(ServiceDB, self).exec_update_sql(sql_insert) is not None:
                    return False
            except Exception, e:
                log.error('database update(volume) error, reason=%s' % e)
                return False
        try:
            sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                              "and service_name='%s'" % (project_uuid, service_name)
            super(ServiceDB, self).exec_update_sql(sql_update_time)
        except Exception, e:
            log.error('database update(font_service) error, reason=%s' % e)
            return False

        return True

    def update_status(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)

        sql_start = "update font_service SET service_status='%s' WHERE service_name='%s' " \
                    "and project_uuid='%s'" % ('ContainerCreating', service_name, project_uuid)

        sql_stop = "update font_service SET service_status='%s' WHERE service_name='%s'" \
                   "and project_uuid='%s'" % ('Stopping', service_name, project_uuid)

        try:
            sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                              "and service_name='%s'" % (project_uuid, service_name)
            super(ServiceDB, self).exec_update_sql(sql_update_time)
        except Exception, e:
            log.error('database update(font_service) error, reason=%s' % e)
            return False

        if dict_data.get('operate') == 'start':
            return super(ServiceDB, self).exec_update_sql(sql_start)
        if dict_data.get('operate') == 'stop':
            return super(ServiceDB, self).exec_update_sql(sql_stop)
        else:
            return False

    def update_telescopic(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        pods_num = dict_data.get('pods_num')
        sql = "update replicationcontrollers SET pods_num=%d WHERE uuid=(SELECT rc_uuid from " \
              "font_service WHERE service_name='%s' and project_uuid='%s')" % (pods_num,
                                                                               service_name,
                                                                               project_uuid)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def update_command(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        command = dict_data.get('command')
        sql = "update replicationcontrollers SET command='%s' WHERE uuid=(SELECT rc_uuid from " \
              "font_service WHERE service_name='%s' and project_uuid='%s')" % (command,
                                                                               service_name, project_uuid)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def domain_list(self, dict_data):
        domain = dict_data.get('domain')
        sql_check = "select private_domain from containers where private_domain is not Null " \
                    "and private_domain !='None' AND private_domain !=''"

        ret = super(ServiceDB, self).exec_select_sql(sql_check)
        log.info('the domain result is %s, type is %s' % (ret, type(ret)))

        for i in range(len(ret)):
            for j in range(len(ret[i])):
                p_domain = re.split(',', ret[i][j])
                i_domain = re.split(',', domain)
                for q in i_domain:
                    if q in p_domain:
                        return False

        return True

    def update_domain(self, dict_data):
        log.info('the data when update the domain is: %s' % dict_data)
        project_uuid, service_name = normal_call(dict_data)
        domain = dict_data.get('domain')
        if self.domain_list(dict_data) is False:
            return False

        sql_up = "update containers SET private_domain='%s', identify='%s' WHERE " \
                 "rc_uuid=(SELECT rc_uuid from font_service WHERE project_uuid='%s' and " \
                 "service_name='%s') and http_domain is not NULL and " \
                 "http_domain != 'None' and http_domain != ''" % (domain, '0', project_uuid, service_name)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        ret = super(ServiceDB, self).exec_update_sql(sql_up, sql_update_time)

        if ret is None:
            return True
        else:
            raise Exception('database update error')

    def get_domain(self, dict_data):
        log.info('the data(operate database) when get the domain is: %s' % dict_data)

        project_uuid, service_name = normal_call(dict_data)
        sql = "select private_domain as domain, identify from containers WHERE " \
              "rc_uuid=(SELECT rc_uuid from font_service WHERE project_uuid='%s' and " \
              "service_name='%s') and http_domain is not NULL and http_domain != 'None' " \
              "and http_domain !=''" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_domain_to_none(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        sql = "update containers SET private_domain=NULL ,identify=NULL WHERE " \
              "rc_uuid=(SELECT rc_uuid from font_service WHERE project_uuid='%s' and " \
              "service_name='%s') and http_domain is not NULL and http_domain != 'None' " \
              "and http_domain != ''" % (project_uuid, service_name)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def update_http_domain(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        sql = "update containers SET http_domain=private_domain WHERE " \
              "rc_uuid=(SELECT rc_uuid from font_service WHERE project_uuid='%s' and " \
              "service_name='%s') and http_domain is not NULL and http_domain != 'None' " \
              "and http_domain != ''" % (project_uuid, service_name)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def get_http_domain(self, dict_data):
        if dict_data.get('domain') == '' or dict_data.get('domain') is None:
            return ((0,),)
        sql = "select count(*) from containers WHERE http_domain='%s'" % dict_data.get('domain')
        return super(ServiceDB, self).exec_select_sql(sql)

    def update_identify_to_1(self, dict_data):
        project_uuid, service_name = normal_call(dict_data)
        sql = "update containers SET private_domain='%s',identify='%s' WHERE " \
              "rc_uuid=(SELECT rc_uuid from font_service WHERE project_uuid='%s' and " \
              "service_name='%s') and http_domain is not NULL AND http_domain !='None' " \
              "and http_domain != ''" % (dict_data.get('domain'),
                                                                                           dict_data.get('identify'),
                                                                                           project_uuid, service_name)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def identify_check(self, dict_data):

        project_uuid, service_name = normal_call(dict_data)

        sql = "select private_domain, identify, container_port from containers where rc_uuid=(SELECT rc_uuid from " \
              "font_service " \
              "WHERE project_uuid='%s' and service_name='%s') and http_domain is not NULL and " \
              "http_domain != 'None' AND http_domain !=''" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_select_sql(sql)

    def get_uuid_from_admin(self, dict_data):
        sql = "select team_uuid,project_uuid from font_service WHERE " \
              "rc_uuid=(SELECT rc_uuid from containers WHERE private_domain='%s')" % dict_data.get('domain')

        return super(ServiceDB, self).exec_select_sql(sql)

    def check_uuid(self, font_uuid=None, rc_uuid=None, container_uuid=None, env_uuid=None, volume_uuid=None,
                   acl_uuid=None):

        sql_font = "select uuid from font_service where uuid='%s'" % font_uuid
        sql_rc = "select uuid from replicationcontrollers where uuid='%s'" % rc_uuid
        sql_container = "select uuid from containers where uuid='%s'" % container_uuid
        sql_env = "select uuid from env where uuid='%s'" % env_uuid
        sql_volume = "select uuid from volume where uuid='%s'" % volume_uuid
        sql_acl = "select resource_uuid from resources_acl where resource_uuid='%s'" % acl_uuid

        try:
            if len(super(ServiceDB, self).exec_select_sql(sql_font)[0]) != 0:
                return False
            if len(super(ServiceDB, self).exec_select_sql(sql_rc)[0]) != 0:
                return False
            if len(super(ServiceDB, self).exec_select_sql(sql_container)[0]) != 0:
                return False
            if len(super(ServiceDB, self).exec_select_sql(sql_env)[0]) != 0:
                return False
            if len(super(ServiceDB, self).exec_select_sql(sql_volume)[0]) != 0:
                return False
            if len(super(ServiceDB, self).exec_select_sql(sql_acl)[0]) != 0:
                return False
        except Exception, e:
            log.error('compare the uuid error, reason=%s' % e)
            return 'error'

    def detail_container(self, context):
        sql = "select * from containers WHERE rc_uuid=(SELECT rc_uuid from font_service where " \
              "uuid='%s')" % (context.get('service_uuid'))

        conn, cur = self.operate.connection()
        container_ret = self.operate.exeQuery(cur, sql)
        self.operate.connClose(conn, cur)

        return container_ret

    def update_publish(self, context):

        if context.get('policy') == 1:
            sql = "update replicationcontrollers SET policy=%d where uuid=(SELECT rc_uuid from " \
                  "font_service WHERE uuid='%s')" % (1, context.get('service_uuid'))
        else:
            sql = "update replicationcontrollers set policy=%d,image_id=%s WHERE " \
                  "uuid=(SELECT rc_uuid from font_service WHERE " \
                  "uuid='%s')" % (0, context.get('image_id'), context.get('service_uuid'))

        sql_update_time = "update font_service SET service_update_time=now() WHERE " \
                          "uuid='%s' " % context.get('service_uuid')

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def update_status_anytime(self, ps, service_status):
        try:
            service_name = ps.split('#')[0]
            project_uuid = ps.split('#')[1]
        except Exception, e:
            log.error('parameters explain error, reason is: %s' % e)
            raise Exception('parameters explain error')

        sql = "update font_service set service_status='%s' WHERE project_uuid='%s' " \
              "and service_name='%s'" % (service_status, project_uuid, service_name)

        log.info("update app status's sql is: %s" % sql)
        return super(ServiceDB, self).exec_update_sql(sql)

    def rc_for_billing(self, dict_data):
        log.info('rc fot billing data is: %s' % dict_data)

        sql = "select a.uuid, a.service_status, b.cm_format, b.pods_num from font_service a, " \
              "replicationcontrollers b WHERE a.project_uuid='%s' and a.service_name='%s' and " \
              "a.rc_uuid=b.uuid" % (dict_data.get('project_uuid'), dict_data.get('service_name'))

        log.info('get the rc message for billings sql is: %s' % sql)
        return super(ServiceDB, self).exec_select_sql(sql)

    def update_cm(self, dict_data):
        cm_format = dict_data.get('cm_format')
        container_cpu = dict_data.get('container_cpu')
        container_memory = dict_data.get('container_memory')
        service_name = dict_data.get('service_name')
        project_uuid = dict_data.get('project_uuid')

        sql = "update replicationcontrollers set cm_format='%s',container_cpu='%s',container_memory='%s' " \
              "WHERE uuid=(SELECT rc_uuid from font_service WHERE service_name='%s' AND " \
              "project_uuid='%s' )" % (cm_format, container_cpu, container_memory, service_name, project_uuid)

        sql_update_time = "update font_service SET service_update_time=now() WHERE project_uuid='%s' " \
                          "and service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql, sql_update_time)

    def update_description(self, dict_data):
        service_uuid = dict_data.get('service_uuid')
        description = dict_data.get('description')

        sql = "update font_service set description='%s' where uuid='%s'" % (description,
                                                                            service_uuid)

        log.info('update the database sql is: %s' % sql)
        return super(ServiceDB, self).exec_update_sql(sql)

    def get_user_uuid(self, project_uuid, service_name):

        sql = "select user_uuid from font_service WHERE service_name='%s' and " \
              "project_uuid='%s'" % (service_name, project_uuid)

        return super(ServiceDB, self).exec_select_sql(sql)

    def get_ingress_certify(self, project_uuid, service_name):
        sql = "select access_mode from containers where rc_uuid = (select rc_uuid from font_service " \
              "WHERE project_uuid='%s' AND service_name='%s') and access_mode is not NULL " \
              "AND access_mode != '' and access_mode != 'None'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_ingress_certify(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')
        certify = dict_data.get('certify')

        sql = "update font_service set certify=%d WHERE project_uuid='%s' AND service_name='%s'" % (certify,
                                                                                                    project_uuid,
                                                                                                    service_name)
        return super(ServiceDB, self).exec_update_sql(sql)

    def phy_insert(self, dict_data):
        project_uuid = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')

        sql = "insert into logic(service_uuid) select uuid from font_service WHERE project_uuid='%s' and " \
              "service_name='%s'" % (project_uuid, service_name)

        return super(ServiceDB, self).exec_update_sql(sql)

    def delete_in24(self):

        sql = "select service_uuid from logic WHERE delete_time>=date_sub(now(), interval 24 hour)"

        return super(ServiceDB, self).exec_select_sql(sql)

    def create_in24(self):

        sql = "select a.uuid resource_uuid, a.service_name resource_name, a.service_status," \
              "a.team_uuid, a.project_uuid, a.user_uuid,b.pods_num, b.cm_format FROM font_service a, " \
              "replicationcontrollers b WHERE a.service_create_time>=date_sub(now(), interval 24 hour)"

        return super(ServiceDB, self).exec_select_sql(sql)

    def update_in24(self):

        sql = "select a.uuid resource_uuid, a.service_name resource_name, a.service_status," \
              "a.team_uuid, a.project_uuid, a.user_uuid,b.pods_num, b.cm_format FROM font_service a, " \
              "replicationcontrollers b WHERE a.service_update_time>=date_sub(now(), interval 24 hour)"

        return super(ServiceDB, self).exec_select_sql(sql)


class CertifyDB(MysqlInit):
    def __init__(self):
        super(CertifyDB, self).__init__()
        self.operate = DbOperate()

    def infix_certify(self, dict_data):
        log.info('certify in database , the data is: %s' % dict_data)
        content = dict_data.get('content')
        crt = content.get('tls.crt')
        tls_key = content.get('tls.key')
        certify_uuid = str(uuid.uuid4())
        team_uuid = dict_data.get('team_uuid')
        project_uuid = dict_data.get('project_uuid')
        user_uuid = dict_data.get('user_uuid')

        sql_certify = "insert INTO certify (uuid,crt,tls_key) VALUES ('%s','%s','%s')" % (certify_uuid, crt, tls_key)

        sql_acl = "insert INTO resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid," \
                  "project_uuid, user_uuid) VALUES ('%s', '%s', '%s', '%s', '%s', " \
                  "'%s')" % (certify_uuid, 'certify', 0, team_uuid, project_uuid, user_uuid)

        super(CertifyDB, self).exec_update_sql(sql_certify, sql_acl)

        return certify_uuid

    def query_certify(self, dict_data):

        project_uuid = dict_data.get('project_uuid')
        sql = "select crt, tls_key, uuid from certify WHERE uuid=(SELECT resource_uuid from resources_acl WHERE " \
              "project_uuid='%s' and resource_type='certify')" % project_uuid

        return super(CertifyDB, self).exec_select_sql(sql)

    def update_certify(self, dict_data):
        certify_uuid = dict_data.get('certify_uuid')
        content = dict_data.get('content')
        crt = content.get('tls.crt')
        tls_key = content.get('tls.key')

        sql = "update certify SET crt='%s', tls_key='%s' WHERE uuid='%s'" % (crt, tls_key, certify_uuid)

        return super(CertifyDB, self).exec_update_sql(sql)


class AdminServicesDB(MysqlInit):
    def __init__(self):
        super(AdminServicesDB, self).__init__()

    def get_all_no_stopping_svc(self):
        sql = "select uuid service_uuid, project_uuid, service_name from font_service WHERE lifecycle is NULL or " \
              "lifecycle=''"

        return super(AdminServicesDB, self).exec_select_sql(sql)
