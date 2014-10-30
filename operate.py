#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket
import sys

from script.operate import operate_ftp
from script.operate import operate_ntpd
from script.operate import operate_sendmail
from script.operate import operate_postfix
from script.operate import operate_iptables
from script.operate import operate_selinux
from script.operate import operate_nfs
from script.operate import operate_tivoli
from script.operate import operate_was
from script.operate import operate_ihs
from script.operate import operate_varnish
from script.operate import operate_apache
from script.operate import operate_mysql
from script.operate import operate_db2
from script.operate import operate_nginx
from script.operate import operate_tomcat
from script.operate import operate_redis
#from script.operate import operate_jboss
from script.operate import operate_mongodb
from script.operate import operate_logstash
from script.operate import operate_flume
from script.operate import operate_mq
from script.operate import operate_java

if len(sys.argv) > 2:
    print "输入的参数不正确."
    sys.exit()
elif len(sys.argv) == 2:
    if sys.argv[1] == "start":
        action = "start"
    elif sys.argv[1] == "stop":
        action = "stop"
    else:
        print "请输入start/stop."
        sys.exit()
else:
    print "请输入start/stop."
    sys.exit()

if __name__ == '__main__':
    with open('ip.txt') as lines:
        for line in lines:
            ret = ""
            ip = line.strip('\r\n')
            configfile = "/home/13110508/yao/conf/%s.txt" % ip
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip,22))
                s.close()
                #ftp
                operate_ftp.start_stop_ftp(action,ip,configfile)
                #ntpd
                operate_ntpd.start_stop_ntpd(action,ip,configfile)
                #sendmail
                operate_sendmail.start_stop_sendmail(action,ip,configfile)
                #postfix
                operate_postfix.start_stop_postfix(action,ip,configfile)
                #iptables
                operate_iptables.start_stop_iptables(action,ip,configfile)
                #selinux
                operate_selinux.start_stop_selinux(action,ip,configfile)
                #nfs
                operate_nfs.start_stop_nfs(action,ip,configfile)
                #tivoli
                operate_tivoli.start_stop_tivoli(action,ip,configfile)
                #was
                #operate_was.start_stop_was(action,ip,configfile)
                #ihs
                operate_ihs.start_stop_ihs(action,ip,configfile)
                #varnish
                operate_varnish.start_stop_varnish(action,ip,configfile)
                #apache
                operate_apache.start_stop_apache(action,ip,configfile)
                #mysql
                operate_mysql.start_stop_mysql(action,ip,configfile)
                #db2
                operate_db2.start_stop_db2(action,ip,configfile)
                #nginx
                operate_nginx.start_stop_nginx(action,ip,configfile)
                #tomcat
                operate_tomcat.start_stop_tomcat(action,ip,configfile)
                #redis
                operate_redis.start_stop_redis(action,ip,configfile)
                #jboss
                operate_jboss.start_stop_jboss(action,ip,configfile)
                #mongodb
                operate_mongodb.start_stop_mongodb(action,ip,configfile)
                #logstash
                operate_logstash.start_stop_logstash(action,ip,configfile)
                #flume
                operate_flume.start_stop_flume(action,ip,configfile)
                #mq
                operate_mq.start_stop_mq(action,ip,configfile)
                #java
                operate_java.start_stop_java(action,ip,configfile)
            except:
                 print "%s 22 端口不能连接.\r\n" % ip
