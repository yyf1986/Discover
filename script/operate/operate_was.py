#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import os
import commands
import time

def run(ip,user,cmd):
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = commands.getoutput(cmds)
    except Exception,e:
        out = "error"
    return out

def start_stop_was(action,ip,configfile):
    cmd = """ less %s |grep 'was:1'|wc -l """ % configfile
    out = os.popen(cmd).readlines()[0].strip('\r\n')
    if int(out) == 1:
        cmd = """ less %s |grep 'WAS_USER:'|awk -F ':' '{print $2}' """ % configfile
        wasuser = os.popen(cmd).readlines()[0].strip('\r\n')
        
        cmd = """ less %s |grep 'Dmgr_path:'|wc -l """ % configfile
        num = os.popen(cmd).readlines()[0].strip('\r\n')
        if int(num) == 1:
            cmd = """ less %s |grep 'Dmgr_path:'|awk -F ':' '{print $2}' """ % configfile
            dmgr_path = os.popen(cmd).readlines()[0].strip('\r\n')
            if action == "start":
                cmd = """ su - %s -c 'cd %s/bin;./startManager.sh' """ % (wasuser,dmgr_path)
                print "begin to start dmgr %s\r\n" % dmgr_path
                print run(ip,'root',cmd)
            cmd = """ less %s |grep 'profile_info:' | wc -l """ % configfile
            num = os.popen(cmd).readlines()[0].strip('\r\n')
            if int(num) == 1:
                cmd = """ less %s |grep 'profile_info:' | awk -F ':' '{print $2}' """ % configfile
                profile_infos = os.popen(cmd).readlines()[0].strip('\r\n')
                for profile_info in profile_infos.split(';'):
                    if profile_info != "":
                        profile = profile_info.split('--')[0]
                        servers = profile_info.split('--')[1]
                        if action == "start":
                            cmd = """ su - %s -c 'cd %s/bin/;./startNode.sh' """ % (wasuser,profile)
                            print "begin to start node %s\r\n" % profile
                            print run(ip,'root',cmd)
                        for server in servers.split(','):
                            if action == "start":
                                cmd = """ su - %s -c 'cd %s/bin/;./startServer.sh %s' """ % (wasuser,profile,server)
                                print "begin to start server %s %s\r\n" % (profile,server)
                                print run(ip,'root',cmd)
                            elif action == "stop":
                                cmd = """ su - %s -c 'cd %s/bin/;./stopServer.sh %s -username operator -password 111111' """ % (wasuser,profile,server)
                                print "begin to stop server %s %s\r\n" % (profile,server)
                                print run(ip,'root',cmd)
                        if action == "stop":
                            cmd = """ su - %s -c 'cd %s/bin/;./stopNode.sh -username operator -password 111111' """ % (wasuser,profile)
                            print "begin to stop node %s\r\n" % profile
                            print run(ip,'root',cmd)
            else:
                pass
            if action == "stop":
                cmd = """ su - %s -c 'cd %s/bin;./stopManager.sh -username operator -password 111111' """ % (wasuser,dmgr_path)
                print "begin to stop dmgr %s\r\n" % dmgr_path
                print run(ip,'root',cmd)
        else:
            cmd = """ less %s |grep 'profile_info:' | wc -l """ % configfile
            num = os.popen(cmd).readlines()[0].strip('\r\n')
            if int(num) == 1:
                cmd = """ less %s |grep 'profile_info:' | awk -F ':' '{print $2}' """ % configfile
                profile_infos = os.popen(cmd).readlines()[0].strip('\r\n')
                for profile_info in profile_infos.split(';'):
                    if profile_info != "":
                        profile = profile_info.split('--')[0]
                        servers = profile_info.split('--')[1]
                        if action == "start":
                            cmd = """ su - %s -c 'cd %s/bin/;./startNode.sh' """ % (wasuser,profile)
                            print "begin to start node %s\r\n" % profile
                            print run(ip,'root',cmd)
                        for server in servers.split(','):
                            if action == "start":
                                cmd = """ su - %s -c 'cd %s/bin/;./startServer.sh %s' """ % (wasuser,profile,server)
                                print "begin to start server %s %s\r\n" % (profile,server)
                                print run(ip,'root',cmd)
                            elif action == "stop":
                                cmd = """ su - %s -c 'cd %s/bin/;./stopServer.sh %s -username operator -password 111111' """ % (wasuser,profile,server)
                                print "begin to stop server %s %s\r\n" % (profile,server)
                                print run(ip,'root',cmd)
                        if action == "stop":
                            cmd = """ su - %s -c 'cd %s/bin/;./stopNode.sh -username operator -password 111111' """ % (wasuser,profile)  
                            print "begin to stop node %s\r\n" % profile
                            print run(ip,'root',cmd)
    else:
        pass
