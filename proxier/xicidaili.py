#coding: utf-8
__author__ = 'liufei'

import sys, time
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class xicidaili(base):
    def __init__(self):
        self.data = data()
        self.base = base()
        self.url = self.data.xicidaili
        self.bs = None

    def getLatestFreeURL(self):
        '''
                # 获取该网站最新免费代理页面URL
        '''
        urls = []
        for i in range(self.data.xicidail_pagescount):
            urls.append(self.url % (i+1))
        return urls

    def getProxies(self, url):
        '''
                # 获取目标页面中免费代理
        '''
        html = self.base.request_url(url)
        bs = BS(html, from_encoding="utf8")
        bs = bs.findAll("tr")[1:]
        proxies = []
        for td in bs:
            ip = td.findAll("td")[1].text
            port = td.findAll("td")[2].text
            level = td.findAll("td")[4].text
            if "高匿" in level:
                proxies.append(ip+":"+port)
        return proxies

    def save(self, filename, mode):
        latestUrls = self.getLatestFreeURL()
        result = []
        for url in latestUrls:
                proxies = self.getProxies(url)
                if proxies:
                    result += proxies
                else:
                    break
        base.sava_result(filename, result, mode)
        print time.strftime("%Y-%m-%d %X", time.localtime()) + " | [西刺代理] - Proxy count is %d!" % len(result)

if __name__ == "__main__":
    filename = "/Users/luca/WebServer/Documents/xicidaili.txt"
    while True:
        xcdl = xicidaili()
        xcdl.save(filename, "w")
        time.sleep(180)

