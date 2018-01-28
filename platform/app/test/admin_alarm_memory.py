# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/17 上午10:07


import os
def getAllitems(host, oid):
        sn1 = os.popen('snmpwalk -v 2c -c public ' + host + ' ' + oid).read().split('\n')[:-1]
        return sn1

def getSwapTotal(host):
        swap_total = getAllitems(host, 'UCD-SNMP-MIB::memTotalSwap.0')[0].split(' ')[3]
        return swap_total

def getSwapUsed(host):
        swap_avail = getAllitems(host, 'UCD-SNMP-MIB::memAvailSwap.0')[0].split(' ')[3]
        swap_total = getSwapTotal(host)
        swap_used = str(round(((float(swap_total)-float(swap_avail))/float(swap_total))*100 ,2)) + '%'
        return swap_used

def getMemTotal(host):
        mem_total = getAllitems(host, 'UCD-SNMP-MIB::memTotalReal.0')[0].split(' ')[3]
        return mem_total

def getMemUsed(host):
        mem_total = getMemTotal(host)
        mem_avail = getAllitems(host, 'UCD-SNMP-MIB::memAvailReal.0')[0].split(' ')[3]
        mem_used = str(round(((float(mem_total)-float(mem_avail))/float(mem_total))*100 ,2)) + '%'
        return mem_used

if __name__ == '__main__':
        hosts = ['127.0.0.1']
        print "Monitoring Memory Usage"
        for host in hosts:
                mem_used = getMemUsed(host)
                swap_used = getSwapUsed(host)
                print '==========' + host + '=========='
                print 'Mem_Used = %-15s   Swap_Used = %-15s' % (mem_used, swap_used)
                print
