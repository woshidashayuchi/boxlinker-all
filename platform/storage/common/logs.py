# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import logging


try:
    from conf import conf

    if conf.log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif conf.log_level == 'INFO':
        log_level = logging.INFO
    elif conf.log_level == 'WARNING':
        log_level = logging.WARNING
    elif conf.log_level == 'ERROR':
        log_level = logging.ERROR
    else:
        log_level = logging.INFO

    log_file = conf.log_file
except Exception:
    log_level = logging.WARNING
    log_file = '/var/log/cloud.log'

logging.basicConfig(
    level=log_level,
    filename=log_file,
    format=('%(asctime)s '
            '[%(levelname)s] '
            '[%(filename)s line:%(lineno)d] '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
    )

# console = logging.StreamHandler()
# console.setLevel(log_level)
# formatter = logging.Formatter(
#    ('{"time": \"%(asctime)s\", '
#     '"level": \"%(levelname)s\", '
#     '"file": \"%(filename)s line:%(lineno)d\", '
#     '"log": \"%(message)s\"}'),
#    datefmt='%Y-%m-%d %H:%M:%S')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)
