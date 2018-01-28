#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016/8/9
# Author:wang-xf

import json
import time
import requests
from now_time import get_timestamp_13


def get_index(json_list, log_info):
    log_dict = {
        "time": get_timestamp_13(),
        "level": "INFO",
        "log": {
            "userid": json_list.get('user_uuid'),
            "log_info": log_info
        }
    }
    return log_dict
