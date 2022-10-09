#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 查询VPS主机已使用流量
#Please See：https://www.tmhhost.com/
from urllib import request as req
from lxml import etree
import json

r=req.Request('https://www.tmhhost.com/host/dedicatedserver?host_id=xxxxid') #主机ID
r.add_header('Cookie','PHPSESSID=xxxx')
r.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')

response=req.urlopen(r).read().decode('utf-8')

#print(response)
json_data = json.loads(response)
if json_data["status"] == 200:
    bwlimit=json_data["data"]["host_data"]["bwlimit"] #总流量
    bwusage=json_data["data"]["host_data"]["bwusage"] #已使用流量
    print("总流量：%s GB\n已使用流量：%s GB" %(bwlimit,bwusage))
else:
    print("登录会话已过期或服务器接口异常！")
    print("\n服务器返回如下信息：")
    print("status：%s，msg：%s" % (json_data["status"],json_data["msg"]))
    
    
    
    
#html=etree.HTML(response)
#
#data=html.xpath('/html/body/div[1]/div/section[2]/div[1]/div[2]/div[4]/div[2]/div/p/text()')[0]
#
#print(data.replace(" ",""))

