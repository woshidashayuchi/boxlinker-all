#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: livenowhy@hotmail.com
@time: 2016/3/22 15:55
"""

import os
import sys
import time

import pexpect

from pyStudy.file import remove_file, get_path_file_list

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def do_nothing(file, isok=True):
    print file
    pass


def scp_file(ip, user, passwd, dst_path, filename, dosome=do_nothing):
    """
    :param ip:   远端服务器地址
    :param user:
    :param passwd:
    :param dst_path:   远端文件地址
    :param filename:
    :param dosome:  完成之后对文件做处理
    :return:
    """

    if os.path.exists(filename) is False:
        print "location file is no exists"
        return False

    retbool = True
    pass_key = '.*assword.*'
    if os.path.isdir(filename):
        # scp -r backxml guest@www.livenowhy.com:/home/guest
        cmdline = 'scp -r %s %s@%s:%s' % (filename, user, ip, dst_path)
    else:
        cmdline = 'scp %s %s@%s:%s' % (filename, user, ip, dst_path)

    try:
        print cmdline

        scplog = file('scp.log', 'a')  # set log w write /a append

        child = pexpect.spawn(cmdline, timeout=None)

        child.logfile = scplog  # set log
        child.logfile_send = sys.stdout   # set log

        child.expect(pass_key)
        child.sendline(passwd)
        child.expect(pexpect.EOF)
        if child.echo:
            print "is return True uploading"
        # child.interact()
        # child.read()
        # child.expect('$')
        dosome(filename, child.echo)
        retbool = child.echo
    except Exception as msg:
        for val in msg.args:
            print val
        print "upload faild!"
        retbool = False
    finally:
        return retbool


def scp_file_name_by_time(SCPS, time_name=True):
    """
    :param SCPS:  远端服务器配置
    :param time_name:  是否按时间在远端服务器重命名文件
    :return:
    """

    if time_name:
        time_sec = time.time()
        dd = time.strftime("%Y-%m-%d", time.localtime(time_sec))
        filename = dd + '-' + str(time_sec)
        dst_name = SCPS.dst_path + filename
    else:
        dst_name = SCPS.dst_path

    # 删除文件
    scp_file(ip=SCPS.ip, user=SCPS.user, passwd=SCPS.passwd, dst_path=dst_name,
             filename=SCPS.filename, dosome=remove_file)

    # 保留原始扫描报告
    # scp_file(ip=SCPS.ip, user=SCPS.user, passwd=SCPS.passwd, dst_path=dst_name,
    #          filename=SCPS.filename)


def del_remote_file(host, user, password, targetfile, dosome=do_nothing):
    """
    删除远端服务器的文件
    ssh root@10.1.4.96 'rm -rf /home/liuzhangpei/del/111.46.181.0--24.xml'
    :param host:   远端服务器地址
    :param user:   远端服务器用户名
    :param password: 密码
    :param targetfile: 远端目标文件
    :param dosome:
    :return:
    """

    cmdline = """ssh $USER@$HOST 'rm -rf $TARGTFILE'"""

    cmdline = cmdline.replace('$USER', user).replace('$HOST', host).replace('$TARGTFILE', targetfile)

    retbool = True

    answer_mt = '.*(yes/no).*'

    pass_mt = '.*assword.*'

    answer_rsa = '.*SA key fingerprint.*'

    try:

        scplog = file('scp.log', 'a')  # set log w write /a append

        child = pexpect.spawn(cmdline, timeout=None)

        child.logfile = scplog  # set log
        child.logfile_send = sys.stdout   # set log

        while True:

            i = child.expect([answer_mt, pass_mt, answer_rsa, pexpect.EOF])

            if i == 0:
                child.sendline('yes')
            elif i == 1:
                child.sendline(password)
            elif i == 2:
                child.sendline('yes')
            elif i == 3:
                break


        if child.echo:
            print "is return True uploading"
        child.interact()
        child.read()
        # dosome(filename, child.echo)
        retbool = child.echo
    except Exception as msg:
        for val in msg.args:
            print val
        print "upload faild!"
        retbool = False
    finally:
        return retbool



def scp_remote_file(host, user, password, targetfile, localfile, targe='file'):
    """
    把远端服务器的文件，拷贝到本地
    scp root@10.1.4.97:/home/liuzhangpei/backxml/*.xml .
    :param host:   远端服务器地址
    :param user:   远端服务器用户名
    :param password: 密码
    :param targetfile: 远端目标文件
    :param localfile: 本地存放文件
    :param targe: 目标是文件夹还是  单个文件
    :return:
    """

    if targe == 'file':
        cmdline = """scp $USER@$HOST:$TARGTFILE $LOCALFILE"""
    elif targe == 'path':
        cmdline = """scp -r $USER@$HOST:$TARGTFILE $LOCALFILE"""
    else:
        return False

    cmdline = cmdline.replace('$USER', user).replace('$HOST', host)\
        .replace('$TARGTFILE', targetfile).replace('$LOCALFILE', localfile)

    retbool = True

    answer_mt = '.*(yes/no).*'
    answer_rsa = '.*SA key fingerprint.*'
    pass_mt = '.*assword.*'

    p_denied = '.*Permission denied.*'
    arg_tooLong = 'Argument list too long'  # bash: /usr/bin/scp: Argument list too long  退出

    try:

        scplog = file('scp.log', 'a')  # set log w write /a append

        print cmdline

        child = pexpect.spawn(cmdline, timeout=None)

        child.logfile = scplog  # set log
        child.logfile_send = sys.stdout   # set log

        p_denied_t = False

        while True:
            i = child.expect([answer_mt, answer_rsa, pass_mt, p_denied, arg_tooLong, pexpect.EOF])

            if i == 0:
                child.sendline('yes')
            elif i == 1:
                child.sendline('yes')
            elif i == 2:
                child.sendline(password)
            elif i == 3:
                child.sendcontrol('c')
                p_denied_t = True
            elif i == 4:
                print 'Argument list too long'
                retbool = False
                return False
            elif i == 5:
                break

        child.interact()
        child.read()
        # dosome(filename, child.echo)

        print 'ssssss'
        if child.echo:
            print "is return True uploading"

        if p_denied_t:
            print user + '@' + host + '----Permission denied, please try again.'
        retbool = child.echo
    except Exception as msg:
        for val in msg.args:
            print val
        print "upload faild!"
        retbool = False
    finally:
        return retbool


def scp_remote_file_and_del(host, user, password, targetfile, localfile, delete=True):
    """
    对于单个文件夹下含有许多文件，并且远端服务器下该文件夹下的文件可能随时增加
    1.先吧远端服务器的文件 拷贝到本地
    2.再删除远端服务器的文件
    :param host:
    :param user:
    :param password:
    :param targetfile:
    :param localfile: 最好是随机新生成的文件
    :return:
    """

    if scp_remote_file(host, user, password, targetfile, localfile):  # 拷贝单个文件
        print 'scp is ok'


    filelist = get_path_file_list(localfile)


    if delete is False:
        return True


    dirname = os.path.dirname(targetfile)

    for nodefile in filelist:
        filename = os.path.basename(nodefile)
        targetfilename = dirname + os.sep + filename
        del_remote_file(host, user, password, targetfilename)

        #(host, user, password, targetfile, dosome=do_nothing):


def RegularMoveFile(host, user, password, targetfile, localpath, delete=True):
    """
    在本地文件目录下创建一个新的文件夹，用来存放从远端拷贝的文件
    :param host: 远端主机
    :param user: 远端用户名
    :param password: 密码
    :param targetfile: 远端文件
    :param localpath: 存放本地文件地址
    :return:
    """

    time_sec = time.time()
    dd = time.strftime("%Y-%m-%d", time.localtime(time_sec))
    filename = dd + '-' + str(time_sec)
    dst_name = filename + '-' + host

    dst_path = localpath + os.sep + dst_name

    if os.path.exists(dst_path) is False:
        #os.mkdir(dst_path)
        os.makedirs(dst_path)  # 创建多层目录


    scp_remote_file_and_del(host=host, user=user, password=password, targetfile=targetfile, localfile=dst_path, delete=delete)

    localfilelist = get_path_file_list(dst_path)

    if len(localfilelist) <= 0:
        os.removedirs(dst_path)


def parse_conf_scp(path, delete=True):
    """
    读取ssh主机的配置
    :param path: ssh 用户密码配置
    :param delete: 拷贝成功是否删除远端服务器的文件
    :return:
    """
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception, e:
        print e.message
        return False

    for server in root.findall('server'):
        host = server.find('host').text
        user = server.find('user').text
        password = server.find('password').text
        targetfile = server.find('targetfile').text
        localfile = server.find('localfile').text

        RegularMoveFile(host=host, user=user, password=password,
                        targetfile=targetfile, localpath=localfile, delete=delete)


# ssh sourceHostname 'find ~/sourceDir -type f -name "*.txt" | tar czf archive.tar.gz --files-from -'
# rsync - aP sourceHostname: / path / to / archive.tar.gz / dest

if __name__ == '__main__':
    parse_conf_scp(path=r'/home/love/PythonTools/configure/ssh_key/ssh_test.xml', delete=False)