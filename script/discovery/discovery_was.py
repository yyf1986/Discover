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

def get_was(ip):
    ret = ""
    #判断是否为was
    cmd = """ ps -ef | grep java |grep IBM/WebSphere/AppServer |grep -v grep |wc -l """
    was_pidnum = run(ip,'root',cmd)[0].strip('\r\n')
    ret +="was:1\r\n"
    if int(was_pidnum) >= 1:
        #获取用户
        cmd = """ ps -ef | grep java | grep 'IBM/WebSphere/AppServer'|grep -v grep|awk '{print \$1}'|sort|uniq """
        was_user = run(ip,'root',cmd)[0].strip('\r\n')
        ret +="WAS_USER:%s\r\n" % was_user
        #判断是否是dmgr
        cmd = """ ps -ef|grep java|grep 'IBM/WebSphere/AppServer'|grep dmgr|grep -v grep|awk '{if(\$NF == \\"dmgr\\") print \$0}'|wc -l """
        dmgr_pid_num = run(ip,'root',cmd)[0].strip('\r\n')
        if int(dmgr_pid_num) == 1:
            cmd = """ ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -v grep|grep dmgr|awk '{if(\$NF == \\"dmgr\\") print \$0}'|awk '{for(i=1;i<=NF;i++){if(\$i~ \\"^-Dserver.root\\")print \$i}}'|awk -F '=' '{print \$2}' """
            dmgr_path = run(ip,'root',cmd)[0].strip('\r\n')
            ret +="Dmgr_path:%s\r\n" % dmgr_path
        #判断是否有profile
        cmd = """ ps -ef | grep java|grep 'IBM/WebSphere/AppServer'|grep -Ev 'grep|dmgr|nodeagent'|awk '{for(i=1;i<=NF;i++){if(\$i ~ \\"^-Dserver.root\\")print \$i}}'|awk -F '=' '{print \$2}'|uniq|wc -l """
        profile_num = run(ip,'root',cmd)[0].strip('\r\n')
        if int(profile_num) >= 1:
            li = []
            cmd = """ ps -ef | grep java|grep -Ev 'grep|dmgr|nodeagent'|awk '{for(i=1;i<=NF;i++){if(\$i ~ \\"^-Dserver.root\\")print \$i}}'|awk -F '=' '{print \$2}'|uniq """
            profile_paths = run(ip,'root',cmd)
            for profile_path in profile_paths:
                profile_info = profile_path.strip('\r\n')+'--'
                logpath = profile_path.strip('\r\n')+"/logs"
                cmd = """ cd %s;find . -type d """ % logpath
                files = run(ip,'root',cmd)
                for file in files:
                    if file.strip('\r\n') not in ['./ffdc','./nodeagent','.']:
                        server_name = re.sub('./','',file.strip('\r\n'))
                        cmd = """ cd %s/%s;ls -l |grep SystemOut|wc -l """ % (logpath,server_name)
                        system_out = run(ip,'root',cmd)[0]
                        if int(system_out) >= 2:
                            cmd = """ ps -ef | grep %s |grep -v grep |wc -l """ % server_name
                            pid_num = run(ip,'root',cmd)[0]
                            if int(pid_num) == 1:
                                profile_info+=server_name+","
                        else:
                            pass
                    else:
                        pass
                profile_info = re.sub(',$','',profile_info)
                li.append(profile_info)
            profile_info = ""
            for i in range(0,len(li)):
                profile_info+=li[i]+';'
            #多个profile以分号分隔
            #profile_info = re.sub(';$','',profile_info)
            ret +="profile_info:%s\r\n" % profile_info
        return ret
    else:
        return ""
