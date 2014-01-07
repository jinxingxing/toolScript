#!/bin/env python
# -*- coding:utf-8
'''
www.17ce.com ping测试
by jxing, 2013-01-25
v: 20130125.18.35
'''

import sys, os, time
import urllib, urllib2
import json

def do_exit(code=0):
    if sys.platform.find('win') >= 0: sys.stdin.readline(1)
    sys.exit(code)

def my_print(log, *ks):
    if len(ks):
       log = "%s\t%s" % (log, '\t'.join([ str(i) for i in ks]))
    if sys.platform.find('win') >= 0:
        log = log.decode('utf-8').encode('GBK')
    print log

def add_headers(req):
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('Referer', 'http://www.17ce.com/site/ping')
    return req

def ping(target, isplist=[0], arealist=[1,2]):
    '''
提交检查
isp: 1,电信 2,联通 4,其他  6,铁通 7,移动 8,教育网 0,所有
area:区域, 1,大陆 2,港澳台 3,国外 0,所有
返回: tid
    '''
    post_data = "host=%s&url=%s&" % (target, target)
    post_data += '&'.join([ 'isp[]='+urllib.quote(str(i)) for i in isplist])
    post_data += '&' + '&'.join([ 'area[]='+urllib.quote(str(i)) for i in arealist])
    #my_print(post_data) ## @debug
    req = urllib2.Request('http://www.17ce.com/site/ping', data=post_data)
    req = add_headers(req)
    respon_fd = urllib2.urlopen(req)
    ret_dict = json.load(respon_fd)
    if ret_dict.get('message', '') != '':
        my_print(ret_dict.get('message'))
        do_exit(1)
    tid = ret_dict['tid']
    return tid


import re
json_num_key = re.compile(r'([0-9]+)\s*:\s*{')
def ping_fresh(tid, num):
    '''
获取检查结果,并显示
tid:
num: 已获取到的结果数(服务端会返回), 第一次置0即可
返回: num, 如果返回 -1, 表示所有结果已取完
    '''
    post_data = "tid=%s&num=%s" % (tid, num)
    #my_print(post_data) ## @debug
    req = urllib2.Request('http://www.17ce.com/site/ajaxfresh', data=post_data)
    req = add_headers(req)
    respon_fd = urllib2.urlopen(req)
    respon_s  = respon_fd.read()
    ## 返回的 json 存在使用数字作为 key 的情况, 这里进行修正
    json_s  = json_num_key.sub(r'"\1":{', respon_s)
    ret_dict = json.loads(json_s)
    if ret_dict.get('message', '') != '':
        my_print(ret_dict.get('message'))
        do_exit(1)

    num  = ret_dict['num'] 
    taskstatus = ret_dict['taskstatus']
    ret_num = num
    if taskstatus == '3': ret_num = -1  ## taskstatus == '3'表示测试全部完成

    ## 如果没有一台主机的测试已完成, freshdata会是一个空 []
    if len(ret_dict['freshdata']) == 0: return ret_num  
    for key, ping_data in ret_dict['freshdata'].iteritems():
        show_ping_data(ping_data) 
    if len(ret_dict['average_data']) != 0:
        ad = ret_dict['average_data']
        my_print("%s\t%-8s\t%-18s\t%-3s\t%-10s\t%-10s\t%-10s" % 
			('统计数值', 'ISP', '解析出的IP数 '+str(ad['SrcipNum']), ad['PacketsLost'], ad['Min'], ad['Max'], ad['Avg']))
        
    return ret_num

def show_ping_data(ping_data):
    name = ping_data['name']
    isp = ping_data['isp']
    to_ip = ping_data['SrcIP']['srcip']
    lost = ping_data['PacketsLost']
    min = ping_data['Min']
    max = ping_data['Max']
    avg = ping_data['Avg']
    s = "%s\t%-8s\t%-18s\t%-3s\t%-10s\t%-10s\t%-10s"  % (name, isp, to_ip, lost, min, max, avg)
    my_print(s)
    
    
def main():
    reload(sys)
    if sys.platform.find('win') >= 0:
        sys.setdefaultencoding('GBK')
    else:
        sys.setdefaultencoding('UTF-8')
    
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    else:
        sys.stdout.write(u"请输入主机名:")
        host = sys.stdin.readline().strip()
    
    my_print(str(host)+' 测试中……')
    head = "%-16s\t%-8s\t%-18s\t%-3s\t%-10s\t%-10s\t%-10s"  % ('监测点', 'ISP','目标IP', '丢包%', '最小', '最大', '平均')
    my_print(head)
    tid = ping(host)
    num = 0
    while 1:
        num = ping_fresh(tid, num)
        if num == -1: break
        time.sleep(5)

    my_print('http://www.17ce.com/site/ping/%s.html' % (tid))
    do_exit(0)

if __name__ == '__main__':
    main()
