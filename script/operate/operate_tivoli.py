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

def start_stop_tivoli(action,ip,configfile):
    cmd = """ less %s |grep 'tivoli:1'|wc -l """ % configfile
    out = commands.getoutput(cmd)
    if int(out) == 1:
        if action == "stop":
            cmd = """ cd /tivoli/for_os/bin/;./itmcmd agent stop lz """
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep tivoli|grep -v grep|wc -l """
            out = run(ip,'root',cmd)
            if int(out) == 0:
                return "%s tivoli stop sucess." % ip
            else:
                return "%s tivoli stop fail." % ip
        elif action == "start":
            cmd = """ cd /tivoli/for_os/bin/;./itmcmd agent start lz """
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep tivoli|grep -v grep|wc -l """
            out = run(ip,'root',cmd)
            if int(out) == 1:
                return "%s tivoli start sucess." % ip
            else:
                return "%s tivoli start fail." % ip
    else:
        return ""

#print start_stop_tivoli("start","192.168.171.1","/home/13110508/yao/conf/192.168.171.1.txt")
