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

def start_stop_ntpd(action,ip,configfile):
    cmd = """ less %s |grep 'ntpd:1'|wc -l """ % configfile
    out = commands.getoutput(cmd)
    if int(out) == 1:
        if action == "stop":
            cmd = """ service ntpd stop """
            run(ip,'root',cmd)
            cmd = """ service ntpd status """
            out = run(ip,'root',cmd)
            if re.search('is stopped',out):
                return "%s ntpd stop sucess." % ip
            else:
                return "%s ntpd stop fail." % ip
        elif action == "start":
            cmd = """ service ntpd start """
            run(ip,'root',cmd)
            cmd = """ service ntpd status """
            out = run(ip,'root',cmd)
            if re.search('is running',out):
                return "%s ntpd start sucess." % ip
            else:
                return "%s ntpd stop fail." % ip
    else:
        return ""

#print start_stop_ntpd("start","192.168.171.1","/home/13110508/yao/conf/192.168.171.1.txt")
