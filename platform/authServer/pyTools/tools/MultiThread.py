#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/10 下午1:22
"""


import os
import subprocess
import Queue
import threading
import time
import random
import sys


#QUEUE = Queue.Queue(40)  # 队列

QUEUE = []  # 队列数组
THREADS = []
EVENT = [] # 通用的条件变量 数组
MUREX = threading.Lock()   # 互斥锁,保护文件


MANGERQUEUEVALUENUM = 10

def valueToQueueList(queue, queuelen, index, value):
    """
    :param queue:  队列数组
    :param queuelen: 队列的长度
    :param index:    当前需要放进的队列序列
    :param value:
    :return:
    """
    doing = True

    while doing:

        if index >= queuelen:
            index = 0
        try:
            queue[index].put(item=value, block=False)
            doing = False
        except Exception as msg:
            doing = True
            index += 1


def valuehandle(value):
    '''
    测试用的数据处理函数,方法调用
    :param value:
    :return:
    '''
    print 'valuehandle' + str(value)
    return True

VALUEHANDLE = None   # 使用不同的处理方法替换即可

def getValueToNmap(queue, mutex, fp):
    try:
        val = queue.get(block=False, timeout=3)  # 没有数据立即退出,否则会造成死锁
    except Exception as msg:
        return False

    # val 处理逻辑
    if VALUEHANDLE(val):
        return True
    # val 处理逻辑

    if mutex.acquire():  # 锁定
        fp.writelines(val + '\n')
        fp.flush()
        mutex.release()  # 释放锁
    return False

def managerQueueValue(queue, event, mutex, fp, debug=1):
    """
    :param queue:  队列
    :param event:  通用的条件变量
    :param fp:  未成功的ip写入文件
    :param debug: 如果是0, 就把该进程模拟成处理速度比较慢的进程，模拟阻塞进程
    :return:
    """
    while event.is_set() or (False == queue.empty()):  # 只有两个条件同时成立时才标志数据已经处理完成
        # if queue.empty():
        #     print "队列空"
        # if event.is_set():
        #     print "event.is_set()"
        # if debug == 0:
        #     print "debug == 0"
        #     time.sleep(1)
        #
        # time.sleep(0.001)
        getValueToNmap(queue, mutex, fp)




def readFileToQueue(queue, event):

    index = 0
    i = 0
    with open(CONF.IP_FILE, 'r') as fp:
        for line in fp:
            if index >= MANGERQUEUEVALUENUM:
                index = 0
            valueToQueueList(queue, queuelen=MANGERQUEUEVALUENUM, index=index, value=line.strip())
            index += 1

    for index in range(0, MANGERQUEUEVALUENUM):
        event[index].clear()


    print "readFileToQueue exit"

def run(valhandle=valuehandle):
    '''
    多线程处理逻辑
    :param valhandle: 处理每一个数据源的函数句柄
    :return:
    '''
    global VALUEHANDLE

    VALUEHANDLE = valhandle  # 使用不同的处理方法替换即可

    fp = open('error.log', 'a+')

    for i in range(0, MANGERQUEUEVALUENUM):
        q = Queue.Queue(10)
        e = threading.Event()   # 通用的条件变量
        e.set()

        t = threading.Thread(target=managerQueueValue, args=(q, e, MUREX, fp, i))
        THREADS.append(t)
        QUEUE.append(q)
        EVENT.append(e)

    t = threading.Thread(target=readFileToQueue, args=(QUEUE, EVENT))
    #THREADS.append(t)
    t.start()


    for i in range(0, MANGERQUEUEVALUENUM):
        # THREADS[i].setDaemon(True)
        THREADS[i].start()

    # for i in range(0, CONF.MANGERQUEUEVALUENUM + 1):
    #     THREADS[i].join()





if __name__ == '__main__':

    #do()
    run()