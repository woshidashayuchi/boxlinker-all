# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/15

from common.logs import logging as log
from common.db_operate import DbOperate
from common.code import request_result, request_result_for_query
from common.time_log import func_time_log
from service_db import ServiceDB
import re
from k8sapi.driver.photo_driver import get_services_photos
from k8sapi.driver.others_driver import OthersDriver


class MetalWork(object):

    def __init__(self):
        self.operate = DbOperate()
        self.service_db = ServiceDB()
        self.other_driver = OthersDriver()

    def check_auth_power(self, context):
        project_priv = context.get('project_priv')
        team_priv = context.get('team_priv')
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                service_list_info = self.service_db.service_list(context)
                count = self.service_db.service_list_count(context)[0][0]
            else:
                service_list_info = self.service_db.service_list_user(context)
                count = self.service_db.service_list_user_count(context)[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            raise Exception('database select error')

        return service_list_info, count

    @staticmethod
    def merge_list_and_photos(dict_data, arr):
        return arr
        # avatars = []
        # for x in arr:
        #     avatars.append(x.get('service_uuid'))
        # dict_data['avatars_uuid'] = avatars
        # try:
        #     photos = get_services_photos(dict_data)
        # except Exception, e:
        #     log.error('get the photos error, reason is: %s' % e)
        #     return False
        # # log.info('---------arr:%s,photos:%s' % (arr, photos))
        # try:
        #     for i in arr:
        #         for j in photos:
        #             if i.get('service_uuid') == j.get('service_uuid'):
        #                 i.update({'image_dir': j.get('image_dir')})
        # except Exception, e:
        #     log.error('explain the result error, reason is: %s' % e)
        #     return False
        # return arr

    @staticmethod
    def merge_details_and_photos(dict_data, rc):
        dict_data['avatars_uuid'] = [rc.get('service_uuid')]
        try:
            photos = get_services_photos(dict_data)
        except Exception, e:
            log.error('get the photos error, reason is: %s' % e)
            return False

        try:
            for i in photos:
                if i.get('service_uuid') == rc.get('service_uuid'):
                    rc.update({'image_dir': i.get('image_dir')})
        except Exception, e:
            log.error('explain the result error, reason is: %s' % e)
            return False

        return rc

    def query_service(self, dict_data):
        log.info('query the service data(in) is %s' % dict_data)
        ret = []

        try:
            query_ret, count = self.check_auth_power(dict_data)
        except Exception, e:
            log.error('get the service list error...reason=%s' % e)
            raise

        for i in query_ret:
            http_domain = i[2]
            if i[2] == 'None':
                http_domain = ''
            if i[10] != '' and i[10] is not None and i[10] != 'NULL':
                if str(i[10]) == '1':
                    http_domain = i[9]
            ret.append({'service_uuid': i[0],
                        'service_name': i[1],
                        'service_status': i[5],
                        'image_dir': '', #i[6],
                        'ltime': self.operate.time_diff(i[7]),
                        'description': i[8],
                        'container': [{'http_domain': http_domain, 'tcp_domain': i[3], 'container_port': i[4],
                                       'access_mode': i[11]}]
                        })
        ret1 = ret
        result = self.merge_list_and_photos(dict_data, ret)
        if result is False:
            log.info('PRODUCE THE PHOTOS ERROR')
            return request_result_for_query(0, count, ret1)

        return request_result_for_query(0, count, result)

    def query_only_service(self, dict_data):
        log.info('query only service, the data(in) is: %s,type:%s' % (dict_data, type(dict_data)))

        ret = []
        dict_data['only_one_svc'] = 'yes'
        query_all = self.query_service(dict_data).get('result').get('service_list')

        for i in query_all:
            match_string = "[a-zA-Z0-9-_]*%s[a-zA-Z0-9-_]*" % str(dict_data.get("service_name"))
            if re.search(match_string, i.get("service_name")):
                ret.append(i)

        result = self.merge_list_and_photos(dict_data, ret)
        if ret is False:
            log.info('PRODUCE THE PHOTOS ERROR')
            return request_result_for_query(0, len(ret), ret)

        return request_result_for_query(0, len(ret), result)

    def service_detail(self, dict_data):
        log.info('query service detail, the data(in) is: %s' % dict_data)
        containers = []
        env = []
        volume = []
        rc = {}

        rc_ret, containers_ret, env_ret, volume_ret = self.service_db.service_detail(dict_data)

        for x in containers_ret:
            if x[7] == 'None' or x[7] is None or x[7] == '':
                domain = ''
            else:
                domain = x[7]
            containers.append({'container_port': x[0],
                               'protocol': x[1],
                               'access_mode': x[2],
                               'access_scope': x[3],
                               'tcp_port': x[4],
                               'http_domain': x[5],
                               'tcp_domain': x[6],
                               'domain': domain,
                               'identify': x[8],
                               'cname': x[9]})
        if len(env_ret) == 0 or len(env_ret[0]) == 0:
            pass
        else:
            for y in env_ret:
                env.append({'env_key': y[0], 'env_value': y[1]})

        if len(volume_ret) == 0 or len(volume_ret[0]) == 0:
            pass
        else:
            for z in volume_ret:
                volume.append({'volume_uuid': z[0],
                               'disk_path': z[1],
                               'readonly': z[2]})

        for m in rc_ret:
            rc = {'labels_name': m[0],
                  'pods_num': m[1],
                  'image_id': m[2],
                  'cm_format': m[3],
                  'container_cpu': m[4],
                  'container_memory': m[5],
                  'policy': m[6],
                  'auto_startup': m[7],
                  'command': m[8],
                  'service_uuid': m[11],
                  'service_name': m[12],
                  'service_status': m[13],
                  'ltime': self.operate.time_diff(m[10]),
                  'description': m[14]}
            # rc['ltime'] = self.operate.time_diff(m.get('rc_update_time'))

        rc['container'] = containers
        rc['env'] = env
        rc['volume'] = volume

        # del rc['rc_update_time']
        # del rc['rc_create_time']

        ret = self.merge_details_and_photos(dict_data, rc)
        if ret is False:
            log.info('PRODUCE THE PHOTOS ERROR')
            return request_result(0, rc)

        return request_result(0, ret)

    def get_container(self, context):
        try:
            db_ret = self.service_db.get_container_msg(context)
        except Exception, e:
            log.error('at the end, get the detainer container message error, reason is: %s' % e)
            return request_result(404)
        container = []
        for i in db_ret:
            container_port = i[0]
            protocol = i[1]
            access_mode = i[2]
            access_scope = i[3]

            container.append({'container_port': container_port, 'protocol': protocol,
                              'access_mode': access_mode, 'access_scope': access_scope})

        con = {'container': container}
        context.update(con)

        return context
