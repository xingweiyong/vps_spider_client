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


def split_price(cat_ids):
    total_num_rule = u'共.*?(\d+).*?个店铺'
    res = ''
    total_num = ''
    time.sleep(0.6)
    res = dl.get_page(base_url % (cat_ids),[],mutex)
    if res:
        res_xpath = lxml.html.document_fromstring(res)
        blocks = res_xpath.xpath('//div[@id="J_SuggestTipWrap"]/div')
        if len(blocks) == 0:
            total_num = get_data(re.findall(re.compile(total_num_rule), res), 0)
            if total_num and total_num != 'None':  # isinstance(int(total_num),int)
                # if block
                if int(total_num) > 500:  # 店铺一页20共100页
                    if round(abs(cat_ids[2] - cat_ids[1]), 2) <= 0.01:
                        print u'精度达到0.01...', cat_ids
                        split_cat_ids.append(cat_ids)
                    else:
                        mid = round((cat_ids[2] - cat_ids[1]) / 2 + cat_ids[1], 2)
                        print 'cat_id:%s,total_num:%s,left:%s,mid:%s,right:%s' % (
                            cat_ids[0], total_num, cat_ids[1], mid, cat_ids[2])
                        split_price((cat_ids[0], cat_ids[1], mid))
                        split_price((cat_ids[0], round(float(mid + 0.01), 2), cat_ids[2]))
                else:
                    if int(total_num) > 0:
                        print u'小于阈值的价格区间: ', cat_ids
                        split_cat_ids.append(cat_ids)
            else:
                print u'获取最大店铺数失败%s，try again...' % str(cat_ids)
                # err_log += 'err_type:获取最大商品数失败' + '\n'
                aa = Adsl()
                aa.reconnect()
                time.sleep(2)
                split_price((cat_ids[0], cat_ids[1], cat_ids[2]))
        else:
            print 'sure,get no blocks...'
    else:
        print u'split_price,未下载到网页，try again...'
        split_price((cat_ids[0], cat_ids[1], cat_ids[2]))


def get_max_page(cat_ids):
    max_page_rule = u'共(\d+)页，到第'
    res = dl.get_page(base_url % (cat_ids),[],mutex)
    counter = 0
    while True:
        if res:
            max_page = get_data(re.findall(re.compile(max_page_rule), res), 0)
            return max_page
        else:
            counter += 1
            if counter > 3:
                print u'get_max_page err,未下载到网页...'
                return False


def run_split_price():
    # 分隔价格区间
    print u'----------分隔价格区间----------'
    for item in cat_ids:
        split_price(item)
        # print len(split_cat_ids)


def get_total_num(cat_ids):
    total_num_rule = u'共.*?(\d+).*?件相关商品'
    counter = 0
    while True:
        time.sleep(randint(0, 1))
        res = dl.get_page(base_url % (cat_ids),[],mutex)
        counter += 1
        if res:
            total_num = get_data(re.findall(re.compile(total_num_rule), res), 0)
            if total_num and total_num != 'None':
                return int(total_num)
            else:
                print u'get_total_num 获得最大商品数失败...'
                return False
        else:
            if counter > 3:
                print u'get_total_numm 网页下载失败...'
                return False


def run_get_max_page():
    # 翻页
    print u'----------获取翻页----------'
    total_num = len(split_cat_ids)
    for i, item in enumerate(split_cat_ids):
        print u'page,processing: %s in %s' % (str(i + 1), str(total_num))
        time.sleep(randint(0, 8) * 0.1)
        loop_counter = 0
        while True:
            loop_counter += 1
            max_page = get_max_page(item)
            if max_page and max_page != 'None':
                for i in range(1, int(max_page) + 1):
                    final_url.append(base_url % (item) + '&type=pc&totalPage=%s&jumpto=%s' % (max_page, str(i)))
                break
            else:
                if get_total_num(item) > 0:
                    print u'max_page loop: ', loop_counter
                    if loop_counter > 20:
                        print u'max_page loop 超过20，item: ', item
                        break
                    continue
                else:
                    print u'max_page loop 商品数为0...'
                    break
    for url in final_url:
        with codecs.open(os.path.join(current_dir, 'final_url.txt'), 'a') as f:
            f.write(url + '\n')


