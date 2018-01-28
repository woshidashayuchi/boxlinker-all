#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/18 17:39
"""

from enum import Enum, unique


@unique
class Role(Enum):
    owner = '0'   # 拥有者
    admin = '1'    # 管理员
    developer = '2'  # 开发者
    guest = '3'        # 观察者


@unique
class OrgaRole(Enum):
    SystemGod = 100  # 系统管理员       0

    OrgaMaster = 200  # 群主;组织拥有者  1

    OrgaAdmin = 210   # 群管理员        1

    OrgaDevelop = 400  # 群开发者       2



@unique
class AccessCode(Enum):
    O = 0  # owners  拥有者
    M = 1  # Management 管理资源
    R = 2  # Read 读
    W = 3  # Write 写
    D = 4  # Delete 删除
    S = 5  # Search 搜索

if __name__ == '__main__':
    print OrgaRole.SystemGod.value
    print OrgaRole.SystemGod.name

    ss = OrgaRole(100)

    print ss
    print ss.name
    print type(ss.name)
    print dir(ss)

    print dir(AccessCode.D)
