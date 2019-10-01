#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/1 8:47 PM
# @Author  : 573v3n
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : mulPing.py
# @Software: PyCharm
import re
import requests
import time

class Ping:
    def __init__(self):
        self.map=[]

    def matchDomain(self,domain):
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                    domain):
            return False
        return True

    def ip138ping(self,domain):
        headers = {
            "Cookie": "pgv_pvi=1464631296; PHPSESSID=jl4tcbrcm2gac6gkutml8lkqs0; Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1569500204; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1569940840",
            "Host": "site.ip138.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        now = int(round(time.time() * 1000))
        url = "https://site.ip138.com/domain/read.do?domain={0}&time={1}".format(domain, now)
        r = requests.get(headers=headers, url=url)
        if r.status_code == 200:
            result = r.json()
            if "data" in result:
                for i in result["data"]:
                    self.map.append(i["ip"])
            else:
                pass


    def mysslping(self,domain):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        url = "https://myssl.com/api/v1/tools/cdn_check?domain={0}".format(domain)
        r = requests.get(headers=headers, url=url)
        if r.status_code == 200:
            result = r.json()
            if len(result["data"])>0:
                for var1 in result["data"]:
                    self.map.append(var1["ip"])
            else:
                pass

    def chinaping(self,domain):
        headers = {
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection":"keep-alive",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-Site":"none",
            "Sec-Fetch-User":"?1",
            "Upgrade-Insecure-Requests":"1",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Host":"cdn.chinaz.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        if len(domain.split('.'))<=2:
            domain="www."+domain
        url="https://cdn.chinaz.com/ajax/CDNHostIP?host={0}".format(domain)
        print(url)
        r = requests.get(headers=headers,url=url)
        if r.status_code == 200:
            # print(r.text)
            result = r.json()
            if "data" in result.keys():
                for var1 in result["data"]:
                    self.map.append(var1["IP"])
            else:
                pass
    def getping(self):
        return self.map