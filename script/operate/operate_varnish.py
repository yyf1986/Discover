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

def start_stop_varnish(action,ip,configfile):
    cmd = """ less %s |grep 'varnish:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ cd /root;ls -l |grep -E 'Varnishd.sh|varnishd.sh|startVarnishMonitorLog.sh|startVarnishncsaLog.sh'|wc -l """
        sh_num = run(ip,'root',cmd)[0].strip('\r\n')
        if int(sh_num) == 3:
            cmd = "cd /root;ls -l |grep -w Varnishd.sh|grep -v grep |wc -l"
            a = run(ip,'root',cmd)[0].strip('\r\n')
            cmd = "cd /root;ls -l |grep -w varnishd.sh|grep -v grep |wc -l"
            b = run(ip,'root',cmd)[0].strip('\r\n')
            if int(a) == 1 and int(b) == 0:
                start_bin = "Varnishd.sh"
            elif int(a) == 0 and int(b) == 1:
                start_bin = "varnishd.sh"
            if action == "stop":
                cmd = """ cd /root;./%s stop """ % start_bin
                run(ip,'root',cmd)
                cmd = """ ps -ef | grep varnish |grep -E 'varnish_monitor|varnishncsa|/usr/sbin/rotatelogs'|awk '{print \$2}'|xargs -I {} kill -9 {} """
                run(ip,'root',cmd)
                time.sleep(5)
                cmd = """ ps -ef | grep varnish|grep -v grep|wc -l """
                out = run(ip,'root',cmd)[0].strip('\r\n')
                if int(out) == 0:
                    print "%s varnish stop sucess." % ip
                else:
                    print "%s varnish stop fail." % ip
            elif action == "start":
                cmd = """ cd /root;./%s start;./startVarnishMonitorLog.sh;./startVarnishncsaLog.sh """ % start_bin
                run(ip,'root',cmd)
                time.sleep(5)
                cmd = """ ps -ef | grep varnish|grep -v grep|wc -l """
                out = run(ip,'root',cmd)[0].strip('\r\n')
                if int(out) >= 5:
                    print "%s varnish start sucess." % ip
                else:
                    print "%s varnish start fail." % ip
        else:
            print "%s varnish 没有启动脚本或者启动脚本不规范.请手动启动或者停止."
    else:
        pass
