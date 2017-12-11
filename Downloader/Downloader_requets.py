#coding:utf-8
import requests
import time
from random import randint
from adsl import Adsl

class downloader(object):
    def __init__(self,base_url=''):
        self.base_url = base_url
        self.headers={
    'Host': 'tmall.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    }
        if self.base_url != '':
            requests.get(self.base_url,headers=self.headers)
        self.temp = 0

    def goto_init(self):
        self.temp = 0

    def goto_home(self):
        if self.base_url != '':
            requests.get(self.base_url,self.headers)

    def get_page(self, url,mutex):
        while True:
            try:
                # print u'开始加载网页...'
                response = requests.get(url,headers=self.headers,allow_redirects=False)
                time.sleep(1)
                if response.status_code == 200 and 'login' not in response.headers['location']:
                    # print u'完成网页加载...'
                    self.goto_init()
                    return response.text
                    break
                else:
                    mutex.acquire()
                    print u'跳转到登陆页...'
                    print u'重新拨号...'
                    aa = Adsl()
                    aa.reconnect(url)
                    time.sleep(2)
                    self.temp += 1
                    self.goto_home()
                    time.sleep(1)
                    mutex.release()
                    print 'temp:', self.temp
                    if self.temp == 51:
                        print u'尝试50次均失败，作保存处理...'
                        self.goto_init()
                        time.sleep(30)
                        return False
                        break
            except Exception, e:
                print 'get_page err: ', e
                return False
                break
