# Author: YanHua <it-yanh@all-reach.com>

import time
import weakref
import collections


class LocalCache(object):

    notFound = object()

    class Dict(dict):

        def __del__(self):
            pass

    def __init__(self, maxlen=100):

        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxlen)

    def get(self, key):

        value = self.weak.get(key, self.notFound)

        if (value is not self.notFound):

            expire = value['expire']

            if (int(time.time()) >= expire):

                return self.notFound

            else:

                return value

        else:

            return self.notFound

    def set(self, key, value):

        self.weak[key] = strongRef = LocalCache.Dict(value)
        self.strong.append(strongRef)
