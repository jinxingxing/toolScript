#!/bin/env python
# -*- coding: utf-8 -*-

"""
sina blog  文章下载(待完善)
"""
import os,sys
from urllib2 import  urlopen
from HTMLParser import HTMLParser, HTMLParseError

from sgmllib import SGMLParser
import re

class blogUrlParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.is_nextPage_span = False
        self.nextPage_href = ''
        self.last_a_href = ''
        self.print_href = ''
        self.curr_tag = ''

        self.title = ''

    def handle_data(self, text):
        if text.find('后一篇') >= 0:
            self.is_nextPage_span = True;

        elif text.find('打印') >= 0:
            self.print_href = self.last_a_href

        if self.curr_tag == 'title':
            self.title = text

    def start_title(self, attrs):
        self.curr_tag = 'title' 

    def end_title(self):
        self.curr_tag = '' 
    
    def start_a(self, attrs):
        self.curr_tag = 'a'
        href = [v for k, v in attrs if k=='href'] 
        href = ''.join(href)

        self.last_a_href = href

        if  self.is_nextPage_span: 
            self.is_nextPage_span = False
            self.nextPage_href = href

    def end_a(self):
        self.curr_tag = '' 

def myUrlOpen(url):
        html_code =  ''
        for line in urlopen(url).readlines():
            if line.find(r'<!') >= 0:
                continue
            html_code += line 
        return html_code

class pdfUrlParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.fileDownloadUrl = ''

    def start_a(self, attrs):
        #print attrs
        href = [v for k, v in attrs if k=='href']
        href = ''.join(href)
        id = [v for k, v in attrs if k=='id']
        id = ''.join(id)
        #print href, id
        if id == 'fileLinkIcon':
            #print href
            self.fileDownloadUrl = href

def downLoadFile(url, filename=None):
    if not filename:
        filename = os.path.basename(url).split('?')[0]
    rfd = urlopen(url)
    wfd = open(filename, 'w') 
    while True:
        line = rfd.readline()
        if not line: break
        wfd.write(line)

    wfd.close()
        

def getPDFDownLoadURL(url):
    preUrl = r'http://www.web2pdfconvert.com/engine.aspx?lowquality=false&porient=portrait&infostamp=false&logostamp=true&allowplugins=false&allowscript=true&showpagenr=false&margintop=10&marginleft=5&marginbottom=10&marginright=5&psize=a4&userpass=&ownerpass=&allowcopy=true&allowedit=true&allowprint=true&title=&author=&subject=&keywords=&conversiondelay=1&printtype=false&nobackground=false&outline=false&ref=form&cURL='
    getUrl = preUrl + url 
    
    html_code = myUrlOpen(getUrl)
    pdfP =  pdfUrlParser()
    pdfP.feed(html_code)
    return pdfP.fileDownloadUrl

def main(first_page_href):
    nextPage_href = first_page_href
    lister=blogUrlParser()

    while nextPage_href:
        html_code  = myUrlOpen(nextPage_href)
        lister.reset()
        lister.feed(html_code)

        nextPage_href = lister.nextPage_href
        blogID = re.split(r'[:/_.]', nextPage_href)[-2]
        title = lister.title
        print_href =  lister.print_href
        print title, print_href,
        downURL = getPDFDownLoadURL(print_href)
        print downURL
        print 'start download: ' + title
        downLoadFile(downURL, title)
        print 'ok'

if __name__ == "__main_x_":
    #html_code =  ''.join(urlopen("http://blog.sina.com.cn/s/blog_572bd9fc0100048z.html").readlines())
    #print html_code
    html_code =  ''
    for line in file("blog_572bd9fc0100048z.html",'r').readlines():
        if line.find(r'<!') >= 0:
            continue
        html_code += line 
    #print html_code
    hp = MyHTMLParser()
    try:
        hp.feed(html_code)
    except HTMLParseError, e:
        print e
    hp.close()
    print(hp.links)
 

if __name__ == "__main__":
    #html_code =  ''.join(urlopen("http://blog.sina.com.cn/s/blog_572bd9fc0100048z.html").readlines())
    #html_code =  ''.join(file("blog_572bd9fc0100048z.html",'r').readlines())
    #main("http://blog.sina.com.cn/s/blog_572bd9fc0100048z.html") 
    main("http://blog.sina.com.cn/s/blog_9f06fb2d010142tz.html") 
