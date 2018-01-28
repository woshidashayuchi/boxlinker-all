# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/31 下午6:11

import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.append(p_path)
sys.path.append(p_path1)
from manager.recover_manager import RecoverManager
from time import sleep


def run_app():
    while True:
        recover = RecoverManager()
        recover.recover_manager()
        recover.delete_in30_days()
        sleep(3600)

if __name__ == '__main__':
    run_app()
