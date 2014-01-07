#!/bin/env python
# -*- coding:utf-8

import sys, os
import urllib

test_html='''
<script>parent.document.getElementById('detail').innerHTML+='<ul class="head"><li>序号</li><li>Ping的地点</li><li>响应IP</li><li>响应时间</li><li>TTL</li><li>赞助商 <img alt="赞助点联系QQ：1751691323" title="赞助点联系QQ：1751691323" onclick="super1()"  src="/template/default/images/helptip.gif"/></li></ul>';
''''''</script><script>parent.document.getElementById('detail').innerHTML+='<ul><li>1</li><li>上海[多线]</li><li><a href="http://ip.chinaz.com/?IP=112.84.105.38">112.84.105.38</a></li><li style="">43毫秒</li><li>51</li><li><a href="http://www.pdidc.com" target=_blank>浦东数据中心(BGP)</a></li></ul>';</script><script>parent.document.getElementById('detail').innerHTML+='<ul><li>2</li><li>河南郑州[多线]</li><li><a href="http://ip.chinaz.com/?IP=182.118.15.39">182.118.15.39</a></li><li style="">6毫秒</li><li>55</li><li><a href="http://www.37idc.com" target=_blank>37互联 云VPS</a></li></ul>';</script><script>parent.document.getElementById('countresult').innerHTML='最快：河南郑州[多线] <font color="blue"> 6 </font>毫秒&nbsp;&nbsp;&nbsp;&nbsp;最慢：上海[多线] <font color="blue"> 43 </font>毫秒</font><br/>';</script>
'''

base_url = 'http://ping.chinaz.com'

from sgmllib import SGMLParser
class chinaz_ping_Parser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.htmltag = {}
        self.head = []
        self.line = []
        self.lines = []

    def tag_start(self, tag):
        tag = 'htmltag_'+tag
        if not hasattr(self.htmltag, tag): self.htmltag[tag] = 0
        self.htmltag[tag] += 1
        #print tag+': '+ str(self.htmltag[tag])

    def tag_end(self, tag):
        tag = 'htmltag_'+tag
        if not hasattr(self.htmltag, tag): self.htmltag[tag] = 1
        self.htmltag[tag] -= 1
        #print tag+': '+ str(self.htmltag[tag])

    def in_tag(self, tag):
        tag = 'htmltag_'+tag
        return self.htmltag.get(tag, None)

    def start_iframe(self, attrs):
        src = ''.join([ val for key, val in attrs if key == 'src' and val.find('host') >= 0 ])
        if len(src):
            self.ping_iframe_src = src
            return self.ping_iframe_src

    def start_ul(self, attrs):
        ul_class = ''.join([ val  for key, val in attrs if key == 'class' ])
        if ul_class.find('head') >= 0:
            self.tag_start('head_ul')
        else:
            self.tag_start('ul')

    def end_ul(self):
        if self.in_tag('head_ul'): self.tag_end('head_ul')
        else:
            self.lines.append(self.line)
            self.line=[]
            self.tag_end('ul')

    def start_li(self, attr):
        self.tag_start('li')
        
    def end_li(self):
        self.tag_end('li')

    def handle_data(self, text):
        if self.in_tag('head_ul') and self.in_tag('li'):
           self.head.append(text) 

        elif self.in_tag('li'):
           self.line.append(text) 
           
def print_log(log):
    if sys.platform.find('win') >= 0:
        log = log.decode('utf-8').encode('GBK')
    print str(log)

def chinaz_ping(host='www.163.com', linetype=['电信', '联通', '多线', '移动']):
    if type(linetype) == str: linetype = [linetype,]
    linetype = '&'.join([ 'linetype='+urllib.quote(str(i)) for i in linetype if len(i) ])
    submit_url = "%s/?host=%s&%s" % (base_url, host, linetype)
    if sys.platform.find('win') < 0:
        print_log(submit_url)
    respon_fd = urllib.urlopen(submit_url)

    Parser = chinaz_ping_Parser()
    Parser.feed(urllib.urlopen(submit_url).read())
    Parser.close()
    ping_respon_url = "%s/%s" % ( base_url, Parser.ping_iframe_src )
    #print_log(ping_respon_url)

    Parser = chinaz_ping_Parser()
    Parser.feed(urllib.urlopen(ping_respon_url).read().decode('UTF-8'))
    Parser.close()
    return Parser.head, Parser.lines

def show_respon(head, lines):
    rows = [head] + lines

    widths = [ max(map(lambda x: len(x) <= 2 and len(x)*2 or len(x), col)) 
                                                    for col in zip(*rows) ]
    print widths
    for row in rows:
        print "\t".join((val.ljust(width) for val, width in zip(row, widths)))
    return
    def get_head_width(string):
        if string.find('IP') >= 0: return 10
        elif string.find('地点') >= 0: return 10
        elif string.find('赞助') >= 0: return 10
        elif string.find('序号') >= 0: return 4
        elif string.find('时间') >= 0: return 4
        elif string.find('TTL') >= 0: return 4
        else: return 4

    print '\t'.join([ x.ljust(get_head_width(x)) for x in head ])
    for line in lines:
        print '\t'.join([ x for x in line] )
    
def test(): pass

if __name__ == '__main__':
    if sys.platform.find('win') >= 0:
        reload(sys)
        sys.setdefaultencoding('GBK')
    
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    else:
        #host = 'www.163.com'
        sys.stdout.write(u"请输入主机名:")
        host = sys.stdin.readline().strip()
    
    print_log(str(host)+' 测试已执行， 等待结果返回……')
    #head, lines =  chinaz_ping(linetype=['电信','联通','多线', '移动','海外'])
    #head, lines =  chinaz_ping(host, '多线')
    head, lines =  chinaz_ping(host)
    show_respon(head, lines)
    if sys.platform.find('win') >= 0: sys.stdin.readline(1)
