#!/usr/bin/env python

import time

datetime='2016-09-12 18:05:00'

print int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))
