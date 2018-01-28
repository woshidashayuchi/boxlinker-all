#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/9 下午1:39
"""

import sys
import os
import time
import subprocess
#from gittle import Gittle, GittleAuth

import sys

import shutil

from authServer.tools.pipe_tool import run, test_func

from authServer.tools.es_log import send_log

from authServer.pyTools.decode.ctools import random_str


def git_clone(repo_path, repo_url, user_name, labels_logs):

    if os.path.exists(path=repo_path):
        shutil.rmtree(repo_path)
    #repo = Gittle.clone(repo_url, repo_path)

    cmd_demp = 'git clone ' + repo_url + ' ' + repo_path

    log_masg = dict()
    log_masg['log_info'] = cmd_demp
    log_masg['user_name'] = user_name
    log_masg['labels_logs'] = labels_logs

    send_log(log_masg)

    pipe_name = 'pipe_'+ user_name + '_' + random_str(le=6)
    cmd_is_error = pipe_name + ' git clone is error'
    cmd_is_ok = pipe_name + ' git clone is ok'
    ret = run(cmdstr=cmd_demp, pipe_name=pipe_name, cmd_is_error=cmd_is_error, cmd_is_ok=cmd_is_ok, logfunc=send_log, user_name=user_name,
              logfuncargs={"user_name": user_name, "labels_logs": labels_logs})

    return True


def docker_build(docker_path, docker_file, image_name, user_name, image_tag, labels_logs):
    #cmdstr = 'docker build -t  python:test_test /Users/liuzp/temp/Dockerfile/python/2.7.10'

    #imagename_demo = 'index.boxlinker.com/python:2.7.10-ubuntu-flask_apache'
    log_masg = dict()

    log_masg['user_name'] = user_name
    log_masg['labels_logs'] = labels_logs

    if os.path.exists(docker_path) is False:
        log_masg['log_info'] = ' no docker path '
        send_log(log_masg)
        return False, None



    log_masg['log_info'] = ' no docker path '
    imagename_demo = 'index.boxlinker.com/{0}/{1}:{2}'
    imagename = imagename_demo.format(user_name, image_name, image_tag)

    log_masg['log_info'] = ' --- docker_build begin ---: ' + str(imagename)
    send_log(log_masg)

    cmd_demo = 'docker build -t {0} {1}'
    cmd_str = cmd_demo.format(imagename, docker_path)

    pipe_name = 'pipe_'+ user_name + '_' + random_str(le=6)
    cmd_is_error = pipe_name + ' docker build is error'
    cmd_is_ok = pipe_name + ' docker build is ok'

    ret = run(cmdstr=cmd_str, pipe_name=pipe_name, cmd_is_error=cmd_is_error, cmd_is_ok=cmd_is_ok, logfunc=send_log, user_name=user_name,
              logfuncargs={"user_name": user_name, "labels_logs": labels_logs})

    if ret is True:
        log_masg['log_info'] = ' --- docker build is ok --- '
        send_log(log_masg)
    else:
        log_masg['log_info'] = ' --- docker build is error --- '
        send_log(log_masg)
    return ret, imagename



def docker_push(imagename, user_name, labels_logs):
    do_num = 3

    log_masg = dict()

    log_masg['user_name'] = user_name
    log_masg['labels_logs'] = labels_logs

    log_masg['log_info'] = ' --- push image begin: --- '

    send_log(log_masg)
    image_push = 'docker push {0}'.format(imagename)

    pipe_name = pipe_name = 'pipe_'+ user_name + '_' + random_str(le=6)
    cmd_is_error = pipe_name + ' docker push is error'
    cmd_is_ok = pipe_name + ' docker push is ok'

    while do_num > 0:

        ret = run(cmdstr=image_push, pipe_name=pipe_name, cmd_is_error=cmd_is_error, cmd_is_ok=cmd_is_ok,
                  logfunc=send_log, user_name=user_name, logfuncargs={"user_name": user_name, "labels_logs": labels_logs})

        if ret is False:
            do_num -= 1
            return False
        do_num = 0

    log_masg['log_info'] = ' --- push image is ok: --- '

    send_log(log_masg)

    return True




def auto_build(kwargs):

    print kwargs
    print type(kwargs)

    github_repo_id = kwargs['id']

    repo_path = sys.path[0] + '/' + kwargs['git_name'] + '-' + random_str(8) + '/' + kwargs['repo_name']
    repo_url = 'git@github.com:' + kwargs['git_name'] + '/' + kwargs['repo_name'] + '.git'

    user_name = kwargs['user_name']

    # auto_build-UserName-ProNameId
    labels_logs = 'auto_build-' + str(user_name) + '-' + str(github_repo_id)

    git_clone(repo_path=repo_path, repo_url=repo_url, user_name=user_name, labels_logs=labels_logs)



    docker_path = repo_path + kwargs['dockerfile_path']
    ret_bool, imagename = docker_build(docker_path=docker_path, docker_file=kwargs['dockerfile_name'],
                                       image_name=kwargs['images_name'], user_name=kwargs['user_name'],
                                       image_tag=kwargs['image_tag'], labels_logs=labels_logs)


    print 'bbbsuisis'
    print imagename
    print ret_bool

    if ret_bool:
        docker_push(imagename, user_name=user_name, labels_logs=labels_logs)


if __name__ == '__main__':



    repo_path = sys.path[0] + '/testrepo'


    git_clone(repo_path, 'git@github.com:liuzhangpei/webhook_test.git', user_name='boxlinker', labels_logs='auto_build-boxlinker-12')


    # repo_path, repo_url
    exit(-1)


    auto_build()




