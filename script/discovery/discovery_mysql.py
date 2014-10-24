#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import os

def run(ip,user,cmd):
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = os.popen(cmds).readlines()
    except Exception,e:
        out = "error"
    return out

def get_mysql(ip):
    ret = ""
    #判断是否为mysql
    cmd = """ ps -ef | grep mysqld|grep -v grep|wc -l """
    mysql_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(mysql_pidnum) >= 1:
        ret +="mysql:1\r\n"
        return ret
    else:
        return ""

#ip = "192.168.84.237"
#print get_mysql(ip)
