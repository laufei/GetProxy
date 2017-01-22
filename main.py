#coding: utf-8
__author__ = 'liufei'

import sys, time, threading
from proxier.youdaili import youdaili
from proxier.kuaidaili import kuaidaili
from proxier.swei360 import swei360
from proxier.xicidaili import xicidaili
from lib.base import base

reload(sys)
sys.setdefaultencoding('utf-8')
class spider:
    def __init__(self, iptype):
        self.iptype = iptype # 0: 抓取快代理&西刺的高匿代理         # 1: 抓取有代理的所有免费代理       # other: 抓取快代理&西刺&有代理的所有免费代理
        self.ydl = youdaili()
        self.kdl = kuaidaili()
        self.sw360 = swei360()
        self.xcdl = xicidaili()

    def run(self, filename, updateGap):
        while True:
            if self.iptype == 0:    # 抓取360三维代理&西刺的高匿代理
                self.sw360.save(filename, "w")
                self.xcdl.save(filename, "a")
            elif self.iptype == 1:  # 抓取有代理的所有免费代理
                self.ydl.save(filename, "w")
            else:       # 抓取360三维代理&西刺&有代理的所有免费代理
                self.ydl.save(filename, "w")
                self.xcdl.save(filename, "a")
                self.sw360.save(filename, "a")
            time.sleep(updateGap)

if __name__ == "__main__":
    sp = spider(0)
    threads = []
    threads.append(threading.Thread(target=sp.run, args=("proxies.txt", 300)))
    threads.append(threading.Thread(target=base.httpService))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    # 访问抓取的代理地址, 例: http://127.0.0.1:8083/proxies.txt
