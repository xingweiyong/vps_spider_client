# coding:utf-8

import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
from Util.adsl import Adsl
import re
import lxml.html
from random import randint
import codecs
from Downloader.Downloader_phatomjs import downloader
from Resource.cat_dic import cat_dic
from Resource.catIds import cat_ids
from Mythread.mythread import Thread
from Mythread.mythread import Thread_url
import threading
import settings
from DB.MySQLDB import MySql

# ---定义初始信息---
# 爬去批次
flag = settings.flag
# ---定义cat_id列表---
cat_ids = cat_ids
# 根目录
root = settings.root
# port
port = settings.port
# 文件目录
files_dir = settings.files_dir
if not os.path.exists(files_dir):
    os.mkdir(files_dir)

# current dir
# local
#spider_name = __file__.split('/')[-1][:-3]
#project_dir = os.path.join(files_dir,spider_name)

# vps
spider_name = __file__.split('\\')[-1][:-3]
project_dir = files_dir + '\\' + spider_name


if not os.path.exists(project_dir):
    os.mkdir(project_dir)
current_dir = os.path.join(project_dir, flag)
if not os.path.exists(current_dir):
    os.mkdir(current_dir)


def get_data(list_temp, index):
    if list_temp != None and len(list_temp) > index:
        return list_temp[index]
    else:
        return 'None'


def write2file(file_name, dic):
    tmp = ''
    for index, value in enumerate(dic.keys()):
        if index != len(dic.keys()) - 1:
            tmp += (dic[value].decode() if isinstance(dic[value], str) else dic[value]).replace('\n', '') + '&/#'
        else:
            tmp += dic[value].replace('\n', '') + '\n'
    try:
        with codecs.open(os.path.join(current_dir, file_name), 'a', 'utf-8') as f:  # /mnt/scrapyPlat/saveFiles/
            f.write(tmp)
    except:
        pass


def worker(final_url, total_num, dl):
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        mutex.acquire()
        try:
            url = final_url.pop(0)
        except:
            pass
        mutex.release()
        ontime_num = len(final_url)
        print u'[%s],parse,processing: %s in %s' % (str(current_time), str(total_num - ontime_num), str(total_num))
        counter = 0
        while True:
            # dl = downloader()
            html = dl.get_page(url,[],mutex,['login'],min_len=40)
            if html:
                item = {}
                res = lxml.html.document_fromstring(html)
                item['stk'] = get_data(re.findall(re.compile('\?p=(.*)'),url),0)
                item['currentQtr']= get_data(res.xpath('//td[@data-reactid="128"]/span/text()'),0)
                item['nextQtr'] = get_data(res.xpath('//td[@data-reactid="130"]/span/text()'),0)
                item['currentYear'] = get_data(res.xpath('//td[@data-reactid="132"]/span/text()'),0)
                item['nextYear'] = get_data(res.xpath('//td[@data-reactid="134"]/span/text()'),0)
                item['current_date'] = current_date
                #print item['stk'],item['currentQtr'],item['current_date']
                mutex.acquire()
                try:
                    db = MySql('36.110.128.75', 3306, 'root', 'Bigdata1234', 'crawler_db')
                    db.insert_single('''INSERT INTO finance_yahoo(stk,currentQtr,nextQtr,currentYear,nextYear,currentDate)VALUES ('%s','%s','%s','%s','%s','%s')'''%(
                        item['stk'],item['currentQtr'],item['nextQtr'],item['currentYear'],item['nextYear'],item['current_date']))
                    db.close()
                except Exception,e:
                    print 'save to db error...',e
                finally:
                    write2file('yahoo_finance.txt',item)
                mutex.release()
                break

            else:
                counter += 1
                if counter > 3:
                    print u'worker failure more than 3,break...'
                    break
    except Exception, e:
        print 'worker error: ', e

def run(thread_num):
    # 启动程序
    print u'----------启动程序----------'
    print u'----------启动 %s 个线程解析----------' % str(thread_num)
    task_code = ['AOS','IRBT','LOGI','MJN','STX','AAPL','WDC','HPQ','CAJ','KMB','COH','GPRO','HAR','GRMN',
                 'LPL','MSI','RDEN','NKE','GNC','ABT','COLM','EL','KORS','FIT','INTC','XRX','DECK','AMD',
                 'TUP','BBRY','HLF','GT','NOK','SNE']
    final_urls = ['https://finance.yahoo.com/quote/%s/analysts?p=%s'%(x,x) for x in task_code]
    print 'final length ', len(final_urls)
    if len(final_urls) > 0:
        total_num = len(final_urls)
        threads = []
        global mutex
        mutex = threading.Lock()

        for i in range(thread_num):
            t = Thread(worker, final_urls, total_num, start_url='',name='thread_id: %s'%str(i), dl_type='n') # https://finance.yahoo.com
            threads.append(t)
        #for i in range(thread_num):
        #    threads[i].start()
            time.sleep(randint(0,10)*0.1)
            t.start()
        for i in range(thread_num):
            threads[i].join()
    else:
        print u'列表页全部解析完成...'


try:
    global mutex,shop_cat_set
    shop_cat_set = set()
    mutex = threading.Lock()
    thread_num = 1
    run(thread_num)
except KeyboardInterrupt:
    print 'ctrl+c terminated...'
except Exception, e:
    print 'err: ', e
finally:
    print u'all done'


