#coding: utf-8
__author__ = 'liufei'

import sys, threading
import time
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class kuaidaili:
    def __init__(self):
        self.data = data()
        self.base = base()
        self.url = self.data.kuaidaili
        self.bs = None

    def getLatestFreeURL(self):
        '''
                # 获取该网站最新免费代理页面URL
        '''
        urls = []
        for i in range(self.data.kuaidaili_pagescount):
            urls.append(self.url % (i+1))
        return urls

    def getProxies(self, url):
        '''
                # 获取目标页面中免费代理
        '''
        html = self.base.request_url(url)
        print html
        bs = BS(html)
        ip = bs.findAll(name="td", attrs={"data-title": "IP"})
        port = bs.findAll(name="td", attrs={"data-title": "PORT"})
        level = bs.findAll(name="td", attrs={"data-title": "匿名度"})
        type = bs.findAll(name="td", attrs={"data-title": "类型"})
        proxies = []
        proxy = zip(ip, port, level, type)
        for p in proxy:
            # if "匿名" in p[2].text and "HTTPS" in p[3].text:
            if "匿名" in p[2].text:
                proxies.append(p[0].text+":"+p[1].text)
        return proxies

    def save(self, filename, mode):
        latestUrls = self.getLatestFreeURL()
        result = []
        for url in latestUrls:
            try:
                proxies = self.getProxies(url)
            except:
                pass
            if proxies:
                result += proxies
        base.sava_result(filename, result, mode)
        print time.strftime("%Y-%m-%d %X", time.localtime()) + " | [快代理] - Proxy count is %d!" % len(result)

    def run(self, filename, updateGap):
        while True:
            self.save(filename, "w")
            time.sleep(updateGap)

if __name__ == "__main__":
    kdl = kuaidaili()
    threads = []
    threads.append(threading.Thread(target=kdl.run, args=("kuaidaili.txt", 300)))
    threads.append(threading.Thread(target=base.httpService))
    for t in threads:
        t.setDaemon(True) #设置线程为后台线程
        t.start()
    for t in threads:
        t.join()

    # 访问抓取的代理地址,例: http://127.0.0.1:8083/kuaidaili.txt