#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import os
import time

def run(ip,user,cmd):
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = os.popen(cmds).readlines()
    except Exception,e:
        out = "error"
    return out

def start_stop_tomcat(action,ip,configfile):
    cmd = """ less %s |grep 'tomcat:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        if action == "stop":
            print "%s tomcat需要手动停止." % ip
        elif action == "start":
            print "%s tomcat需要手动启动." % ip
    else:
        pass
