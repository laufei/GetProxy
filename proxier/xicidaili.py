#coding: utf-8
__author__ = 'liufei'

import sys, time, threading
from bs4 import BeautifulSoup as BS
from data.data import data
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf-8')

class xicidaili:
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
        bs = BS(html)
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
        proxies, result = [], []
        for url in latestUrls:
            try:
                proxies = self.getProxies(url)
            except:
                pass
            if proxies:
                result += proxies
        base.sava_result(filename, result, mode)
        print time.strftime("%Y-%m-%d %X", time.localtime()) + " | [西刺代理] - Proxy count is %d!" % len(result)

    def run(self, filename, updateGap):
        while True:
            self.save(filename, "w")
            time.sleep(updateGap)

if __name__ == "__main__":
    xcdl = xicidaili()
    threads = []
    threads.append(threading.Thread(target=xcdl.run, args=("xicidaili.txt", 300)))
    threads.append(threading.Thread(target=base.httpService))
    for t in threads:
        t.setDaemon(True) #设置线程为后台线程
        t.start()
    for t in threads:
        t.join()

    # 访问抓取的代理地址, 例: http://127.0.0.1:8083/xicidaili.txt
