# -*- coding: utf-8 -*-
import os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import socket
import time
from worker_spider import Worker
import json
from random import randint
from Downloader.adsl import Adsl
import settings
import codecs
from DB.MySQLDB import MySql

def check_tcp_status(ip, port,message):
    try:
        wk = Worker()
        # 汇总task_pool
        task_pool = []
        task_pool_old = []
        func_name = 'crawler_tmall'
        for each_file in os.listdir(settings.files_dir):
            if each_file == 'shop_url.txt':
                with codecs.open(os.path.join(settings.files_dir,each_file),'r','utf-8') as f:
                    task_pool = [x.split('\n')[0] for x in f]
            if each_file == 'shop_url_old.txt':
                with codecs.open(os.path.join(settings.files_dir,each_file),'r','utf-8') as f:
                    task_pool_old = [x.split('\n')[0] for x in f]
        task_pool = list(set(task_pool) ^ set(task_pool_old))
        if len(task_pool) == 0:
            #wk = Worker()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port)
            sock.connect(server_address)
            print 'Connecting to %s:%s.' % server_address
            #while True:
                #message = raw_input('-->')
            if message:
                print 'Sending "%s".' % message
                sock.sendall(message)
            data = sock.recv(102400)
            data = json.loads(data)

            print 'Closing socket.'
            sock.sendall('bye')
            sock.close()

            
            if data['task'] != 'no more':
                # successfully received msg update to db
                db = MySql('ip', 3306, 'root', 'pwd', 'db')
                for each_task in data['task']['detail']:
                    shop_url = each_task.split('&/#')[0]
                    db.update("""update tmall_shop_url_2 set status = 1 where shop_url = '%s'"""%shop_url)
                db.close()
                
                task_pool.extend(data['task']['detail'])
                func_name = data['task']['func_name']
        print 'task_num', len(task_pool)
        # 清除shop_url记录
        for each_file in os.listdir(settings.files_dir):
            if 'shop_url' in each_file:
                os.remove(os.path.join(settings.files_dir,each_file))
        if len(task_pool) > 0:
            with codecs.open(os.path.join(settings.files_dir, 'shop_url.txt'),'a','utf-8') as f:
                for each_task in task_pool:
                    f.write(each_task+'\n')
            wk.run(func_name,task_pool)
            # feedback = 'got it'
            #print 'Sending "%s".'% 'feedback'
            #sock.sendall(feedback)
            time.sleep(randint(1,3))
        else:
            print 'no more task...'
            time.sleep(10*60)
        # 清除shop_url记录
        for each_file in os.listdir(settings.files_dir):
            if 'shop_url' in each_file:
                os.remove(os.path.join(settings.files_dir,each_file))
    except Exception, e:
        print 'check_tcp_status err',e


if __name__ == "__main__":
    # for i in range(2):
    while True:
        #time.sleep(1)
        #while True:
            #msg = raw_input('-->')
        #time.sleep(randint(60,60*2))
        aa = Adsl()
        try:
            aa.connect()
        except:
            pass
        check_tcp_status("ip", port,'ready')
