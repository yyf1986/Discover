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

def get_varnish(ip):
    ret = ""
    #判断是否为varnish
    cmd = """ ps -ef | grep varnish|grep /usr/sbin/rotatelogs|grep -E 'varnish_log|varnishstat_log'|grep -v '/opt/flume'|wc -l """
    varnish_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(varnish_pidnum) >= 1:
        ret +="varnish:1\r\n"
        return ret
    else:
        return ""

#ip = "192.168.119.145"
#print get_varnish(ip)
