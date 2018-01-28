# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/08

import uuid
from common.logs import logging as log


def normal_call(dict_data):
    project_uuid = dict_data.get('project_uuid')
    service_name = dict_data.get("service_name")
    return project_uuid, service_name


def font_infix_element(dict_data):

    font_uuid = str(uuid.uuid4())
    rc_uuid = str(uuid.uuid4())
    service_uuid = str(uuid.uuid4())
    user_uuid = dict_data.get('user_uuid')
    team_uuid = dict_data.get('team_uuid')
    project_uuid = dict_data.get('project_uuid')
    service_name = dict_data.get('service_name')
    image_dir = dict_data.get('image_dir')
    description = dict_data.get('description')
    certify = dict_data.get('certify')

    return font_uuid, rc_uuid, service_uuid, user_uuid, team_uuid, project_uuid, \
        service_name, image_dir, description, certify


def rc_infix_element(dict_data):

    pods_num = dict_data.get('pods_num')
    image_id = dict_data.get('image_id')
    cm_format = dict_data.get('cm_format')
    container_cpu = dict_data.get('container_cpu')
    container_memory = dict_data.get('container_memory')
    policy = dict_data.get('policy')
    auto_startup = dict_data.get('auto_startup')
    command = dict_data.get('command')
    image_name = dict_data.get('image_name')
    # isUpdate = dict_data.get('isUpdate')

    return pods_num, image_id, cm_format, container_cpu, container_memory, policy, auto_startup, command, image_name


def container_element(dict_data):
    log.info('the data when get the container element is: %s' % dict_data)
    rc_uuid = dict_data.get('rc_uuid')
    container_uuid = str(uuid.uuid4())
    container_port = dict_data.get('container_port')
    protocol = dict_data.get('protocol')
    access_mode = dict_data.get('access_mode')
    access_scope = dict_data.get('access_scope')
    tcp_port = dict_data.get('tcp_port')
    http_domain = dict_data.get('http_domain')
    tcp_domain = dict_data.get('tcp_domain')

    return container_uuid, rc_uuid, container_port, protocol, access_mode, access_scope, tcp_port, http_domain, \
        tcp_domain


def env_element(dict_data):

    env_uuid = str(uuid.uuid4())
    rc_uuid = dict_data.get('rc_uuid')
    env_key = dict_data.get('env_key')
    env_value = dict_data.get('env_value')

    return env_uuid, rc_uuid, env_key, env_value


def volume_element(dict_data):

    v_uuid = str(uuid.uuid4())
    rc_uuid = dict_data.get('rc_uuid')
    volume_uuid = dict_data.get('volume_uuid')
    disk_path = dict_data.get('disk_path')
    readonly = dict_data.get('readonly')

    return v_uuid, rc_uuid, volume_uuid, disk_path, readonly


def uuid_ele():
    return str(uuid.uuid4())
