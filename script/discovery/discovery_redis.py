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

def get_redis(ip):
    ret = ""
    #判断是否为redis
    cmd = """ ps -ef |grep redis|grep -v grep|wc -l """
    redis_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(redis_pidnum) >= 1:
        ret +="redis:1\r\n"
        return ret
    else:
        return ""
