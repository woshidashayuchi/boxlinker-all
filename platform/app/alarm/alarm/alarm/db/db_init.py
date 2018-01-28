# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/4/21 下午4:40


from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import String, Column, Integer
from sqlalchemy import DateTime
from sqlalchemy import Float
from common.logs import logging as log
from conf import conf


class DBInit(object):

    def __init__(self):
        pass

    db_config = {
        'host': conf.db_server01,
        'user': 'cloudalarm',
        'passwd': 'cloudalarm',
        'db': 'monitor_alarm',
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

    alarm = Table('alarming', metadata,
                  Column('uuid', String(64), primary_key=True),
                  Column('user_uuid', String(64)),
                  Column('wise', Integer),   # 0为横向,1为纵向
                  Column('cpu_value', Float),
                  Column('memory_value', Float),
                  Column('network_value', Float),
                  Column('storage_value', Float),
                  Column('time_span', String(32)),
                  Column('alarm_time', DateTime),
                  Column('email', String(64)),
                  Column('phone', String(64)),
                  Column('update_time', DateTime, server_default=func.now()))

    alarm_service_rules = Table('alarm_service_rules', metadata,
                                Column('uuid', String(64), primary_key=True),
                                Column('alarm_uuid', String(64)),
                                Column('service_uuid', String(64)),
                                Column('email', String(64)),
                                Column('phone', String(32)))

    alarm_step_record = Table('alarm_step_record', metadata,
                              Column('uuid', String(64), primary_key=True),
                              Column('alarm_type', String(32)),
                              Column('send_or_not', Integer),
                              Column('last_send_time', DateTime))
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
    metadata.create_all(engine)

