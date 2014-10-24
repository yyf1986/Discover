#!/usr/bin/python
#-*- coding: utf-8 -*-

from script.discovery import discovery_system
from script.discovery import discovery_was
from script.discovery import discovery_ihs
from script.discovery import discovery_varnish
from script.discovery import discovery_apache
from script.discovery import discovery_mysql
from script.discovery import discovery_db2
from script.discovery import discovery_nginx
from script.discovery import discovery_tomcat
from script.discovery import discovery_redis
from script.discovery import discovery_jboss
from script.discovery import discovery_mongodb
from script.discovery import discovery_java
from script.discovery import discovery_logstash
from script.discovery import discovery_flume
from script.discovery import discovery_mq

import socket
import sys

if __name__ == '__main__':
    with open('ip.txt') as lines:
        for line in lines:
            ip = line.strip('\r\n')
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip,22))
                s.close()
                ret = ""
                fp = open('./conf/'+ip+'.txt','w+')
                ret +=ip+"\r\n"
                fs_status = discovery_system.get_fsinfo(ip)
                ret +="%s\r\n" % fs_status
                ftp_status = discovery_system.get_ftpstatus(ip)
                ret +="ftp:%s\r\n" % ftp_status
                ntpd_status = discovery_system.get_ntpd(ip)
                ret +="ntpd:%s\r\n" % ntpd_status
                sendmail_status = discovery_system.get_sendmail(ip)
                ret +="sendmail:%s\r\n" % sendmail_status
                postfix_status = discovery_system.get_postfix(ip)
                ret +="postfix:%s\r\n" % postfix_status
                iptables_status = discovery_system.get_iptables(ip)
                ret +="iptables:%s\r\n" % iptables_status
                selinux_status = discovery_system.get_selinux(ip)
                ret +="selinux:%s\r\n" % selinux_status
                nfs_status = discovery_system.get_nfs(ip)
                ret +="nfs:%s\r\n" % nfs_status
                tivoli_status = discovery_system.get_tivoli(ip)
                ret +="tivoli:%s\r\n" % tivoli_status
                #was
                if discovery_was.get_was(ip) != "":
                    ret +=discovery_was.get_was(ip)+"\r\n"
                #ihs
                if discovery_ihs.get_ihs(ip) != "":
                    ret +=discovery_ihs.get_ihs(ip)+"\r\n"
                #varnish
                if discovery_varnish.get_varnish(ip) != "":
                    ret +=discovery_varnish.get_varnish(ip)+"\r\n"
                #apache
                if discovery_apache.get_apache(ip) != "":
                    ret +=discovery_apache.get_apache(ip)+"\r\n"
                #mysql
                if discovery_mysql.get_mysql(ip) != "":
                    ret +=discovery_mysql.get_mysql(ip)+"\r\n"
                #db2
                if discovery_db2.get_db2(ip) != "":
                    ret +=discovery_db2.get_db2(ip)+"\r\n"
                #nginx
                if discovery_nginx.get_nginx(ip) != "":
                    ret +=discovery_nginx.get_nginx(ip)+"\r\n"
                #tomcat
                if discovery_tomcat.get_tomcat(ip) != "":
                    ret +=discovery_tomcat.get_tomcat(ip)+"\r\n"
                #redis
                if discovery_redis.get_redis(ip) != "":
                    ret +=discovery_redis.get_redis(ip)+"\r\n"
                #jboss
                if discovery_jboss.get_jboss(ip) != "":
                    ret +=discovery_jboss.get_jboss(ip)+"\r\n"
                #mongodb
                if discovery_mongodb.get_mongodb(ip) != "":
                    ret +=discovery_mongodb.get_mongodb(ip)+"\r\n"
                #logstash
                if discovery_logstash.get_logstash(ip) != "":
                    ret +=discovery_logstash.get_logstash(ip)+"\r\n"
                #flume
                if discovery_flume.get_flume(ip) != "":
                    ret +=discovery_flume.get_flume(ip)+"\r\n"
                #mq
                if discovery_mq.get_mq(ip) != "":
                    ret +=discovery_mq.get_mq(ip)+"\r\n"
                #java
                if discovery_java.get_java(ip) != "":
                    ret +=discovery_java.get_java(ip)+"\r\n"
                
                fp.write(ret)
                print ret
                if fp != None:
                    fp.close()
            except:
                print "%s 22 端口不能连接.\r\n" % ip
