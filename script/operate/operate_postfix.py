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

def start_stop_postfix(action,ip,configfile):
    cmd = """ less %s |grep 'postfix:1'|wc -l """ % configfile
    out = commands.getoutput(cmd)
    if int(out) == 1:
        if action == "stop":
            cmd = """ service postfix stop """
            run(ip,'root',cmd)
            cmd = """ service postfix status """
            out = run(ip,'root',cmd)
            if re.search('is stopped',out):
                return "%s postfix stop sucess." % ip
            else:
                return "%s postfix stop fail." % ip
        elif action == "start":
            cmd = """ service postfix start """
            run(ip,'root',cmd)
            cmd = """ service postfix status """
            out = run(ip,'root',cmd)
            if re.search('is running',out):
                return "%s postfix start sucess." % ip
            else:
                return "%s postfix start fail." % ip
    else:
        return ""

#print start_stop_postfix("start","192.168.171.1","/home/13110508/yao/conf/192.168.171.1.txt")
