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

def get_nginx(ip):
    ret = ""
    #判断是否为nginx
    cmd = """ ps -ef | grep nginx|grep -E 'master process|worker process'|grep -v 'bash -c'|wc -l """
    nginx_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(nginx_pidnum) >= 1:
        ret +="nginx:1\r\n"
        cmd = """ ps -ef | grep nginx|grep 'master process'|grep -v 'bash -c'|awk '{if(\$3 == \\"1\\")print \$2}' """
        nginx_pid = run(ip,'root',cmd)[0].strip('\r\n')
        cmd = """ cd /proc/%s;ls -l |grep exe |awk '{print \$NF}' """ % nginx_pid 
        nginx_bin = run(ip,'root',cmd)[0].strip('\r\n')
        ret +="nginx_bin:%s\r\n" % nginx_bin
        return ret
    else:
        return ""

#ip = "192.168.119.104"
#print get_nginx(ip)
