#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@func: 实时获取终端执行输出
"""

import os
import time
import sys
import subprocess

def child(pipe_name, cmdstr, cmd_is_error, cmd_is_ok):
    try:
        pipeout = os.open(pipe_name, os.O_WRONLY)
        ps = subprocess.Popen(cmdstr, shell=True, bufsize=0, stdin=subprocess.PIPE,
                              stdout=pipeout, stderr=pipeout)
        retcode = ps.wait()

        if str(retcode) == '0':
            os.write(pipeout, cmd_is_ok + '\n')
    except Exception as msg:
        os.write(pipeout, msg.message + '\n')
        os.write(pipeout, cmd_is_error + '\n')



def parent(pipe_name, logfunc, user_name, cmd_is_error, cmd_is_ok, logfuncargs):
    """
    :param pipe_name:    管道名字
    :param logfunc:      处理日志的函数
    :param pipe_w_stop:  写管道终止信息
    :return:
    """
    pipein = open(pipe_name, 'r')
    ret = False
    while True:
        line = pipein.readline().strip()
        if line == '':
            continue

        if cmd_is_error == line:
            logfuncargs['log_info'] = line
            logfunc(logfuncargs)
            break

        if cmd_is_ok == line:
            logfuncargs['log_info'] = line
            logfunc(logfuncargs)
            ret = True
            break

        logfuncargs['log_info'] = line
        logfunc(logfuncargs)
    return ret



def test_func(var, var1):
    print var, var1


def run(pipe_name, cmd_is_error, cmd_is_ok, logfunc, user_name, cmdstr, logfuncargs):

    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)
    pid = os.fork()
    if pid != 0:
        ret = parent(pipe_name=pipe_name, logfunc=logfunc, cmd_is_error=cmd_is_error, cmd_is_ok=cmd_is_ok,
                     user_name=user_name, logfuncargs=logfuncargs)
        return ret
    else:
        child(pipe_name=pipe_name, cmdstr=cmdstr, cmd_is_error=cmd_is_error, cmd_is_ok=cmd_is_ok)




if __name__ == '__main__':

    pipe_name = 'pipe_test'
    pipe_w_stop = pipe_name + ' is stop write'
    cmd_is_ok = pipe_name + ' is ok'

    repo_path = sys.path[0] + '/testrepo'

    cmd_demp = 'git clone ' + 'git@github.com:liuzhangpei/homepage.git' + ' ' + repo_path

    cmd_demp = 'docker push index.boxlinker.com/boxlinker/webhook_test_test:auto_2'
    print run(cmdstr=cmd_demp, pipe_name=pipe_name, pipe_w_stop=pipe_w_stop, cmd_is_ok=cmd_is_ok,
              user_name='boxlinker',
              logfunc=test_func, logfuncargs={"user_name": 'boxlinker', "log": "log"})