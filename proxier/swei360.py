#coding: utf-8
__author__ = 'liufei'

import sys, threading
import time
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class swei360:
    def __init__(self):
        self.data = data()
        self.base = base()
        self.url = self.data.swei360
        self.bs = None

    def getLatestFreeURL(self):
        '''
                # 获取该网站最新免费代理页面URL
        '''
        urls = []
        for i in range(self.data.swei360_pagescount):
            urls.append(self.url % (i+1))
        return urls

    def getProxies(self, url):
        '''
                # 获取目标页面中免费代理
        '''
        html = self.base.request_url(url)
        bs = BS(html)
        proxiesElement = bs.findAll("td")
        ip, port, level, type, proxies = [], [], [], [], []
        for i in range(10):
            ip += proxiesElement[i*8]
            port += proxiesElement[i*8+1]
            level += proxiesElement[i*8+2]
            type += proxiesElement[i*8+3]
        proxy = zip(ip, port, level, type)
        for p in proxy:
            # if "高匿" in p[2] and "HTTPS" in p[3]:
            # if u"\xb8\xdf\xc4\xe4" in p[2]:
                proxies.append(p[0].strip() + ":" + p[1].strip())
        return proxies

    def save(self, filename, mode):
        try:
            latestUrls = self.getLatestFreeURL()
        except:
            return
        result = []
        for url in latestUrls:
            proxies = self.getProxies(url)
            if proxies:
                result += proxies
        base.sava_result(filename, result, mode)
        print time.strftime("%Y-%m-%d %X", time.localtime()) + " | [360代理] - Proxy count is %d!" % len(result)

    def run(self, filename, updateGap):
        while True:
            self.save(filename, "w")
            time.sleep(updateGap)

if __name__ == "__main__":
    kdl = swei360()
    threads = []
    threads.append(threading.Thread(target=kdl.run, args=("360.txt", 300)))
    threads.append(threading.Thread(target=base.httpService))
    for t in threads:
        t.setDaemon(True) #设置线程为后台线程
        t.start()
    for t in threads:
        t.join()

    # 访问抓取的代理地址,例: http://127.0.0.1:8083/360.txt