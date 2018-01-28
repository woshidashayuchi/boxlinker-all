#! /usr/bin python
# -*- coding:utf8 -*-
# Date: 2016/8/9
# Author: wang-xf

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import String, Column, Integer
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy.databases import mysql
from common.logs import logging as log
from conf import conf


class DBInit(object):

    def __init__(self):
        pass

    db_config = {
        'host': conf.db_server01,
        'user': 'cloudsvc',
        'passwd': 'cloudsvc',
        'db': 'servicedata',
        'charset': 'UTF8',
        'port': conf.db_port
    }
    try:
        engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=%s' % (db_config['user'],
                                                                      db_config['passwd'],
                                                                      db_config['host'],
                                                                      db_config['port'],
                                                                      db_config['db'],
                                                                      db_config['charset'],
                                                                      ), echo=True)
    except Exception, e:
        log.error('connect the database error, please check')
        raise Exception('connect the database error, please check')

    metadata = MetaData(engine)

    font_service = Table('font_service', metadata,
                         Column('uuid', String(64), primary_key=True),
                         Column('user_uuid', String(64)),
                         Column('team_uuid', String(64)),
                         Column('project_uuid', String(64)),
                         Column('service_uuid', String(64)),
                         Column('rc_uuid', String(64)),
                         Column('service_name', String(64)),
                         Column('service_status', String(20)),
                         Column('description', String(320)),
                         Column('lifecycle', String(64)),
                         Column('image_dir', String(200)),
                         Column('certify', Integer),
                         Column('service_create_time', DateTime, server_default=func.now()),
                         Column('service_update_time', DateTime, server_default=func.now())
                         )

    rc_table = Table('replicationcontrollers', metadata,
                     Column('uuid', String(64), primary_key=True),
                     Column('labels_name', String(64)),
                     Column('pods_num', Integer),
                     Column('image_id', String(64)),
                     Column('cm_format', String(32)),
                     Column('container_cpu', String(64)),
                     Column('container_memory', String(64)),
                     Column('policy', Integer),
                     Column('auto_startup', Integer),
                     Column('command', String(320)),
                     Column('image_name', String(320)),
                     Column('isUpdate', Integer),
                     Column('rc_create_time', DateTime, server_default=func.now()),
                     Column('rc_update_time', DateTime, server_default=func.now())
                     )

    container = Table('containers', metadata,
                      Column('uuid', String(64), primary_key=True),
                      Column('rc_uuid', String(64)),
                      Column('container_port', Integer),
                      Column('protocol', String(32)),
                      Column('access_mode', String(32)),
                      Column('access_scope', String(32)),
                      Column('tcp_port', String(32)),
                      Column('http_domain', String(64)),
                      Column('cname', String(64)),
                      Column('tcp_domain', String(64)),
                      Column('private_domain', String(64)),
                      Column('identify', String(32))
                      )

    env = Table('env', metadata,
                Column('uuid', String(64), primary_key=True),
                Column('rc_uuid', String(64)),
                Column('env_key', String(32)),
                Column('env_value', String(32))
                )

    acl = Table('resources_acl', metadata,
                Column('resource_uuid', String(64), primary_key=True),
                Column('resource_type', String(64)),
                Column('admin_uuid', String(64)),
                Column('team_uuid', String(64)),
                Column('project_uuid', String(64)),
                Column('user_uuid', String(64)),
                Column('create_time', DateTime, server_default=func.now()),
                Column('update_time', DateTime, server_default=func.now())
                )

    logic = Table('logic', metadata,
                  Column('service_uuid', String(64)),
                  Column('delete_time', DateTime, server_default=func.now()))

    volume = Table('volume', metadata,
                   Column('uuid', String(64), primary_key=True),
                   Column('rc_uuid', String(64)),
                   Column('volume_uuid', String(64)),
                   Column('disk_path', String(64)),
                   Column('readonly', String(32), server_default='True')
                   )

    certify = Table('certify', metadata,
                    Column('uuid', String(64), primary_key=True),
                    Column('crt',  mysql.MSMediumText),
                    Column('tls_key', mysql.MSMediumText),
                    Column('certify_create_time', DateTime, server_default=func.now()))

    metadata.create_all(engine)

    Table('replicationcontrollers', metadata, autoload=True)
    Table('font_service', metadata, autoload=True)
    Table('containers', metadata, autoload=True)
    Table('env', metadata, autoload=True)
    Table('volume', metadata, autoload=True)
    Table('logic', metadata, autoload=True)
    Table('resources_acl', metadata, autoload=True)
