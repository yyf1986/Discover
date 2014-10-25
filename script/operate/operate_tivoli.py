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
                print "%s tivoli stop sucess." % ip
            else:
                print "%s tivoli stop fail." % ip
        elif action == "start":
            cmd = """ cd /tivoli/for_os/bin/;./itmcmd agent start lz """
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep tivoli|grep -v grep|wc -l """
            out = run(ip,'root',cmd)
            if int(out) == 1:
                print "%s tivoli start sucess." % ip
            else:
                print "%s tivoli start fail." % ip
    else:
        pass
