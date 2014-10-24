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

def start_stop_nginx(action,ip,configfile):
    cmd = """ less %s |grep 'nginx:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ less %s |grep nginx_bin|awk -F ':' '{print $2}' """ % configfile
        nginx_bin = os.popen(cmd).readlines()[0].strip('\r\n')
        if action == "stop":
            cmd = """ %s -s stop """ % nginx_bin
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep nginx|grep -E 'master process|worker process'|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                return "%s nginx stop sucess." % ip
            else:
                return "%s nginx stop fail." % ip
        elif action == "start":
            cmd = """ %s """ % nginx_bin
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep nginx|grep -E 'master process|worker process'|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) >= 2:
                return "%s nginx start sucess." % ip
            else:
                return "%s nginx start fail." % ip
    else:
        return ""
