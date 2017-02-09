#coding: utf-8
__author__ = 'liufei'

import sys, random, requests
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
from conf.conf import conf
from data.data import data

reload(sys)
sys.setdefaultencoding('utf-8')

class base:
    conf = conf()
    test_url = data().test_url
    ua = random.choice(conf.USER_AGENTS_WEB)
    headers = {"User-Agent": ua,
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'Upgrade-Insecure-Requests': '1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
               }

    @classmethod
    def request_url(cls, url, timeout=100):
        try:
            re = requests.get(url=url, headers=cls.headers, timeout=timeout).text
            return re
        except Exception, e:
            print e

    @classmethod
    def verify_proxy(cls, ip, port):
        proxy = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
        try:
            r = requests.get(url=cls.test_url, headers=cls.headers, timeout=10, proxies=proxy)
            if r.ok or r.text.find(ip) != -1:
                return True
            else:
                return False
        except Exception, e:
            return False

    @classmethod
    def reset_result_file(cls):
        try:
            with open(cls.filename, 'w') as ff:
                    ff.write("")
        except Exception as e:
            assert False, "重置结果文件失败: " + str(e)

    @classmethod
    def sava_result(cls, filename, result, mode='a'):
        try:
            with open(filename, mode) as ff:
                for r in result:
                    ff.write(r+"\r\n")
        except Exception as e:
            assert False, "写入失败: " + str(e)

    @classmethod
    def httpService(cls, HandlerClass = SimpleHTTPRequestHandler, ServerClass = BaseHTTPServer.HTTPServer):
        port = 8083
        server_address = ('', port)
        try:
            httpd = ServerClass(server_address, HandlerClass)
            httpd.serve_forever()
        except Exception, e:
            print e

if __name__ == "__main__":
    print base.verify_proxy("113.18.193.10", "80")