def worker_shop(final_url, total_num, dl):
    # 解析店铺url more products
    global shop_cat_set
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
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
            res_0 = dl.get_page(url,[],mutex)
            if res_0:
                res = lxml.html.document_fromstring(res_0)
            else:
                res = res_0
            # dl.delete()
            if res:
                shop_blocks = res.xpath('//div[@class="shopHeader-info"]')
                base_url_more = 'https://list.tmall.com/search_shopitem.htm?user_id=%s&q=&sort=s&cat=%s&from=_1_&is=p'
                if len(shop_blocks) > 0:
                    for shop_block in shop_blocks:
                        shop_url = get_data(shop_block.xpath('./a/@href'),0)
                        shop_brand = get_data(shop_block.xpath('./p/span/text()'),0)
                        user_id = get_data(re.findall(re.compile('\?user_id=(\d+)&'), shop_url), 0)
                        #base_url_more = 'https://list.tmall.com/search_shopitem.htm?%s&q=&sort=s&%s&%s'
                        cat_id = get_data(re.findall(re.compile('cat=(\d+)'), url), 0)
                        #para2 = get_data(re.findall(re.compile('(start_price=\d+&end_price=\d+)'), url), 0)
                        #url_more = base_url_more % (shop_id, para1, para2)
                        if (user_id,cat_id) not in shop_cat_set:
                            url_more = base_url_more%(user_id,cat_id)
                            shop_cat_set.add((user_id,cat_id))
                            mutex.acquire()
                            with codecs.open(os.path.join(current_dir, 'shop_url.txt'), 'a', 'utf-8') as f:
                                f.write(url_more+'&/#'+ shop_brand + '\n')
                            mutex.release()
                else:
                    print u'no list item'
                mutex.acquire()
                with codecs.open(os.path.join(current_dir, 'final_url_old.txt'), 'a', 'utf-8') as f:
                    f.write(url + '\n')
                mutex.release()
                break

            else:
                counter += 1
                if counter > 3:
                    print u'work_shop failure more than 3,break...'
                    break
    except Exception, e:
        print 'worker_shop error: ', e


def worker_product(final_url, total_num, dl):
    # 解析product url
    shop_brand = ''
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
            shop_name = 'None'
        ontime_num = len(final_url)
        print u'[%s],parse,processing: %s in %s' % (str(current_time), str(total_num - ontime_num), str(total_num))
        counter = 0
        while True:
            # dl = downloader()
            base_url = 'https://www.tmall.com/'
            url_pre = 'https://list.tmall.com/search_product.htm?' + re.findall('(cat.*)',url)[0] + '&style=g'
            url_bef = 'https://list.tmall.com/search_product.htm?' + re.findall('(cat.*)',url)[0] + '&style=w'
            res_0 = dl.get_page(url,[],mutex)
            time.sleep(randint(0, 50) * 0.1)
            # dl.delete()
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
                                mutex.acquire()
                                with codecs.open(os.path.join(current_dir, 'product_url.txt'), 'a', 'utf-8') as f:
                                    f.write('https:'+ each_product_url +'\n')
                                mutex.release()
                                # parse detail
                                time.sleep(randint(20,50)*0.1)
                                worker_parse_detail('https:'+ each_product_url,shop_brand,dl)
                                
                        else:
                            print u'该页没有product列表',final_url_product
                else:
                    print u'no list item'

                mutex.acquire()
                with codecs.open(os.path.join(current_dir, 'shop_url_old.txt'), 'a', 'utf-8') as f:
                    f.write(url+'&/#'+ shop_brand.decode('utf-8') + '\n')
                mutex.release()

                break
            else:
                counter += 1
                if counter > 3:
                    print u'worker_product failure more than 3,break... '
                    break
    except Exception, e:
        print 'worker_product error: ', e


