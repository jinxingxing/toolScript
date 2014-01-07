#!/usr/bin/env  python
#coding: gbk
"""
页面分割
待做的功能:
1. 指定贴子的首页， 自动下载楼主所有的贴子然后过滤回复贴中长度小于50的内容(不下载css, script, img 到本地)
2. 分析html下载css, script, img 到本地
3. *
"""
import sys, os
from bs4 import BeautifulSoup
import urllib, urllib2
from urlparse import urlparse

def filename2localencode(filename):
    if isinstance(filename, unicode):
        return filename.encode(sys.getfilesystemencoding())
    else:
        return unicode(filename).encode(sys.getfilesystemencoding())

#print urllib2.unquote(testurl).decode("utf8")
#sys.exit(0)
#testurl = filename2localencode(testurl)
class MFPage(object):
    def __init__(self, url):
        url = urllib2.unquote(testurl).decode("utf8")
        respon = urllib2.urlopen(url)
        html = respon.read()
        #html =  open(testurl).read()
        #print respon.headers.dict
        #print respon.headers.getencoding()
        self.soup = BeautifulSoup(html)
    
    def __getattr__(self, name):
        return getattr(self.soup, name)
        
    def __str__(self):
        return str(self.soup)
        
    def html_head_s(self):
        return str(self.soup.head)
        
    def tag_in_body_s(self, tagname):
        return "\n".join(map(str, self.soup.body.find_all(tagname)))
    
    def script_and_link_in_body_s(self):
        return "%s\n%s" % ( self.tag_in_body("link"),
                            self.tag_in_body("script") )
    
    def split_page_head(self):
        tmp_soup = BeautifulSoup()
        tmp_soup.append(self.soup.head)
        for tag in self.soup.body.find_all("link"):
            tmp_soup.append(tag)
        for tag in self.soup.body.find_all("script"):
            tmp_soup.append(tag)
        return tmp_soup
        
    def split_page_head_s(self):
        return str(self.split_page_head())
    
    def decompose_by_name(self, tagname):
        for tag in self.soup.find_all(tagname):
            tag.decompose()
    
    def decompose_by_id(self, tagid):
        for tag in self.soup.find_all(id=tagid):
            tag.decompose()
    
    def decompose_by_class(self, tagclass):
        for tag in self.soup.find_all(class_=tagclass):
            tag.decompose()
    
    def decompose_by_select(self, select_):
        for tag in self.soup.select(select_):
            tag.decompose()
    
    def first_page(self):
        new_soup  = BeautifulSoup(self.split_page_head())
        new_soup.wrap(soup.new_tag("html"))
        
def decompose_by_select(_soup, selecter):
    for tag in _soup.select(selecter):
        tag.decompose()
        
def decompose_by_find_all(_soup, *args, **kwargs):
    for tag in _soup.find_all(*args, **kwargs):
        tag.decompose()
    
