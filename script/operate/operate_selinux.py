#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import commands
import time

def run(ip,user,cmd):
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = commands.getoutput(cmds)
    except Exception,e:
        out = "error"
    return out

def start_stop_selinux(action,ip,configfile):
    cmd = """ less %s |grep 'selinux:1'|wc -l """ % configfile
    out = commands.getoutput(cmd)
    if int(out) == 1:
        return "%s selinux 配置有问题请检查." % ip
    else:
        return ""

#print start_stop_selinux("start","192.168.171.1","/home/13110508/yao/conf/192.168.171.1.txt")
