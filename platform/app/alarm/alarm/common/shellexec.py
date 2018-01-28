# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

# 执行shell工具模块

import os
import shlex
import subprocess

from common.logs import logging as log


def execute(*cmd, **kwargs):
    """Helper method to shell out and execute a command through subprocess.

    Allows optional retry.

    :param cmd:             Passed to subprocess.Popen.
    :type cmd:              string
    :param cwd:             Set the current working directory
    :type cwd:              string
    :param process_input:   Send to opened process.
    :type process_input:    string
    :param env_variables:   Environment variables and their values that
                            will be set for the process.
    :type env_variables:    dict
    :param run_as_root:     True | False. Defaults to False. If set to True,
                            the command is prefixed by the command specified
                            in the root_helper kwarg.
    :type run_as_root:      boolean
    :param root_helper:     command to prefix to commands called with
                            run_as_root=True
    :type root_helper:      string
    :param shell:           whether or not there should be a shell used to
                            execute this command. Defaults to false.
    :type shell:            boolean
    """

    cwd = kwargs.pop('cwd', None)
    process_input = kwargs.pop('process_input', None)
    env_variables = kwargs.pop('env_variables', None)
    run_as_root = kwargs.pop('run_as_root', False)
    root_helper = kwargs.pop('root_helper', '')
    shell = kwargs.pop('shell', False)

    if kwargs:
        return 'config parameter error'

    if run_as_root and hasattr(os, 'geteuid') and os.geteuid() != 0:
        if not root_helper:
            log.error('Command requested root, but did not '
                      'specify a root helper.')
        if shell:
            # root helper has to be injected into the command string
            cmd = [' '.join((root_helper, cmd[0]))] + list(cmd[1:])
        else:
            # root helper has to be tokenized into argument list
            cmd = shlex.split(root_helper) + list(cmd)

    cmd = [str(c) for c in cmd]

    try:
        _PIPE = subprocess.PIPE  # pylint: disable=E1101

        # 如果把preexec_fn设置为一个可调用的对象（比如函数），就会在子进程被执行前被调用。
        preexec_fn = None
        close_fds = True

        obj = subprocess.Popen(cmd,
                               stdin=_PIPE,
                               stdout=_PIPE,
                               stderr=_PIPE,
                               close_fds=close_fds,
                               preexec_fn=preexec_fn,
                               shell=shell,
                               cwd=cwd,
                               env=env_variables)

        result = obj.communicate(process_input)

        obj.stdin.close()  # pylint: disable=E1101
        _returncode = obj.returncode  # pylint: disable=E1101
        log.debug('CMD "%s" returned: %s' % (cmd, _returncode))

        return (result, _returncode)

    except Exception, e:
        log.error('CMD exec error, cmd = %s, reason=%s' % (cmd, e))
