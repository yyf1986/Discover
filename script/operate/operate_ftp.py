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

def start_stop_ftp(action,ip,configfile):
    cmd = """ less %s |grep 'ftp:1'|wc -l """ % configfile
    out = commands.getoutput(cmd)
    if int(out) == 1:
        if action == "stop":
            cmd = """ service vsftpd stop """
            run(ip,'root',cmd)
            cmd = """ service vsftpd status """
            out = run(ip,'root',cmd)
            if re.search('is stopped',out):
                return "%s ftp stop sucess." % ip
            else:
                return "%s ftp stop fail." % ip
        elif action == "start":
            cmd = """ service vsftpd start """
            run(ip,'root',cmd)
            cmd = """ service vsftpd status """
            out = run(ip,'root',cmd)
            if re.search('is running',out):
                return "%s ftp start sucess." % ip
            else:
                return "%s ftp start fail." % ip
    else:
        return ""

#print start_stop_ftp("start","192.168.171.1","/home/13110508/yao/conf/192.168.171.1.txt")
