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
import mulPort
import json
from multiprocessing import freeze_support,Pool

class Scanner:
    def __init__(self):
        self.data=[]
        self.logName="log-{0}.txt".format((datetime.datetime.now()).strftime('%Y-%m-%d-%H.%M.%S'))
        self.result=[]
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

        start = time.time()
        for var1 in self.data:
            pingMap = {}
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
            pingMap["host"]=var1
            pingMap["ip"] = list(set(mp.getping()))
            if len(pingMap["ip"])>1:
                pingMap["cdn"]=True
            else:
                pingMap["cdn"]=False
            self.result.append(pingMap)

        end=time.time()
        print(u"ping检测耗时:{0}".format(round(end - start, 3)))
        self.printHanlder("ping")
        # self.resultHandler()

    def portResultHandler(self):
        start = time.time()
        for var1 in self.result:
            if not var1["cdn"]:
                mp=mulPort.Port(var1["ip"][0])
                mp.startDetect()
                var2=mp.getPort()
                var1["info"]=var2
        end = time.time()
        print(u"端口扫描耗时:{0}".format(round(end - start, 3)))
        self.printHanlder("port")


    def start(self):
        self.pingResultHandler()
        self.portResultHandler()
        self.resultHandler()


        # print(self.result)


    def resultHandler(self):
        f=open(self.logName,"w")
        jsObj=json.dumps(self.result)
        f.write(jsObj)
        f.close()

    def printHanlder(self,dtype):
        if dtype=="ping":
            print("[*]ping检测结果")
            for var1 in self.result:
                print("[*]{0} Ping检测结果：".format(var1["host"]))
                print("[+]{0}".format(",".join(var1["ip"])))
                print("[+]CDN:{0}".format(var1["cdn"]))
        elif dtype=="port":
            for var1 in self.result:
                if not var1["cdn"]:
                    var3=[]
                    print("[*]{0}[{1}]端口扫描结果:".format(var1["host"],var1["ip"][0]))
                    for var2 in var1["info"]:
                        var3.append(str(var2["port"]))

                    print("[+]{0}".format(",".join(var3)))
        pass


if __name__ == '__main__':
    s=Scanner()
    s.readFile('source.txt')
    s.start()


