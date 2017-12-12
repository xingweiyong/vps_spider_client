#coding:utf-8


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
import json
from HTMLParser import HTMLParser

# ---定义初始信息---
base_url = 'https://list.tmall.com/search_product.htm?cat=%s&sort=s&style=w&start_price=%s&end_price=%s'
# ---定义容器---
# 记录下载失败的url
download_failed = settings.download_failed
# 记录二分出来的url
split_cat_ids = settings.split_cat_ids
# 记录最终的url
final_url = settings.final_url
# 异常记录
err_log = settings.err_log
# linesep
linesep = settings.linesep
# cat_id和名称对应关系
catDic = cat_dic
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
global time_start,time_scope
time_start = time.time()
time_scope = 120

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

#tmall_crawler

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


def worker_parse_detail(url,dl,mutex):
    try:
        #print chardet.detect(brand)
        crawl_time_stamp = str(time.time())
        html = dl.get_page(url,[],mutex)
        res = html
        # dl.delete()
        if res:
            item = {}
            res = lxml.html.document_fromstring(res)
            try:
                item['cat_id'] = get_data(re.findall(re.compile('cat_id=(\d+)&'), url), 0)
            except:
                item['cat_id'] = 'none'
            try:
                item['cat_name'] = catDic[item['cat_id']]
            except:
                item['cat_name'] = 'none'
            try:
                item['product_id'] = get_data(re.findall(re.compile('[\?|&]id=(\d+)&'), url), 0)
            except:
                item['product_id'] = 'none'
            try:
                item['sku_id'] = get_data(re.findall(re.compile('skuId=(\d+)&'), url), 0)
            except:
                item['sku_id'] = 'none'
            try:
                item['price'] = get_data(res.xpath('//span[@class="tm-price"]/text()'),-1)
            except:
                item['price'] = 'none'
            try:
                item['sales'] = get_data(res.xpath('//li[@class="tm-ind-item tm-ind-sellCount"]/div[@class="tm-indcon"]/span[@class="tm-count"]/text()'),0)
            except:
                item['sales'] = 'none'
            try:
                lines = html.split('\n')
                for index,each_line in enumerate(lines):
                    if 'TShop.Setup' in each_line:
                        brand_str = lines[index+1]
                        break;
                brand_dic = json.loads(brand_str)
                item['brand'] = brand_dic['itemDO']['brand']
                item['brand'] = HTMLParser().unescape(item['brand'].replace('amp;',''))
            except Exception,e:
                print 'parse brand err: ',e
                item['brand'] = 'none'
            #print item['brand']
            #try:
            #    item['brand'] = brand
            #except:
            #    item['brand'] = 'none'
            #print brand
            try:
                item['title'] = get_data(res.xpath('//h1[@data-spm="1000983"]/a/text()'), 0).strip()
            except:
                item['title'] = 'none'
            if item['title'] == 'None':
                item['title'] = get_data(res.xpath('//h1[@data-spm="1000983"]/text()'), 0).strip()
            #try:
            #    with codecs.open(os.path.join(current_dir, 'code_temp.txt'), 'wb', 'utf-8') as f:
            #        f.write(item['title'])
            #except:
            #    with open(os.path.join(current_dir, 'code_temp.txt'), 'wb',) as f:
            #        f.write(item['title'])
            #with codecs.open(os.path.join(current_dir, 'code_temp.txt'), 'r', 'utf-8') as f:
            #    item['title'] = [x for x in f][0].replace('\'','')
            item['title'] = item['title'].replace('\'','')

            item['flag'] = flag
            item['crawl_time_stamp'] = crawl_time_stamp
            try:
                item['shop_name'] = get_data(res.xpath('//a[@class="slogo-shopname"]/strong/text()'), 0)
            except:
                item['shop_name'] = 'none'

            item['price_range'] = 'None'
            item['worker_num'] = port

            mutex.acquire()
            try:
                db = MySql('ip', 3306, 'root', 'pwd', 'db')
                db.insert_single('''INSERT INTO tmall_product(sku_id,product_id,cat_name,title,price,crawl_time,brand,sales,shop_name,flag,price_range,cat_id,worker_num)VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''%(
                    item['sku_id'],item['product_id'],item['cat_name'],item['title'],item['price'],item['crawl_time_stamp'],item['brand'],item['sales'],item['shop_name'],item['flag'],item['price_range'],item['cat_id'],item['worker_num']))
                db.close()
            except Exception,e:
                print 'save to db error: ',str(e)
            finally:
                write2file(os.path.join(current_dir,port+'_'+flag+'_'+'tmall_product_info.txt'),item)
            mutex.release()

        mutex.acquire()
        with codecs.open(os.path.join(current_dir, 'product_url_old.txt'), 'a', 'utf-8') as f:
            f.write(url + '\n')
        mutex.release()
    except Exception, e:
        print 'worker_parse_detail error: ', e
    finally:
        if len(res.xpath('//span[@class="tm-price"]/text()')) == 0 and '&q=' in url:
            return False
        elif len(res.xpath('//span[@class="tm-price"]/text()')) == 0 and '&q=' not in url:
            return True
        return None


    
def crawler_tmall(final_url, total_num, dl,mutex):
    # 解析product url
    shop_brand = ''
    is_q = True
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mutex.acquire()
        pre_url = final_url.pop(0)
        mutex.release()
        try:
            url = pre_url.split('&/#')[0]
            shop_brand =  pre_url.split('&/#')[1]
        except:
            url = pre_url
            shop_brand = 'None'
        ontime_num = len(final_url)
        print u'[%s],parse,processing: %s in %s' % (str(current_time), str(total_num - ontime_num), str(total_num))
        global time_start,time_scope
        time_delta = time.time() - time_start
        if time_delta < time_scope and (total_num - ontime_num) != 1:
            print u'time_delta left %d s'%(time_scope - time_delta)
            time.sleep(time_scope - time_delta)
        counter = 0
        while True:
            # dl = downloader()
            base_url = 'https://www.tmall.com/'
            url_pre = 'https://list.tmall.com/search_product.htm?' + re.findall('(cat.*)',url)[0] + '&style=g'
            url_bef = 'https://list.tmall.com/search_product.htm?' + re.findall('(cat.*)',url)[0] + '&style=w'
            time.sleep(randint(5, 20))
            res_0 = dl.get_page(url.replace('&q=',''),[],mutex)
            # dl.delete()
            time_start = time.time()
            if res_0:
                #print len(res_0)
                res = lxml.html.document_fromstring(res_0)
                total_num_rule = '//p[@class="crumbTitle"]/span/text()'
                max_page_rule = u'共(\d+)页'
                product_num = get_data(res.xpath(total_num_rule), 0)
                max_page = get_data(re.findall(re.compile(max_page_rule), res_0), 0)
                #print product_num, max_page
                if product_num != 'None' and max_page != 'None':
                    for each_page in range(1, int(max_page) + 1):
                        blocks_rule = '//div[@class="productImg-wrap"]/a/@href'
                        final_url_product = url + '&totalPage=%d&jumpto=%d' % (int(max_page), each_page)
                        # print 'final_url', final_url
                        res_1 = lxml.html.document_fromstring(dl.get_page(final_url_product,[],mutex))
                        product_urls = res_1.xpath('//div[@class="productImg-wrap"]/a/@href')
                        if len(product_urls) > 0:
                            for each_product_url in product_urls:
                                if 'areaId' not in each_product_url:
                                    each_product_url = each_product_url + '&areaId=120100'
                                mutex.acquire()
                                with codecs.open(os.path.join(current_dir, 'product_url.txt'), 'a', 'utf-8') as f:
                                    f.write('https:'+ each_product_url +'\n')
                                mutex.release()
                        else:
                            print u'该页没有product列表',final_url_product
                    mutex.acquire()
                    try:
                        with codecs.open(os.path.join(files_dir, 'shop_url_old.txt'), 'a', 'utf-8') as f:
                            f.write(url + '&/#' + shop_brand + '\n')
                    except:
                        pass
                    mutex.release()
                else:
                    print u'no list item worker_product'

                break
            else:
                counter += 1
                if counter > 3:
                    print u'worker_product failure more than 3,break... '
                    break
        # parse detail
        task_pool = []
        task_pool_old = []
        for each_file in os.listdir(current_dir):
            if each_file == 'product_url.txt':
                with codecs.open(os.path.join(current_dir,each_file),'r','utf-8') as f:
                    task_pool = [x.split('\n')[0] for x in f]
            if each_file == 'product_url_old.txt':
                with codecs.open(os.path.join(current_dir,each_file),'r','utf-8') as f:
                    task_pool_old = [x.split('\n')[0] for x in f]
        task_pool = list(set(task_pool) ^ set(task_pool_old))

        # time.sleep(randint(5,15)*0.1)
        if len(task_pool) > 0:
            #dl.delete()
            #dl = downloader(bt=1)
            for each_url in task_pool:
                worker_parse_detail(each_url, dl,mutex)
        else:
            print 'task_pool is empty!'

        # successfully received msg update to db
        db = MySql('ip', 3306, 'root', 'pwd', 'db')
        shop_url = url
        db.update("""update tmall_shop_url2 set status = 2 where shop_url = '%s'"""%shop_url)
        db.close()
    except Exception, e:
        print 'worker_product error: ', e

