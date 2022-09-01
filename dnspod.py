#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
#官方Github：https://github.com/codeif/dnspod-sdk
#官方pypi：https://pypi.org/project/dnspod-sdk/
from dnspod_sdk import DnspodClient
import collections
import json
import sys
import re

#获取用户信息
def getAccountInfo():
    return dc.post("/User.Detail").json()    

#格式化json数据
def formatJSON(jsonstr):
    return json.dumps(jsonstr,indent=4,ensure_ascii=False)

#获取域名ID
def getDomainID(jsonstr):
    return ["domains"][0]["id"]
    
#获取域名列表
def getDomainList(keyword=None,type="all"):
    r = dc.post("/Domain.List", data={"keyword":keyword, "type":type})
    return r.json()

#根据关键字搜索域名
def searchDomain(domain):
    r = dc.post("/Domain.List", data={"type": "all", "keyword":domain})
    return r.json()  

#添加单个域名到DNSPod；eg：example.com
#See:https://www.dnspod.cn/docs/domains.html#domain-create
def addDomain(domain,group_id=None,is_mark="no"):
    r = dc.post("/Domain.Create", data={"domain":domain, "group_id":group_id, "is_mark":is_mark})
    return r.json()  

#获取域名解析记录列表
def getRecordList(domain,keyword=None,length=3000):
    r = dc.post("/Record.List", data={"domain":domain,"keyword":keyword, "length":length})
    return r.json()

#获取单条域名解析记录
#See:https://www.dnspod.cn/docs/records.html#record-list
def getRecordOne(domain,subdomain):
    r = dc.post("/Record.List", data={"domain":domain,"sub_domain":subdomain})
    return r.json()

#获取域名下某条记录的ID，如果记录不存在，返回0
def getRecordID(domain,subdomain):
    r = dc.post("/Record.List", data={"domain":domain,"sub_domain":subdomain})
    try:
        return r.json()["records"][0]["id"]
    except KeyError:
        return 0
    
#修改单条域名解析记录
def modifyRecord(domain,record_id,sub_domain,value,record_type="A",record_line="默认"):
    r = dc.post("/Record.Modify", data={"domain":domain,"record_id":record_id,"sub_domain":sub_domain,"value":\
    value,"record_type":record_type, "record_line":record_line})
    return r.json()
    
#增加单条域名解析记录
def addRecord(domain,sub_domain,value,record_type="A",record_line="默认"):
    r = dc.post("/Record.Create", data={"domain":domain,"sub_domain":sub_domain,"value":\
    value,"record_type":record_type, "record_line":record_line})
    return r.json()

#删除域名记录：
#See：https://www.dnspod.cn/docs/records.html#record-remove
def removeRecord(domain,record_id):
    r = dc.post("/Record.Remove", data={"domain":domain,"record_id":record_id})
    return r.json()

#获取帮助信息：
def printHelp():
    return """
$1 domain [必选，根域名]
$2 sub_domain [必选，子域名]
$3 value    [可选，记录值]
$4 record_type [可选，记录类型，传值为英文字母大写(A,CNAME,AAAA,TXT,URL)，默认为 A]
$5 is_delete  [可选，是否是删除指令，固定为--del,当指定删除动作时，$3和$4可以省略]

eg:
dnspod example.com bbs 11.11.11.11 A\t#添加或修改一条A记录（记录存在则修改，不存在则添加）
dnspod example.com blog cdn.a.aliyun.com CNAME\t#同上，添加/修改CNAME记录
dnspod example.com blog --del\t#删除 blog.example.com 解析
dnspod example.com . --list\t#获取域名下所有解析记录列表
dnspod example.com abc --list\t#获取域名下包含abc的解析记录

dnspod . . --domainlist\t#获取账户下所有域名
dnspod . hjk --domainlist\t#获取账户下包含hjk的所有域名

dnspod example.com . --adddomain\t#添加某个新域名到DNSPod
    """
    
# ------------------------------------ #
#此处敏感信息已脱敏，请替换为自己的token
token_id = 10010
token = "xxxxxxxxxxxxxxx"
user_agent = "xxxxxxxxxxxxx@qq.com"

dc = DnspodClient(token_id, token, user_agent)

#r = dc.post("/Info.Version")
#print(r.json())

# r = dc.post("/Domain.List", data={"type": "all", "length": 1})
# print(r.json())
# print(formatJSON(r.json()))

if len(sys.argv)==2 and (sys.argv[1].lower()=="-h" or sys.argv[1].lower()=="--help"):
    print("DNSPod SDK命令行工具【增加/修改/删除域名记录】：\n%s"%printHelp(),end="")
    sys.exit()

if len(sys.argv)<4:
    print("缺少参数！\n%s"%printHelp(),end="")
    sys.exit(1)

#See:https://stackoverflow.com/questions/5423381/checking-if-sys-argvx-is-defined
arg_names = ['domain', 'sub_domain', 'value', 'record_type', 'delete']
args = dict(zip(arg_names, sys.argv[1:]))
Arg_list = collections.namedtuple('Arg_list', arg_names)
args = Arg_list(*(args.get(arg, None) for arg in arg_names))

domain=args.domain
sub_domain=args.sub_domain
value=args.value
record_type=args.record_type

is_delete=True if sys.argv[-1].lower()=="--del" else False
is_list=True if sys.argv[-1].lower()=="--list" else False
is_domainlist=True if sys.argv[-1].lower()=="--domainlist" else False
is_adddomain=True if sys.argv[-1].lower()=="--adddomain" else False

#是否是添加新域名动作：
if is_adddomain == True:
    keyword=sub_domain if not sub_domain=="." else None
    ret=addDomain(domain)
    if int(ret["status"]["code"]) == 1:
        print(formatJSON(ret))
    else:
        print("添加域名失败：")
        print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
    sys.exit()

#是否是获取域名列表动作：
if is_domainlist == True:
    keyword=sub_domain if not sub_domain=="." else None
    ret=getDomainList(keyword, "all")
    if int(ret["status"]["code"]) == 1:
        print(formatJSON(ret))
    else:
        print("获取域名列表失败：")
        print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
    sys.exit()

#是否是获取解析记录列表动作：
if is_list == True:
    #print("获取域名解析记录：")
    ret=getRecordList(domain,sub_domain)
    if int(ret["status"]["code"]) == 1:
        print(formatJSON(ret))
    else:
        print("获取域名解析记录失败：")
        print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
    sys.exit()

recordID=getRecordID(domain,sub_domain)

#是否是删除动作：
if is_delete == True:
    print("删除域名记录：")
    if recordID == 0:
        print("要删除的记录不存在！")
    else:
        ret=removeRecord(domain,recordID)
        print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
    sys.exit()

if not record_type and value:
    record_type="A" if re.match("^[0-9\.]+$",value) else "CNAME"

if recordID == 0:
    print("增加域名记录：")
    ret=addRecord(domain,sub_domain,value,record_type)
    print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
else:
    print("修改域名记录：")
    ret=modifyRecord(domain,recordID,sub_domain,value,record_type)
    print("{}：{}".format(ret["status"]["code"],ret["status"]["message"]))
    
if int(ret["status"]["code"]) == 1:
    print("成功处理的域名：\n%s.%s"%(sub_domain,domain))