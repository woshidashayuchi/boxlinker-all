#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/20 15:02
"""

from imageAuth.db.image_repo import ImageRepositoryDb


from imageAuth.manager import images_manage, user_manage


from imageAuth.db.db import Session

class ImageRepoRpcAPI(object):

    def __init__(self):
        self.images_manage = images_manage.ImageRepoManager()
        self.usercenter = user_manage.UcenterManager()
        self.db_session = Session()

    def test_image_repo_public(self, page=1, page_size=10):
        return self.images_manage.image_repo_public(self.db_session, page, page_size)

if __name__ == '__main__':
    IRRA = ImageRepoRpcAPI()
    print IRRA.test_image_repo_public()