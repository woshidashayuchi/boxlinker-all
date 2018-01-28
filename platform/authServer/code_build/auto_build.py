#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/9/27 14:48
"""

import sys
import os
import time
import subprocess
import sys

import shutil


from authServer.tools.es_log import send_log

from authServer.pyTools.decode.ctools import random_str

from authServer.pyTools.tools.timeControl import get_now_time

from authServer.pyTools.tools.mysqloperate import mysqlOperation
from authServer.conf.db import hub_db


# # 构建状态 1:构建成功, 2:构建构建中,  3:构建失败  build_status
update_status = """UPDATE image_repository_build SET build_status=%(build_status)s WHERE image_repository_id=%(build_pro_id)s;"""
update_last_build = """UPDATE image_repository_build SET last_build=%(last_build)s WHERE image_repository_id=%(build_pro_id)s;"""
update_use_time = """UPDATE image_repository_build SET use_time=%(use_time)s WHERE image_repository_id=%(build_pro_id)s;"""


update_status_last_build = """UPDATE image_repository_build SET build_status=%(build_status)s,
last_build=%(last_build)s WHERE image_repository_id=%(build_pro_id)s;"""


update_status_use_time = """UPDATE image_repository_build SET build_status=%(build_status)s,
use_time=%(use_time)s WHERE image_repository_id=%(build_pro_id)s;"""


update_status_last_build_use_time = """UPDATE image_repository_build SET build_status=%(build_status)s,
use_time=%(use_time)s, last_build=%(last_build)s WHERE image_repository_id=%(build_pro_id)s;"""

def child(kwargs, pipe_name):

    db = hub_db()
    DBOP = mysqlOperation(host=db.host, user=db.user, passwd=db.pawd, port=db.port, db=db.cydb, debug=True)

    # 开始时间
    begin_time = time.time()


    docker_file = kwargs['dockerfile_name']
    image_name = kwargs['images_name']
    user_name = kwargs['user_name']
    image_tag = kwargs['image_tag']
    github_repo_id = kwargs['id']


    # 更新状态
    # # 构建状态 1:构建成功, 2:构建构建中,  3:构建失败
    args_d = dict()
    args_d['build_pro_id'] = github_repo_id
    args_d['build_status'] = '2'
    args_d['last_build'] = get_now_time()

    print 'last_build'
    print args_d['last_build']

    DBOP.InsertOrUpdateBySql(update_status_last_build, args_d)



    # 日志索引
    labels_logs = 'auto_build-' + str(user_name) + '-' + str(github_repo_id)

    repo_path = sys.path[0] + '/' + kwargs['git_name'] + '-' + random_str(8) + '/' + kwargs['repo_name']\

    # clone 代码地址
    repo_url = 'git@github.com:' + kwargs['git_name'] + '/' + kwargs['repo_name'] + '.git'

    if os.path.exists(path=repo_path):
        shutil.rmtree(repo_path)

    git_cmd = 'git clone ' + repo_url + ' ' + repo_path

    try:
        pipeout = os.open(pipe_name, os.O_WRONLY)
        os.write(pipeout, '--> git clone begin: ' + git_cmd + '\n')

        ps = subprocess.Popen(git_cmd, shell=True, bufsize=0, stdin=subprocess.PIPE,
                              stdout=pipeout, stderr=pipeout)
        retcode = ps.wait()
        if str(retcode) == '0':
            os.write(pipeout, '--> git clone is ok' + '\n')
    except Exception as msg:
        print msg.message
        print msg.args

        os.write(pipeout, '--> git clone is error ' + '\n')
        args_d['build_status'] = '3'
        args_d['use_time'] = str(time.time() - begin_time)
        DBOP.InsertOrUpdateBySql(update_status_last_build_use_time, args_d)
        return True

    docker_path = repo_path + kwargs['dockerfile_path']

    if os.path.exists(docker_path) is False:
        os.write(pipeout, 'error: --> git clone scr file is not exists ' + '\n')
        return False


    try:
        # imagename_demo = 'index.boxlinker.com/{0}/{1}:{2}'
        # imagename = imagename_demo.format(user_name, image_name, image_tag)
        # 20161009 修改镜像命名逻辑
        imagename_demo = 'index.boxlinker.com/{0}:{1}'
        imagename = imagename_demo.format(image_name, image_tag)

        docker_build_cmd_demo = 'docker build -t {0} {1}'
        # docker_build_cmd_demo = 'docker build --no-cache -t {0} {1}'
        docker_build_cmd = docker_build_cmd_demo.format(imagename, docker_path)

        os.write(pipeout, '--> docker build begin: ' + str(imagename) + '\n')
        os.write(pipeout, '--> docker build cmd  : ' + str(docker_build_cmd) + '\n')

        ps = subprocess.Popen(docker_build_cmd, shell=True, bufsize=0, stdin=subprocess.PIPE,
                              stdout=pipeout, stderr=pipeout)
        retcode = ps.wait()

        if str(retcode) == '0':
            os.write(pipeout, '--> docker build is ok: ' + '\n')
    except Exception as msg:
        print msg.message
        print msg.args
        os.write(pipeout, '--> docker build is error: ' + '\n')

        args_d['build_status'] = '3'
        args_d['use_time'] = str(time.time() - begin_time)
        DBOP.InsertOrUpdateBySql(update_status_last_build_use_time, args_d)
        return True

    try:
        image_push = 'docker push {0}'.format(imagename)
        os.write(pipeout, '--> push image begin: ' + image_push + '\n')
        ps = subprocess.Popen(image_push, shell=True, bufsize=0, stdin=subprocess.PIPE,
                              stdout=pipeout, stderr=pipeout)
        retcode = ps.wait()
        if str(retcode) == '0':
            os.write(pipeout, 'docker push is ok: ' + image_push + '\n')
            os.write(pipeout, ' ---- An automated build all three steps completed successfully ---- ' + '\n')

        args_d['build_status'] = '1'
    except Exception as msg:
        print msg.message
        print msg.args

        os.write(pipeout, 'docker push is error: ' + image_push + '\n')
        args_d['build_status'] = '3'
    finally:
        # 更新状态
        # 构建状态 1:构建成功, 2:构建构建中,  3:构建失败

        args_d['use_time'] = str(time.time() - begin_time)
        DBOP.InsertOrUpdateBySql(update_status_last_build_use_time, args_d)


def parent(kwargs, pipe_name):
    """
    :param pipe_name:    管道名字
    :param logfunc:      处理日志的函数
    :return:
    """

    user_name = kwargs['user_name']
    github_repo_id = kwargs['id']

    # 日志索引
    labels_logs = 'auto_build-' + str(user_name) + '-' + str(github_repo_id)

    log_masg = dict()
    log_masg['user_name'] = user_name
    log_masg['labels_logs'] = labels_logs
    pipein = open(pipe_name, 'r')
    ret = False

    log_n = random_str(8)  # 测试用, 稳定之后删除
    fp_temp = open(log_n + '.log', 'a+')  # 测试用, 稳定之后删除
    while True:
        line = pipein.readline().strip()
        if line == '':
            continue

        log_masg['log_info'] = line

        # 测试用, 稳定之后删除
        fp_temp.writelines(line + '\n')
        fp_temp.flush()
        # 测试用, 稳定之后删除

        send_log(log_masg)

    fp_temp.close()   # 测试用, 稳定之后删除

    return ret


def auto_build_two(kwargs):
    print kwargs

    pid = os.fork()

    user_name = kwargs['user_name']
    r_str = random_str(le=8)

    pipe_name = 'pipe_' + user_name + '_' + r_str

    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)

    if pid != 0:
        parent(kwargs=kwargs, pipe_name=pipe_name)
    else:
        child(kwargs=kwargs, pipe_name=pipe_name)



