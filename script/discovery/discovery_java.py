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

def get_java(ip):
    ret = ""
    #判断是否为java
    cmd = """ ps -ef |grep java|grep -Ev 'IBM/WebSphere/AppServer|tomcat|jboss|/opt/logstash-1.4.1|/opt/flume'|grep -v grep|wc -l """
    java_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    if int(java_pidnum) >= 1:
        ret +="java:1\r\n"
        return ret
    else:
        return ""
