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

def start_stop_jboss(action,ip,configfile):
    cmd = """ less %s |grep 'jboss:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        if action == "stop":
            cmd = """ ps -ef | grep '/opt/jboss'|grep -v grep|awk '{print \$2}' """
            run(ip,'root',cmd)
            time.sleep(2)
            cmd = """ ps -ef | grep jboss|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                return "%s jboss stop sucess." % ip
            else:
                return "%s jboss stop fail." % ip
        elif action == "start":
            cmd = """ cd /opt/jboss-1.4.1/bin;nohup ./app.sh start > /dev/null & """
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep jboss|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) >= 2:
                return "%s jboss start sucess." % ip
            else:
                return "%s jboss start fail." % ip
    else:
        return ""