def split_page(mainurl):
    page = MFPage(mainurl)
    #print page.html_head()
    #print page.script_and_link_in_body()
    for x in page.soup.select("#header .top"): x.decompose()
    for x in page.soup.select("#header .nav"): x.decompose()
    for x in page.soup.find_all(id="topic_crumb_top"): x.decompose()
    for x in page.soup.find_all(id="topic_filter_head"): x.decompose()
    for x in page.soup.find_all(id="footer"): x.decompose()
    for x in page.soup.find_all(id="topic_reply"): x.decompose()
    for x in page.soup.select("#go-top"): x.decompose()
    for x in page.soup.select("#feedback"): x.decompose()
    postbits = page.soup.select("div#topic_post_list div.postbit")
    all_css_tag = page.soup.find_all(rel="stylesheet")
    all_css_tag.extend(page.soup.find_all("style", type="text/css"))
    first_postbit = postbits[0]
    #print first_postbit
    postlen = len(postbits)
    for i in xrange(1, postlen):
        onepage = postbits[i]
        for css_tag in all_css_tag:
            onepage.append(css_tag)
        onepage.table["width"]="50%"
        onepage.table["align"]="center"
        
        posttime = onepage.table.select(".postbit_time")[0]
        posttitle = onepage.table.select(".postbit_title")[0]
        posttime.append(posttitle)
        onepage.table.select(".postbit_title")[0].decompose()
        onepage.table.select(".postbit_author")[0].decompose()
        
        onepage.append( page.soup.new_tag("div", id="soup_add-pageindex", width="80%", align="right"))
        pageindex =  page.soup.find(id="soup_add-pageindex")
        
        tag =  page.soup.new_tag("a", href="index.html")
        tag.append( page.soup.new_string(u"&nbsp;首页&nbsp;"))
        onepage.append(tag)
        
        if i > 1:
            tag =  page.soup.new_tag("a", href="page.%d.html" % (i-1))
            tag.append( page.soup.new_string(u"&nbsp;上一页&nbsp;"))
            onepage.append(tag)
        if i < postlen-1:
            tag =  page.soup.new_tag("a", href="page.%d.html" % (i+1) )
            tag.append( page.soup.new_string(u"&nbsp;下一页&nbsp;"))
            onepage.append(tag)
        
        open("page.%s.html" % i, 'wb').write(str(page.soup.head)+str(onepage))
        #postbits[i].decompose()
        

    for css_tag in all_css_tag:
            page.soup.append(css_tag)
            
    #page.soup.append(postbits[0])
    page.soup.append(page.soup.new_tag("div", id="soup_add-pageindex-first", width="80%"))
    pageindex = page.soup.find(id="soup_add-pageindex-first")
    tag = page.soup.new_tag("a", href="index.html")
    tag.append(page.soup.new_string(u"&nbsp;第001页&nbsp;"))
    pageindex.append(tag)
    for i in xrange(1, len(postbits)):
        postbits[i].decompose()
        if i % 20 == 0:
            pageindex.append(page.soup.new_tag("br"))
        tag = page.soup.new_tag("a", href="page.%d.html" % (i))
        tag.append(page.soup.new_string(u"&nbsp;第%03d页&nbsp;" % (i+1)))
        pageindex.append(tag)
        
    print pageindex
    
    page.soup.append(pageindex)
    open("index.html", 'w').write(str(page.soup))

def main():
    testurl=r"E:\pro_data\百度云\code\py\美国摩托日记 - 磨房.htm"
    testurl=r"file:///E:/pro_data/%E7%99%BE%E5%BA%A6%E4%BA%91/code/py/%E7%BE%8E%E5%9B%BD%E6%91%A9%E6%89%98%E6%97%A5%E8%AE%B0%20-%20%E7%A3%A8%E6%88%BF.htm"
    testurl = r"http://www.doyouhike.net/forum/topic_filter?tid=944422&uid=955214"
    testurl = r"http://www.doyouhike.net/forum/topic_filter?tid=516916&uid=567723"
    #split_page(testurl)
    print testurl
    req = urllib2.Request(testurl)
    req.add_header("Referer", "http://www.doyouhike.net/forum/globe/516916.html")
    open('globe.out.html', 'wb').write(urllib2.urlopen(req).read())
    #print urllib.urlretrieve(req, 'rout.html')
    
def down_load_res():
    in_file = "globe.out.html"
    out_dir = "res_out"
    out_file = in_file+'.r.html'
    soup = BeautifulSoup(open(in_file))
    for tag in soup.find_all(lambda tag: tag.has_attr('src') ):
        try:
            src_url = tag.get("src")
            parse_r = urlparse(src_url)
            filepath = "%s%s"  % (parse_r.netloc.replace(':', '.'), parse_r.path)
            out_filepath = out_dir+'/'+filepath
            if not os.path.exists(out_filepath):
                print src_url, "downloading..."
                if not os.path.isdir(os.path.dirname(out_filepath)):
                    os.makedirs(os.path.dirname(out_filepath))
                try:
                    open(out_filepath, "wb").write(urllib2.urlopen(src_url).read())
                except Exception , e:
                    print e
                    if os.path.exists(out_filepath):
                        os.remove(out_filepath)
            else:
                print src_url, "file exists, skip download"
            tag["src"] = src_url.replace(parse_r.scheme+"://", out_dir+"/")
        except Exception, e:
            import traceback
            traceback.print_exc()
            print e
    open(out_file, "wb").write(str(soup))
if __name__ == "__main__":
    #main()
    down_load_res()


    