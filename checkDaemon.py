#!/bin/env python
# -*- coding:utf-8 -*-
import os, sys 

def checkDaemon( name, pidfile=-1):
    """检查进程是否已运行"""
    if pidfile == -1:
        pidfile = "/var/run/%s.pid" % (name)
    elif not pidfile:  ## 没有 pidfile, 通过 pgrep 过滤进程
        pidfile = None 
        child_stdin, child_stdout = os.popen2("pgrep %s" % (name))
        pid = int(child_stdout.readline())
        if not pid: return None
        else: return pid
    try:
        pid = int(file(pidfile).readline())
    except Exception, e:
        return 1

    statusfile = '/proc/%s/stat' % pid
    if os.path.exists(statusfile):
        try:
            pidName = file(statusfile).readline().split()[1].strip('()')
        except Exception, e:
            return 1
        if pidName == name: return pid
        else: return None
    else:
        return None

if sys.platform.find('nux') < 0:
    raise OSError, "Can only be run on the *nux OS"
if __name__ == '__main__':
    print checkDaemon('crond')
