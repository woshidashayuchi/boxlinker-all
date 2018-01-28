# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/06
import sys
p_path = sys.path[0] + '/../..'
p_path1 = sys.path[0] + '/..'
sys.path.append(p_path)
sys.path.append(p_path1)
from restapi_register import rest_app_run


if __name__ == "__main__":
    rest_app_run()
