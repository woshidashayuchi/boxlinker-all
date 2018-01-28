#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '/logtest')

from common.logs import logging as log


def test_log():

    while True:
        log.info('{"userid": "boxlinker", "log_info": "log test"}')
        sleep(5)


if __name__ == '__main__':
    test_log()
