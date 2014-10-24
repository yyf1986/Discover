#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
def run(ip,user,cmd):
    import commands
    cmds = """ sudo ssh -oConnectTimeout=10 %s@%s "%s" """ % (user,ip,cmd)
    try:
        out = commands.getoutput(cmds)
    except:
        out = "error"
    return out

def get_fsinfo(ip):
    cmd = "df -lh"
    out = run(ip,'root',cmd)
    return out

def get_ftpstatus(ip):
    cmd = "service vsftpd status"
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('is running',out):
            return "1"
        else:
            return "0"
    else:
        return "e"

def get_ntpd(ip):
    cmd = "service ntpd status"
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('is running',out):
            return "1"
        else:
            cmd = "chkconfig ntpd off"
            run(ip,'root',cmd)
            return "0"
    else:
        return "e"

def get_sendmail(ip):
    cmd = "service sendmail status"
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('is running',out):
            return "1"
        else:
            cmd = "chkconfig sendmail off"
            run(ip,'root',cmd)
            return "0"
    else:
        return "e"

def get_postfix(ip):
    cmd = "service postfix status"
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('is running',out):
            return "1"
        else:
            cmd = "chkconfig postfix off"
            run(ip,'root',cmd)
            return "0"
    else:
        return "e"

def get_iptables(ip):
    cmd = "service iptables status"
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('policy ACCEPT',out):
            return "1"
        else:
            cmd = "chkconfig iptables off"
            run(ip,'root',cmd)
            return "0"
    else:
        return "e"

def get_selinux(ip):
    cmd = """ cat /etc/selinux/config |grep -v ^#|grep SELINUX=|awk -F '=' '{print \$2}' """
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if out == "disabled":
            return "0"
        else:
            return "1"
    else:
        return "e"

def get_nfs(ip):
    cmd = """ service nfs status """
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if re.search('nfsd is running',out):
            return "1"
        elif re.search('nfsd is stopped',out):
            return "0"
        else:
            return "0"
    else:
        return "e"

def get_tivoli(ip):
    cmd = """ netstat -nupt|grep 1918|grep EST|wc -l """
    out = run(ip,'root',cmd)
    if str(out) != "error":
        if out == "1":
            return "1"
        else:
            return "0"
    else:
        return "e"

#print get_nfs("192.168.171.1")
