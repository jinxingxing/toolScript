#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
python gui ssh
解析SecureCRT的.ini配置文件， 然后跟据配置参数连接主机
'''

import os, sys
from optparse import OptionParser


#S:"Hostname"=192.168.199.128
#S:"Firewall Name"=None
#S:"Username"=root
#D:"[SSH2] 端口"=00000016

def parserini(inifile):
    inifilename = os.path.basename(inifile)
    retDict = {'title':inifilename}
    def_line = "" #定义变量的一行

    # 变量的定义格式
    # D:"Cursor Key Mode"=00000000

    # line 表示文件的一行
    for line in file(inifile).readlines():
        line = line.strip()
        if line[1:3] == ':"': ## new key
            datatype, key, val = def_line.split('"',3)
            def_line = ""

            val = val.lstrip("=")
            datatype = datatype.rstrip(":")
            #print datatype, key ,val 
            if datatype == 'D': # hexnumber
                val =  int(val, 16)
            retDict[key] = val
            
        def_line = def_line + line
    return retDict

def ssh(ssh_option, hostname, title='', term_option=''):
    if not title: title = 'pgsh -> ' + str(hostname)
    if hostname[0].isdigit(): add_hosts(hostname)

    gui_term_cmd="terminal --title=%s --role=pgsh --hide-menubar -H %s -x" % (title, term_option)
    ssh_cmd ="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 %s" %  (ssh_option)
    cmd = "%s %s" %( gui_term_cmd, ssh_cmd)
    os.system("echo '登陆到 %s ...'" % (hostname))
    os.system(cmd)

def add_hosts(ip):
    for line in file('/etc/hosts').readlines():
            tlist = line.split()
            if tlist and  tlist[0]  == ip: 
               return True
    try:
        file('/etc/hosts', 'a').write('%s %s.remap.%s.com' % (ip, ip, ip))
    except:
        return False
    else:
        return True

def main():
    inifile = sys.argv[1]
    cf = parserini(inifile)
    title = cf['title']
    hostname = cf['Hostname']
    username =  cf.get('Username', 'root')
    sshport  =  cf.get('[SSH2] 端口', 22)
    ssh_opt = "-l %s -p %s %s" % (username, sshport, hostname)
    ssh( ssh_opt, hostname, title=title)

if __name__ == '__main__':
    main()
