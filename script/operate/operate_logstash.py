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

def start_stop_logstash(action,ip,configfile):
    cmd = """ less %s |grep 'logstash:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        if action == "stop":
            cmd = """ cd /opt/logstash-1.4.1/bin;./app.sh stop """
            run(ip,'root',cmd)
            time.sleep(2)
            cmd = """ ps -ef | grep logstash|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                return "%s logstash stop sucess." % ip
            else:
                return "%s logstash stop fail." % ip
        elif action == "start":
            cmd = """ cd /opt/logstash-1.4.1/bin;nohup ./app.sh start > /dev/null & """
            run(ip,'root',cmd)
            time.sleep(5)
            cmd = """ ps -ef | grep logstash|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) >= 1:
                return "%s logstash start sucess." % ip
            else:
                return "%s logstash start fail." % ip
    else:
        return ""
