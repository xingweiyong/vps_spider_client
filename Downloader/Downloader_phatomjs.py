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
    def __init__(self,base_url='',temp_num=50,bt=0):
        try:
            os.system('taskkill /im chrome.exe /f')
            time.sleep(randint(0,5)*0.1)
            self.U_A = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
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
                   'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
                        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
                        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36']

            self.u_a = self.U_A[randint(0,len(self.U_A)-1)]
            self.cap = webdriver.DesiredCapabilities.PHANTOMJS
            self.cap["phantomjs.page.settings.resourceTimeout"] = 1000
            self.cap["phantomjs.page.settings.loadImages"] = True
            self.cap["phantomjs.page.settings.disk-cache"] = True
            self.cap["phantomjs.page.settings.userAgent"] = self.u_a
            self.cap["phantomjs.page.customHeaders.User-Agent"] = self.u_a
            if bt == 1:
                self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs.exe',service_log_path='C:/ghostdriver.log',desired_capabilities=self.cap) #,desired_capabilities=cap
            elif bt == 0:
                # use chrome
                self.chromedriver = "C:\Users\Administrator\AppData\Local\Google\Chrome\Application\Chromedriver.exe"
                self.chrome_options = webdriver.ChromeOptions()
                self.chrome_options.add_argument('--headless')
                self.chrome_options.add_argument('--user-agent=%s'%self.u_a)
                self.driver = webdriver.Chrome(executable_path=self.chromedriver,chrome_options=self.chrome_options)
                #self.driver = webdriver.Chrome(chromedriver)
                #self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs.exe',
                #                                   service_log_path='C:/ghostdriver.log')

            # use ie
            # IEdriver='C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe'
            # os.environ["webdriver.ie.driver"] = IEdriver
            # self.driver = webdriver.Ie(IEdriver)
            #self.driver = webdriver.Firefox()

            self.driver.set_page_load_timeout(500)
            self.base_url = base_url
            if self.base_url != '':
                self.driver.get(self.base_url)
            time.sleep(0.5)
            if len(self.driver.page_source) < 50:
                aa = Adsl()
                aa.connect()
            self.temp = 0
            self.temp_change = 0
            self.temp_num = temp_num
            if self.temp_num == None:
                self.temp_num = 10
            # 三种不同跳转方式
            #self.mode = 0
        except Exception,e:
            print 'downloader init failed...',e

    def goto_init(self):
        # self.driver.get('https://tmall.com')
        self.temp = 0
        self.temp_change = 0

    def goto_home(self):
        if self.base_url != '':
            self.driver.get(self.base_url)
            time.sleep(1)
    def choose_mode(self,url):
        url_list = []
        url_list.append(url)
        url_list.append(re.sub(re.compile('&q=.*?&'),'&',url)+'&sku_properties=')
        url_list.append(re.sub(re.compile('&q=.*?&'),'&',url))
        url_list.append(re.sub(re.compile('&areaId=.*'),'',re.sub(re.compile('&q=.*?&'),'&',url)))
        for index,each_url in enumerate(url_list):
            print 'each_url',each_url
            temp = 0
            while temp < 6:
                aa = Adsl()
                aa.reconnect()
                self.driver.get(each_url)
                res = self.driver.page_source
                res = lxml.html.document_fromstring(res)
                if 'login' not in self.driver.current_url:
                    if len(res.xpath('//span[@class="tm-price"]/text()'))!=0 or len(res.xpath('//li[@class="tm-ind-item tm-ind-sellCount "]/div[@class="tm-indcon"]/span[@class="tm-count"]/text()'))!=0:
                        print 'mode_0',index + 1
                        return index + 1
                    else:
                        print '%d len == 0'%(index+1)
                        temp += 2
                else:
                    print 'login in url'
                    time.sleep(temp)
                    temp += 1
                    
        print 'mode_1',4
        return 4
    def get_page(self, url,pre_url,mutex):
        while True:
            #if self.mode == 0 and 'detail' in url:
            #    self.mode = self.choose_mode(url)
            #if 'detail' in url:
            #    if self.mode == 1:
            #        url = url
            #    elif self.mode == 2:
            #        url = re.sub(re.compile('&q=.*?&'),'&',url)
            #        url = re.sub(re.compile('&areaId=.*'),'',url)
            #    elif self.mode == 3:
            #        url = re.sub(re.compile('&q=.*?&'),'&',url)
            #    elif self.mode == 4:
            #        url = re.sub(re.compile('&q=.*?&'),'&',url)+'&sku_properties='
            try:
                # print u'开始加载网页...'
                if len(pre_url)>0:
                    for each_url in pre_url:
                        self.driver.get(each_url)
                        time.sleep(0.5)
                #print 'current_url',url
                #if 'search_shopitem' in url:
                #    time.sleep(randint(10,30))
                self.driver.get(url)
                '''
                my_headers = {
    'Host': 'tmall.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    }
                '''
                time.sleep(randint(0,15)*0.1)
                #print 'current_url',self.driver.current_url
                res_get_page = self.driver.page_source
                res_get_page = lxml.html.document_fromstring(res_get_page)
                page_source = None
                if 'detail' not in url:
                    if len(self.driver.page_source) > 40 and 'login' not in self.driver.current_url and 'sec.taobao' not in self.driver.current_url:
                        if u'search_shopitem' in url:
                            products = None
                            try:
                                products = self.driver.find_element_by_xpath('//div[@class="product"]')
                            except:
                                pass
                            if products != None:
                                try:
                                    ele = self.driver.find_element_by_xpath('//div[@class="product"][1]/div/p[@class="productTitle"]/a')
                                    #print ele
                                    #ele.click()
                                    
                                    ele.send_keys(Keys.ENTER) 
                                    #time.sleep(5)
                                    #print 'current',self.driver.current_url
                                    #self.driver.close()
                                    #self.driver.back()
                                    time.sleep(5)
                                except:
                                    pass
                                #print 'current',self.driver.current_url
                                page_source = self.driver.page_source
                        self.goto_init()
                        #print self.driver.page_source
                        #time.sleep(100)
                        if page_source is None:
                            page_source = self.driver.page_source
                        return page_source
                else:
                    if len(res_get_page.xpath('//span[@class="tm-price"]/text()')) != 0 or len(res_get_page.xpath(
                            '//li[@class="tm-ind-item tm-ind-sellCount "]/div[@class="tm-indcon"]/span[@class="tm-count"]/text()')) != 0:
                        self.goto_init()
                        return self.driver.page_source
                    pai_mai = None
                    try:
                        pai_mai = res_get_page.xpath('//span[@class="price"]/text()')[0]
                    except:
                        pass
                    if pai_mai != None:
                        self.goto_init()
                        return self.driver.page_source
                print 'length:',len(self.driver.page_source),'current_url:',self.driver.current_url[:20],'origon_url:',url[:20]
                mutex.acquire()
                print u'重新拨号...'
                aa = Adsl()
                aa.reconnect()
                self.temp += 1
                self.goto_home()
                print 'temp:', self.temp
                mutex.release()
                if self.temp > 4:
                    if self.temp_change < 5 or self.temp%10 == 0:
                        print 'kill a driver'
                        self.driver.quit()
                        self.u_a = self.U_A[randint(0,len(self.U_A)-1)]
                        #self.cap["phantomjs.page.settings.userAgent"] = self.u_a
                        #self.cap["phantomjs.page.customHeaders.User-Agent"] = self.u_a
                        #self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs.exe',service_log_path='C:/ghostdriver.log',desired_capabilities=self.cap)
                        self.chrome_options.add_argument('--user-agent=%s'%self.u_a)
                        self.driver = webdriver.Chrome(executable_path=self.chromedriver,chrome_options=self.chrome_options)
                        self.temp_change += 1
                if self.temp%10 == 0 and self.temp != 0:
                    wait = randint((self.temp/10)*300,(self.temp/10)*600)
                    print 'wait %s s...'%str(wait)
                    print 'kill a driver'
                    self.driver.quit()
                    self.u_a = self.U_A[randint(0,len(self.U_A)-1)]
                    self.chrome_options.add_argument('--user-agent=%s'%self.u_a)
                    time.sleep(wait)
                    self.driver = webdriver.Chrome(executable_path=self.chromedriver,chrome_options=self.chrome_options)
                if self.temp == self.temp_num:
                    print u'尝试%s次均失败，作保存处理...'%(self.temp_num-1)
                    self.driver.quit()
                    self.u_a = self.U_A[randint(0,len(self.U_A)-1)]
                    self.chrome_options.add_argument('--user-agent=%s'%self.u_a)
                    self.goto_init()
                    #self.mode = 0
                    time.sleep(randint(9,15)*60)
                    self.driver = webdriver.Chrome(executable_path=self.chromedriver,chrome_options=self.chrome_options)
            except Exception, e:
                print 'get_page err: ', e
                return False



    def delete(self):
        try:
            #self.driver.quit()
            os.system('taskkill /im chrome.exe /f')
            os.system('taskkill /im chromedriver.exe /f')
        except:
            pass


