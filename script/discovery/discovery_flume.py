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

def get_flume(ip):
    ret = ""
    #判断是否为flume
    cmd = """ ps -ef |grep '/opt/flume'|grep -v grep|wc -l """
    flume_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(flume_pidnum) >= 1:
        ret +="flume:1\r\n"
        return ret
    else:
        return ""
