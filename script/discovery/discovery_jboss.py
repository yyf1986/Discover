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

def get_jboss(ip):
    ret = ""
    #判断是否为jboss
    cmd = """ ps -ef |grep /opt/jboss|grep -v grep|wc -l """
    jboss_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(jboss_pidnum) >= 1:
        ret +="jboss:1\r\n"
        return ret
    else:
        return ""

#ip = "192.168.87.229"
#print get_db2(ip)
