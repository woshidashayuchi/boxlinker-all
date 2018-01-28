# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/3 下午4:34

from common.logs import logging as log

from allow_all import AllowAll


if __name__ == '__main__':
    all = AllowAll()
    try:
        all.mains()
    except Exception, e:
        log.error('error......reason is: %s' % e)
