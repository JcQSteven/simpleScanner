#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/2 8:18 PM
# @Author  : 573v3n
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : mulPort.py
# @Software: PyCharm
from gevent import monkey;monkey.patch_all()
import gevent
import gevent.pool
import socket
import requests
from lxml import etree
import time
class Port:
    def __init__(self,ip):
        self.ip=ip
        self.port=[27017]
        self.map=[]
    def TCP_connect(self,port):
        timeout = 0.5
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }

        TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_sock.settimeout(timeout)
        try:
            result = TCP_sock.connect_ex((self.ip, int(port)))  # 判断是否存在TCP端口
            if result == 0:  # 顺便判断下是不是web服务，来获取title
                url = "http://{0}:{1}".format(self.ip, port)
                r = requests.get(headers=headers, url=url)
                if r.status_code == 200:
                    root = etree.HTML(r.content)
                    title = root.xpath("//title//text()")
                    self.map.append({
                        "port":port,
                        "title":title[0]
                    })
                    print("[+]{0}:{1}   {2}".format(self.ip,port,title[0]))

                else:
                    self.map.append({
                        "port": port,
                        "title": None
                    })
                    print("[+]{0}:{1}".format(self.ip, port))
            else:
                pass

            TCP_sock.close()
        except socket.error as e:
            print("[!]socket错误:{0}".format(e))

    def startDetect(self):
        thread_num = 100

        for i in range(22, 10000):
            self.port.append(i)

        # start = time.time()

        g = gevent.pool.Pool(thread_num)  # 设置线程数

        run_list = []
        for var1 in self.port:
            run_list.append(g.spawn(self.TCP_connect,var1))
        gevent.joinall(run_list)
        # end = time.time()
        # pbar.finish()
        # print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
        # return map_dict

    def getPort(self):
        # print(self.map)
        return self.map