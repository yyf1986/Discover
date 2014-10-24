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

def get_logstash(ip):
    ret = ""
    #判断是否为logstash
    cmd = """ ps -ef |grep '/opt/logstash-1.4.1'|grep -v grep|wc -l """
    logstash_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(logstash_pidnum) >= 1:
        ret +="logstash:1\r\n"
        return ret
    else:
        return ""
