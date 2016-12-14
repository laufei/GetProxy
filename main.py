#coding: utf-8
__author__ = 'liufei'

import sys, time, threading
from proxier.youdaili import youdaili
from proxier.kuaidaili import kuaidaili
from proxier.xicidaili import xicidaili
from lib.base import base

reload(sys)
sys.setdefaultencoding('utf-8')
class spider:
    def __init__(self, iptype):
        self.iptype = iptype
        self.ydl = youdaili()
        self.kdl = kuaidaili()
        self.xcdl = xicidaili()

    def run(self, filename, updateGap):
        while True:
            if self.iptype == 0:    # 抓取快代理&西刺的高匿代理
                self.kdl.save(filename, "w")
                self.xcdl.save(filename, "a")
            elif self.iptype == 1:  # 抓取有代理的所有免费代理
                self.ydl.save(filename, "w")
            else:       # 抓取快代理&西刺&有代理的所有免费代理
                self.ydl.save(filename, "w")
                self.xcdl.save(filename, "a")
                self.kdl.save(filename, "a")
            time.sleep(updateGap)

if __name__ == "__main__":
    sp = spider(0)
    threads = []
    threads.append(threading.Thread(target=sp.run, args=("proxies.txt", 300)))
    threads.append(threading.Thread(target=base.httpService))
    for t in threads:
        t.setDaemon(True) #设置线程为后台线程
        t.start()
    for t in threads:
        t.join()

    # 访问抓取的代理地址, 例: http://127.0.0.1:8083/proxies.txt
