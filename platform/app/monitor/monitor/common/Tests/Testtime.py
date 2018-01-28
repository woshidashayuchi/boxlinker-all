#!/usr/bin/env python

import sys


sys.path.insert(1, '../..')

from time import sleep
from common.logs import logging as log
from common.time_log import time_log

@time_log
def test_log():

    sleep(3)
    log.debug('log test')

    return

if __name__ == '__main__':
    test_log()
