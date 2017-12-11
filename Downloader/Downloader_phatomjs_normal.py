#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from adsl import Adsl
import lxml.html
from random import randint
import requests
import threading
import re
#global mutex
#mutex = threading.Lock()

class downloader(object):
    def __init__(self,base_url='',temp_num=10):
        try:
            time.sleep(randint(0,5)*0.1)
            U_A = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
                   'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
                   'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36']

            u_a = U_A[randint(0,len(U_A)-1)]
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = u_a
            cap["phantomjs.page.customHeaders.User-Agent"] = u_a
            if randint(0,9) < 10:
                self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs.exe',service_log_path='C:/ghostdriver.log',desired_capabilities=cap) #,desired_capabilities=cap
            else:
                # use chrome
                chromedriver = "C:\Users\Administrator\AppData\Local\Google\Chrome\Application\Chromedriver.exe"
                os.environ["webdriver.chrome.driver"] = chromedriver
                self.driver = webdriver.Chrome(chromedriver)
                # self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs.exe',
                #                                   service_log_path='C:/ghostdriver.log')

            # use ie
            # IEdriver='C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe'
            # os.environ["webdriver.ie.driver"] = IEdriver
            # self.driver = webdriver.Ie(IEdriver)
            #self.driver = webdriver.Firefox()

            self.driver.set_page_load_timeout(2000)
            self.base_url = base_url
            if self.base_url != '':
                self.driver.get(self.base_url)
                time.sleep(0.5)
                if len(self.driver.page_source) < 50:
                    aa = Adsl()
                    aa.connect()
            self.temp = 0
            self.temp_num = temp_num
            if self.temp_num == None:
                self.temp_num = 10

        except Exception,e:
            print 'downloader init failed...',e

    def goto_init(self):
        # self.driver.get('https://tmall.com')
        self.temp = 0

    def goto_home(self):
        if self.base_url != '':
            self.driver.get(self.base_url)
            time.sleep(1)

    def get_page(self, url,pre_url,mutex,arg_list,min_len=40):
        while True:
            try:
                # print u'开始加载网页...'
                if len(pre_url)>0:
                    for each_url in pre_url:
                        self.driver.get(each_url)
                        time.sleep(0.5)
                #print 'current_url',url
                self.driver.get(url)
                time.sleep(randint(0,15)*0.1)
                #print 'current_url',self.driver.current_url
                current_url = self.driver.current_url
                status = True
                for each_kw in arg_list:
                    if each_kw in current_url:
                        status = False
                        break
                if len(self.driver.page_source) > min_len and status: 
                    # print u'完成网页加载...'
                    self.goto_init()
                    #mutex.release()
                    return self.driver.page_source

                else:
                    print 'length:',len(self.driver.page_source),'current_url:',self.driver.current_url[:20],'origon_url:',url[:20]
                    #self.driver.get('https://www.baidu.com/')
                    #if len(self.driver.page_source) < 50:
                    #print u'跳转到登陆页...'
                    mutex.acquire()
                    #print 'origion url',url
                    #print 'current_url',self.driver.current_url
                    print u'重新拨号...'
                    aa = Adsl()
                    if aa.reconnect(url):
                        #time.sleep(2)
                        self.temp += 1
                        self.goto_home()
                        #time.sleep(1)
                        print 'temp:', self.temp
                        # time.sleep(self.temp*60)
                    mutex.release()
                    if self.temp == self.temp_num:
                        print u'尝试%s次均失败，作保存处理...'%(self.temp_num-1)
                        self.goto_init()
                        #mutex.release()
                        time.sleep(randint(9,11)*60)
                        return False
                        break
                    #else:
                    #    print u'already connected...'
            except Exception, e:
                print 'get_page err: ', e
                #mutex.release()
                return False
                break



    def delete(self):
        try:
            self.driver.quit()
        except:
            pass


if __name__ == '__main__':
    d = downloader()
    urls = [
            'https://detail.tmall.hk/hk/item.htm?id=546956520560&is_b=1&cat_id=51234037&rn=76615c9bf4eb7d79ba8f450a5693cac7',
            'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.1a8Vp2&id=545828211529&skuId=3459326151229&sku=122216531:27553497&standard=1&user_id=3164693811&cat_id=50918005&is_b=1&rn=7b086cc1736f3a42e619fba73d4cd9d9',
            'https://detail.tmall.com/item.htm?id=546249451559&is_b=1&cat_id=50024400&q=&rn=10e35e1a0caa2a012a770744d8d2218b=1&rn=cbb0e0a83edbd5bbb3faeefd8394d58f']
    #urls = ['https://detail.tmall.com/item.htm?id=546249451559&is_b=1&cat_id=50024400&rn=10e35e1a0caa2a012a770744d8d2218b',
            #'https://detail.tmall.com/item.htm?id=546249451559&is_b=1&cat_id=50024400&rn=10e35e1a0caa2a012a770744d8d2218b&sku_properties=10004:385316259;5919063:6536025']
    for url in urls[0:1]:
        
        res = d.get_page(url,[],threading.Lock(),['login','sec.taobao'],min_len=40)
        #print res
        res = lxml.html.document_fromstring(res)
        sales = res.xpath('//li[@class="tm-ind-item tm-ind-sellCount "]/div[@class="tm-indcon"]/span[@class="tm-count"]/text()')
        time.sleep(3)
        print sales
    d.delete()
    time.sleep(10)
