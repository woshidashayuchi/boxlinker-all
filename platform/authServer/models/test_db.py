#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/15 下午6:31
"""



import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import authServer.conf.db as DB



# 创建对象的基类:
Base = declarative_base()


mysql_engine = "mysql://root:root123admin@192.168.1.6:3306/registry?charset=utf8"

engine = create_engine(mysql_engine, echo=True)

def init_create_hub_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
    # 否则你就必须在调用 init_db() 之前导入它们。
    print "init_create_hub_db"
    Base.metadata.create_all(bind=engine, checkfirst=True)


init_create_hub_db()


Session = sessionmaker(bind=engine)


