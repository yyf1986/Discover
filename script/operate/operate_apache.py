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

def start_stop_apache(action,ip,configfile):
    cmd = """ less %s |grep 'apache:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ less %s |grep apache_bin|awk -F ':' '{print $2}' """ % configfile
        apache_bin = os.popen(cmd).readlines()[0].strip('\r\n')
        cmd = """ less %s |grep apache_conf|awk -F ':' '{print $2}' """ % configfile
        apache_conf = os.popen(cmd).readlines()[0].strip('\r\n')
        if action == "stop":
            if apache_conf != "":
                cmd = """ %s/apachectl -k stop -f %s """ % (apache_bin,apache_conf)
                run(ip,'root',cmd)
            else:
                cmd = """ %s/apachectl -k stop """ % (apache_bin,apache_conf)
                run(ip,'root',cmd)
            time.sleep(10)
            cmd = """ ps -ef | grep httpd|grep apache|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) == 0:
                return "%s apache stop sucess." % ip
            else:
                return "%s apache stop fail." % ip
        elif action == "start":
            if apache_conf != "":
                cmd = """ %s/apachectl -k start -f %s """ % (apache_bin,apache_conf)
                run(ip,'root',cmd)
            else:
                cmd = """ %s/apachectl -k start """ % (apache_bin,apache_conf)
                run(ip,'root',cmd)
            cmd = """ ps -ef | grep httpd|grep apache|grep -v grep|wc -l """
            out = run(ip,'root',cmd)[0].strip('\r\n')
            if int(out) >= 2:
                return "%s apache start sucess." % ip
            else:
                return "%s apache start fail." % ip
    else:
        return ""