if __name__ == '__main__':
    d = downloader()
    #urls = ['https://list.tmall.com/search_shopitem.htm?spm=a220m.1000858.1000725.35.2a70033euN3GFX&user_id=3157322542&q=&sort=s&cat=50928001&from=_1_&is=p',
    #        'https://list.tmall.com/search_shopitem.htm?user_id=3157322542&q=&sort=s&cat=50928001&from=_1_&is=p',
    #        'https://list.tmall.com/search_shopitem.htm?user_id=3157322542&sort=s&cat=50928001&from=_1_&is=p']
    urls = ['https://detail.tmall.com/item.htm?id=546249451559&is_b=1&cat_id=50024400&rn=10e35e1a0caa2a012a770744d8d2218b',
            'https://detail.tmall.com/item.htm?id=544548886206&is_b=1&cat_id=50101358&rn=758fba49be8511ed9ff3e807a9b7490f']
            #'https://detail.tmall.com/item.htm?id=546249451559&is_b=1&cat_id=50024400&rn=10e35e1a0caa2a012a770744d8d2218b&sku_properties=10004:385316259;5919063:6536025']
    for url in urls[:]:
        
        res = d.get_page(url,['https://www.tmall.com/'],threading.Lock())
        #print res
        res = lxml.html.document_fromstring(res)
        sales = res.xpath('//span[@class="tm-price"]/text()')
        time.sleep(3)
        print sales
    d.delete()
    time.sleep(10)
