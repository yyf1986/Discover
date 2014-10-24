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

def start_stop_ihs(action,ip,configfile):
    cmd = """ less %s |grep 'ihs:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ less %s |grep ihs_bin|awk -F ':' '{print $2}' """ % configfile
        ihs_bin = os.popen(cmd).readlines()[0].strip('\r\n')
        cmd = """ less %s |grep ihs_conf|awk -F ':' '{print $2}' """ % configfile
        ihs_conf = os.popen(cmd).readlines()[0].strip('\r\n')
        if action == "stop":
            if ihs_conf != "":
                cmd = """ %s/apachectl -k stop -f %s """ % (ihs_bin,ihs_conf)
                #run(ip,'root',cmd)
            else:
                cmd = """ %s/apachectl -k stop """ % ihs_bin
                #run(ip,'root',cmd)
            time.sleep(10)
            cmd = """ ps -ef | grep httpd|grep IBM|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                return "%s ihs stop sucess." % ip
            else:
                return "%s ihs stop fail." % ip
        elif action == "start":
            if ihs_conf != "":
                cmd = """ %s/apachectl -k start -f %s """ % (ihs_bin,ihs_conf)
                #run(ip,'root',cmd)
            else:
                cmd = """ %s/apachectl -k start """ % ihs_bin
                #run(ip,'root',cmd)
            cmd = """ ps -ef | grep httpd|grep IBM|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) >= 2:
                return "%s ihs start sucess." % ip
            else:
                return "%s ihs start fail." % ip
    else:
        return ""
