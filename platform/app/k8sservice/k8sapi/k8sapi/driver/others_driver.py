# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/3/20 下午3:34

from common.logs import logging as log


class OthersDriver(object):
    def __init__(self):
        pass

    @staticmethod
    def paging_driver(query_list, page_size, page_num):
        if page_size is None or page_num is None:
            return len(query_list), query_list
        else:
            page_size = int(page_size)
            page_num = int(page_num)

        count = len(query_list)

        if count == 0:
            return count, []
        else:
            if count <= page_size:
                return count, query_list
            else:
                query_list = query_list[(page_num-1)*page_size:]
                if len(query_list) <= page_size:
                    return count, query_list
                else:
                    query_list = query_list[:page_size]

                    return count, query_list