def worker_parse_detail(url,brand,dl):
    try:
        #print chardet.detect(brand)
        crawl_time_stamp = str(time.time())
        '''
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mutex.acquire()
        try:
            url = re.sub(re.compile('&skuId=\d+'),'',final_url.pop(0))
        except:
            pass
        mutex.release()
        ontime_num = len(final_url)
        print u'[%s],parse,processing: %s in %s' % (str(current_time), str(total_num - ontime_num), str(total_num))
        # dl = downloader()
        '''
        res = dl.get_page(url,[],mutex)
        # dl.delete()
        if res:
            item = {}
            res = lxml.html.document_fromstring(res)
            item['cat_id'] = get_data(re.findall(re.compile('cat_id=(\d+)&'), url), 0)
            item['cat_name'] = catDic[item['cat_id']]
            item['product_id'] = get_data(re.findall(re.compile('[\?|&]id=(\d+)&'), url), 0)
            item['sku_id'] = get_data(re.findall(re.compile('skuId=(\d+)&'), url), 0)
            item['price'] = get_data(res.xpath('//span[@class="tm-price"]/text()'),-1)
            item['sales'] = get_data(res.xpath('//li[@class="tm-ind-item tm-ind-sellCount "]/div[@class="tm-indcon"]/span[@class="tm-count"]/text()'),0)
            #item['brand'] = get_data(res.xpath('//div[@id="J_BrandAttr"]/div[@class="name"]/a/text()'),0).strip()
            item['brand'] = brand.decode('utf-8')
            item['title'] = get_data(res.xpath('//h1[@data-spm="1000983"]/a/text()'), 0).strip()
            if item['title'] == 'None':
                item['title'] = get_data(res.xpath('//h1[@data-spm="1000983"]/text()'), 0).strip()
            item['flag'] = flag
            item['crawl_time_stamp'] = crawl_time_stamp
            item['shop_name'] = get_data(res.xpath('//a[@class="slogo-shopname"]/strong/text()'), 0)
            item['price_range'] = 'None'
            mutex.acquire()
            write2file(os.path.join(current_dir,port+'_'+'tmall_product_info.txt'),item)
            mutex.release()

        mutex.acquire()
        with codecs.open(os.path.join(current_dir, 'product_url_old.txt'), 'a', 'utf-8') as f:
            f.write(url + '\n')
        mutex.release()
    except Exception, e:
        print 'worker_parse_detail error: ', e


def run_parse_html(thread_num):
    # 解析网页
    print u'----------解析列表页----------'
    with open(os.path.join(current_dir, 'final_url.txt'), 'r') as f:
        final_urls = [x.split('\n')[0] for x in f]
    print 'final length ', len(final_urls)
    # 扫描本地文件
    # path = os.path.split(os.path.realpath(__file__))[0]
    files = os.listdir(current_dir)
    if 'final_url_old.txt' in files:
        print 'final_url_old exists...'
        with codecs.open(os.path.join(current_dir, 'final_url_old.txt'), 'r') as f:
            url_old = [x.split('\n')[0] for x in f]
        print 'url_old length ', len(url_old)
        final_urls = list(set(final_urls) ^ set(url_old))
    print 'final length after ', len(final_urls)
    '''
    #记录解析批次
    flag = 0
    while len(final_urls) > 0:
        flag += 1
        final_url = []
        print u'-----------第 %s 个500 task----------' %str(flag)
        if len(final_urls) >= 500:
            for i in range(500):
                final_url.append(final_urls.pop(0))
        else:
            final_url = final_urls
    '''
    if len(final_urls) > 0:
        total_num = len(final_urls)
        threads = []
        global mutex
        mutex = threading.Lock()

        for i in range(thread_num):
            t = Thread(worker_shop, final_urls, total_num, start_url='https://www.tmall.com/',name='thread_id: %s'%str(i), dl_type='p')
            threads.append(t)
        #for i in range(thread_num):
        #    threads[i].start()
            time.sleep(randint(0,10)*0.1)
            t.start()
        for i in range(thread_num):
            threads[i].join()
    else:
        print u'列表页全部解析完成...'


