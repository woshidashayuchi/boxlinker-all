#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/8 10:25
"""



from enum import Enum, unique

@unique
class unActionCode(Enum):
    FindPassword = 100  # 找回密码

    VerifyEmail = 200  # 验证邮箱




if __name__ == '__main__':
    print unActionCode.FindPassword.value
    print unActionCode.FindPassword.name

    ss = unActionCode(100)

    print ss
    print ss.name
    print type(ss.name)
    print dir(ss)

