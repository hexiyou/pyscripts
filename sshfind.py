#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#根据主机别名查找openSSH配置文件~/.ssh/config对应主机配置项
#自用sshfind命令python实现版本
#原始sshfind为shell脚本实现，参看：/v/bin/sshfind
import sys
import os
import re

sshConfigFile="~/.ssh/config"
sshConfigFile=os.path.expanduser(sshConfigFile)

if len(sys.argv)<2 or (len(sys.argv)==2 and (str(sys.argv[1]).lower()=="--help" or str(sys.argv[1]).lower()=="-h")):
	print("""
	/v/bin/sshfind.py
	使用主机别名或别名部分关键字查找主机配置项信息，查找 ~/.ssh/config 文件内容.
	注：脚本优先做主机别名全字匹配，没有结果再尝试模糊匹配.
	$2为查询到多个主机时，至多返回的主机个数，可省略。默认返回全部匹配到的主机。

Usage:
        sshfind.py [keyword] [max hosts]
Example:
        sshfind.py racknerd 1
	
	""")
	sys.exit(0)
else:
	hoststr=str(sys.argv[1]).strip()

foundCount=0
limitCount=-1
wrapMatch=False #全字匹配标志符

# $2参数传入时，查询至多返回$2个结果
if len(sys.argv)==3 and sys.argv[2]:
	limitCount=int(sys.argv[2])

with open(sshConfigFile,"r") as read_f:
	Tag=False
	for num,line in enumerate(read_f.readlines(),1):
		#if re.match(r'Host .*[ ]?'+hoststr+'[ $]?',line,re.I):
		if re.match(r'Host .*[^-\.]?'+hoststr+'[ $]?',line,re.I):
			Tag=True
			foundCount+=1
			if re.match(r'.* '+hoststr+'( |$)',line,re.I):
				#标识全字匹配
				wrapMatch=True
			if limitCount!=-1 and foundCount>limitCount:
				break
			#找到两个及以上主机时，打印空行隔开
			if foundCount>=2:
				print("\n")
			#找到主机匹配则先打印开始行的行号，以供sshedit命令使用
			print(num)
			print(line,end='')
			continue
		if Tag==True and re.match(r'[ ]*Host ',line,re.I):
			Tag=False
		if Tag==True:
			print(line,end='')

if wrapMatch==True and foundCount==1:
	print("\n\t以上为全字匹配结果")
	
print("\nsshfind执行完毕；Python版本:%s"%sys.version)