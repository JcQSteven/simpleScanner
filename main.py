#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/1 9:51 PM
# @Author  : 573v3n
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import mulPing
import datetime
import time
from multiprocessing import freeze_support,Pool

class Scanner:
    def __init__(self):
        self.data=[]
        self.logName="log-{0}.txt".format((datetime.datetime.now()).strftime('%Y-%m-%d-%H.%M.%S'))
        self.result={}
        pass

    def readFile(self,path):
        data = open(path).read().splitlines()
        for i in range(len(data)):
            data[i] = data[i].replace('\r', '')
            data[i] = data[i].replace('\n', '')
            data[i] = data[i].rstrip()
            data[i] = data[i].lstrip()
        self.data=data

    def pingResultHandler(self):
        pingMap={}
        start = time.time()
        for var1 in self.data:

            mp=mulPing.Ping()
            # 这里的利用multi progress线程导致结果没有返回值，仍需修正
            # p=Pool(processes=4)
            #
            # freeze_support() #windows must add this
            # p.apply_async(mp.mysslping, args=(var1,))
            # p.apply_async(mp.ip138ping,args=(var1,))
            #
            # p.close()
            # p.join()
            # pingMap[var1] = list(set(mp.getping()))

            mp.mysslping(var1)    #如果速度想要快一点就注释这个接口，20s
            mp.ip138ping(var1)
            mp.chinaping(var1)
            pingMap[var1] = list(set(mp.getping()))


        end=time.time()
        print(u"耗时：")
        print(round(end - start, 3))

        return pingMap

    def start(self):
        t=self.pingResultHandler()
        print(t)


    def resultOutput(self,var1):
        f=open(self.logName,"a+")
        f.write(var1)
        f.close()



if __name__ == '__main__':
    s=Scanner()
    s.readFile('source.txt')
    s.start()