def run_parse_shop(thread_num):
    # 解析网页
    print u'----------解析shop页----------'
    with open(os.path.join(current_dir, 'shop_url.txt'), 'r') as f:
        final_urls = [x.split('\n')[0] for x in f]
    print 'final shop_url length ', len(final_urls)
    # 扫描本地文件
    # path = os.path.split(os.path.realpath(__file__))[0]
    files = os.listdir(current_dir)
    if 'shop_url_old.txt' in files:
        print 'shop_url_old exists...'
        with codecs.open(os.path.join(current_dir, 'shop_url_old.txt'), 'r') as f:
            url_old = [x.split('\n')[0] for x in f]
        print 'shop_url_old length ', len(url_old)
        final_urls = list(set(final_urls) ^ set(url_old))
    print 'final shop_url length after ', len(final_urls)

    if len(final_urls) > 0:
        total_num = len(final_urls)
        threads = []
        global mutex
        mutex = threading.Lock()

        for i in range(1):
            t = Thread(worker_product, final_urls, total_num,name='thread_id: %s'%str(i), dl_type='p',temp_num=6) # , start_url='https://www.tmall.com/'
            threads.append(t)
        #for i in range(thread_num):
        #    threads[i].start()
            time.sleep(randint(0,10)*0.1)
            t.start()
        for i in range(thread_num):
            threads[i].join()
    else:
        print u'shop页全部解析完成...'


def run_parse_detail(thread_num):
    print u'----------解析详情页----------'
    # path = os.path.split(os.path.realpath(__file__))[0]
    files = os.listdir(current_dir)
    if 'product_url.txt' in files:
        print 'product_url exists...'
        with codecs.open(os.path.join(current_dir, 'product_url.txt'), 'r', 'utf-8') as f:
            final_product_urls = [x.split('\n')[0] for x in f]
            print 'final_product_urls length:', len(final_product_urls)
        if 'product_url_old.txt' in files:
            print 'product_url_old exists...'
            with codecs.open(os.path.join(current_dir, 'product_url_old.txt'), 'r', 'utf-8') as f:
                final_product_old = [x.split('\n')[0] for x in f]
            final_product_urls = list(set(final_product_urls) ^ set(final_product_old))
            print 'diff final_product_urls length: ', len(final_product_urls)
        total_num = len(final_product_urls)
        threads = []
        global mutex
        mutex = threading.Lock()

        for i in range(thread_num):
            t = Thread(worker_parse_detail, final_product_urls, total_num, start_url='https://www.tmall.com/',
                       name='thread_id: %s'%str(i),dl_type='p')
            threads.append(t)
        #for i in range(thread_num):
        #    threads[i].start()
            time.sleep(randint(0,10)*0.1)
            t.start()
        for i in range(thread_num):
            threads[i].join()
    else:
        print 'there is no product_url yet...'


def run(thread_num):
    # 启动程序
    print u'----------启动程序----------'
    print u'----------启动 %s 个线程解析----------' % str(thread_num)
    # 扫描本地文件
    # path = os.path.split(os.path.realpath(__file__))[0]
    # print current_dir
    files = os.listdir(current_dir)
    # print files
    if 'final_url.txt' in files:
        print '=====final_url exists====='
        dl.delete()
        run_parse_html(thread_num)
        #run_parse_shop(thread_num)
        #run_parse_detail(thread_num)
    else:
        print '=====from begining====='
        run_split_price()
        run_get_max_page()
        dl.delete()
        run_parse_html(thread_num)
        #run_parse_shop(thread_num)
        #run_parse_detail(thread_num)


try:
    global mutex,shop_cat_set
    shop_cat_set = set()
    mutex = threading.Lock()
    dl = downloader(base_url='https://www.tmall.com/')
    thread_num = 1
    run(thread_num)
except Exception, e:
    print 'err: ', e
finally:
    print u'all done'


