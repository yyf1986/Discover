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

def get_apache(ip):
    ret = ""
    #判断是否为apache
    cmd = """ ps -ef | grep httpd|grep apache|grep -Ev 'grep'|grep -v '/opt/flume'|wc -l """
    apache_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(apache_pidnum) >= 1:
        ret +="apache:1\r\n"
        cmd = """ ps -ef | grep httpd|grep apache|grep -Ev 'grep'|grep -v '/opt/flume'|awk '{if(\$3 == \\"1\\")print \$2}' """
        apache_pid = run(ip,'root',cmd)[0].strip('\r\n')
        cmd = """ cd /proc/%s;ls -l |grep exe |awk '{print \$NF}'|sed -e 's/\/httpd//' """ % apache_pid 
        apache_bin = run(ip,'root',cmd)[0].strip('\r\n')
        ret +="apache_bin:%s\r\n" % apache_bin
        cmd = """ ps -ef |grep httpd |grep apache|grep -Ev 'grep'|grep -v '/opt/flume'|awk '{if(\$3 == \\"1\\")print \$0}'|awk '{for(i=1;i<=NF;i++){if (\$i ~ \\".conf\\")print \$i}}' """
        if len(run(ip,'root',cmd)) == 1:
            apache_conf = run(ip,'root',cmd)[0].strip('\r\n')
        else:
            apache_conf = ""
        ret +="apache_conf:%s\r\n" % apache_conf
        
        return ret
    else:
        return ""

#ip = "192.168.52.38"
#print get_apache(ip)
