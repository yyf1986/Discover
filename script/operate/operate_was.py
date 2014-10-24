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

def start_stop_was(action,ip,configfile):
    cmd = """ less %s |grep 'was:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ less %s |grep 'WAS_USER:'|awk -F ':' '{print $2}' """ % configfile
        wasuser = os.popen(cmd).readlines()[0].strip('\r\n')

        cmd = """ less %s |grep 'profile_info:' | wc -l """ % configfile
        num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(num) == 1:
            cmd = """ less %s |grep 'profile_info:' | awk -F ':' '{print $2}' """ % configfile
            profile_infos = os.popen(cmd).readlines()[0].strip('\r\n')
            for profile_info in profile_infos.split(';'):
                if profile_info != "":
                    profile = profile_info.split('--')[0]
                    servers = profile_info.split('--')[1]
                    for server in servers.split(','):
                        if action == "start":
                            cmd = """ su - %s -c "cd %s/bin/;./startServer.sh %s" """ % (wasuser,profile,server)
                            print cmd
                        elif action == "stop":
                            cmd = """ su - %s -c "cd %s/bin/;./stopServer.sh %s -username operator -password xtbspasswd" """ % (wasuser,profile,server)
                            print cmd
        else:
            pass

        cmd = """ less %s |grep 'Dmgr_path:'|wc -l """ % configfile
        num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(num) == 1:
            cmd = """ less %s |grep 'Dmgr_path:'|awk -F ':' '{print $2}' """ % configfile
            dmgr_path = os.popen(cmd).readlines()[0].strip('\r\n')
            if action == "start":
                cmd = """ su - %s -c "cd %s/bin;./startManager.sh" """ % (wasuser,dmgr_path)
                print cmd
            elif action == "stop":
                cmd = """ su - %s -c "cd %s/bin;./stopManager.sh -username operator -password xtbspasswd" """ % (wasuser,dmgr_path)
                print cmd
        else:
            pass
    else:
        return ""

start_stop_was("stop","192.168.161.1","/home/13110508/yao/conf/192.168.161.1.txt")
