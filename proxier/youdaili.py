#coding: utf-8
__author__ = 'liufei'

import sys, time
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class youdaili(base):
    def __init__(self):
        self.data = data()
        self.base = base()
        self.url = self.data.youdaili
        self.bs = None

    def getLatestFreeURL(self, url):
        '''
                # 获取该网站最新免费代理页面URL
        '''
        urls = []
        html = self.base.request_url(url)
        self.bs = BS(html, from_encoding="utf8")
        for i in range(self.data.youdaili_newItem):
            url = self.bs.select("ul.ilist_c a")[i].attrs["href"]
            urls.append(url)
        return urls

    def getProxies(self, url):
        '''
                # 获取目标页面中免费代理
        '''
        html = self.base.request_url(url)
        bs = BS(html, from_encoding="utf8")
        proxyModels = bs.select("div.content p span")
        proxies = []
        for p in proxyModels:
            item = p.text.split("@")[0]
            proxies.append(item)
        return proxies

    def save(self, filename, mode):
        latestUrls = self.getLatestFreeURL(self.data.youdaili)
        result = []
        for url in latestUrls:
            pageUrl = url[:-5]
            i = 1
            while True:
                if i == 1:
                    url = pageUrl + ".html"
                else:
                    url = pageUrl + "_%d.html" % i
                proxies = self.getProxies(url)
                if proxies:
                    result += proxies
                    i += 1
                else:
                    break
        base.sava_result(filename, result, mode)
        print time.ctime() + " | 有代理  -   Proxy count is %d!" % len(result)

if __name__ == "__main__":
    filename = "/Users/luca/WebServer/Documents/youdaili.txt"
    while True:
        ydl = youdaili()
        ydl.save(filename)
        time.sleep(180)
