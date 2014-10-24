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

def get_db2(ip):
    ret = ""
    #判断是否为db2
    cmd = """ ps -ef |grep -E 'db2sysc|/opt/ibm/db2'|grep -v grep|wc -l """
    db2_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(db2_pidnum) >= 1:
        ret +="db2:1\r\n"
        return ret
    else:
        return ""

#ip = "192.168.87.229"
#print get_db2(ip)
