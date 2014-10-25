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

def start_stop_flume(action,ip,configfile):
    cmd = """ less %s |grep 'flume:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        if action == "stop":
            cmd = """ ps -ef | grep '/opt/flume'|grep -v grep |awk '{print \$2}'|xargs -I {} kill {} """
            run(ip,'root',cmd)
            time.sleep(15)
            cmd = """ ps -ef | grep '/opt/flume'|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                print "%s flume stop sucess." % ip
            else:
                cmd = """ ps -ef | grep '/opt/flume'|grep -v grep |awk '{print \$2}'|xargs -I {} kill -9 {} """
                run(ip,'root',cmd)
                cmd = """ ps -ef | grep '/opt/flume'|grep -v grep|wc -l """
                out = run(ip,'root',cmd)[0].strip('\r\n')
                if int(out) == 0:
                    print "%s flume stop sucess." % ip
                else:
                    print "%s flume stop fail." % ip
        elif action == "start":
            print "%s flume 有定时任务会自动启动." % ip
    else:
        pass
