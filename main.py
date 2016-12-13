#coding: utf-8
__author__ = 'liufei'

import sys, time
from proxier.youdaili import youdaili
from proxier.kuaidaili import kuaidaili
from proxier.xicidaili import xicidaili

reload(sys)
sys.setdefaultencoding('utf-8')
class spider:
    def __init__(self, iptype):
        self.iptype = iptype
        self.ydl = youdaili()
        self.kdl = kuaidaili()
        self.xcdl = xicidaili()

    def run(self, filename):
        if self.iptype == 0:
            self.kdl.save(filename, "w")
            self.xcdl.save(filename, "a")
        elif self.iptype == 1:
            self.ydl.save(filename, "w")
        else:
            self.ydl.save(filename, "w")
            self.xcdl.save(filename, "a")
            self.kdl.save(filename, "a")

if __name__ == "__main__":
    filename = "/Users/luca/WebServer/Documents/proxies.txt"
    spider = spider(0)
    while True:
        spider.run(filename)
        time.sleep(300)
