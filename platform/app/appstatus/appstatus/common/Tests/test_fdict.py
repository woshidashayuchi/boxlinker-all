#!/usr/bin/env python

class test(object):

    def a_01(self):
        print 'a_01'
        return(01)

    def a_02(self):
        print 'a_02'
        return(02)

#################################

p = test()

fun = {101: p.a_01, 102: p.a_02}

print fun[102]()

