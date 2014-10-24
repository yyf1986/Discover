#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import os

def run(ip,user,cmd):
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = os.popen(cmds).readlines()
    except Exception,e:
        out = "error"
    return out

def get_ihs(ip):
    ret = ""
    #判断是否为ihs
    cmd = """ ps -ef | grep httpd|grep IBM|grep -Ev 'grep|admin.conf'|grep -v '/opt/flume'|wc -l """
    ihs_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(ihs_pidnum) >= 1:
        ret +="ihs:1\r\n"
        cmd = """ ps -ef | grep httpd|grep IBM|grep -Ev 'grep|admin.conf'|grep -v '/opt/flume'|awk '{if(\$3 == \\"1\\")print \$2}' """
        ihs_pid = run(ip,'root',cmd)[0].strip('\r\n')
        cmd = """ cd /proc/%s;ls -l |grep exe |awk '{print \$NF}'|sed -e 's/\/httpd//' """ % ihs_pid 
        ihs_bin = run(ip,'root',cmd)[0].strip('\r\n')
        ret +="ihs_bin:%s\r\n" % ihs_bin
        cmd = """ ps -ef |grep httpd |grep IBM|grep -Ev 'grep|admin.conf'|grep -v '/opt/flume'|awk '{if(\$3 == \\"1\\")print \$0}'|awk '{for(i=1;i<=NF;i++){if (\$i ~ \\".conf\\")print \$i}}' """
        if len(run(ip,'root',cmd)) == 1:
            ihs_conf = run(ip,'root',cmd)[0].strip('\r\n')
        else:
            ihs_conf = ""
        ret +="ihs_conf:%s\r\n" % ihs_conf
        
        return ret
    else:
        return ""

#ip = "192.168.171.6"
#print get_ihs(ip)
