# -*- coding: utf-8 -*-


import logging



try:
    from pyTools.conf import conf

    filename = conf.log_file
except ImportError, e:
    filename = '/var/log/tloud.log'

logging.basicConfig(
    level=logging.INFO,
    filename=filename,
    format=('%(asctime)s '
            '[%(levelname)s] '
            '[%(filename)s line:%(lineno)d] '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
)