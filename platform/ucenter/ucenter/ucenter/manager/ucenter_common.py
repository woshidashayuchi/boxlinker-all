# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.md5_encrypt import md5_encrypt


def passwd_encrypt(user_name, password, salt):

    str1 = '%s%s' % (str(user_name), str(salt))
    str2 = md5_encrypt(str1)[0:8]
    str3 = md5_encrypt(str2)[8:16]
    str4 = md5_encrypt(str3)[16:24]
    str5 = md5_encrypt(str4)[24:32]
    str6 = '%s%s%s' % (str(password), str5, str(salt))

    return md5_encrypt(str6)
