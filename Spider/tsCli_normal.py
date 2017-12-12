# -*- coding: utf-8 -*-
import os, sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import socket
import time
from worker_spider_normal import Worker
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
        # func_name = 'crawler_tmall'
        for each_file in os.listdir(settings.files_dir):
            if each_file == 'task_url.txt':
                try:
                    with codecs.open(os.path.join(settings.files_dir,each_file),'r','utf-8') as f:
                        task_pool = [(x.split('\n')[0].split('&/#')[0],x.split('\n')[0].split('&/#')[1]) for x in f]
                except:
                    pass
            if each_file == 'task_url_old.txt':
                try:
                    with codecs.open(os.path.join(settings.files_dir,each_file),'r','utf-8') as f:
                        task_pool_old = [(x.split('\n')[0].split('&/#')[0],x.split('\n')[0].split('&/#')[1]) for x in f]
                except:
                    pass
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
                for each_task in data['task']['task_list']:
                    task_url = each_task
                    db.update("""update task_list set status = 1 where task_item = '%s'"""%task_url)
                db.close()
                pool_temp = zip(data['task']['func_list'],data['task']['task_list'])
                task_pool.extend(pool_temp)
        print 'task_num', len(task_pool)
        # 清除task_url记录
        for each_file in os.listdir(settings.files_dir):
            if 'task_url' in each_file:
                os.remove(os.path.join(settings.files_dir,each_file))
        if len(task_pool) > 0:
            with codecs.open(os.path.join(settings.files_dir, 'task_url.txt'),'a','utf-8') as f:
                for each_task in task_pool:
                    f.write(each_task[0]+'&/#'+each_task[1]+'\n')
            wk.run(task_pool)
            # feedback = 'got it'
            #print 'Sending "%s".'% 'feedback'
            #sock.sendall(feedback)
            time.sleep(randint(1,3))
        else:
            print 'no more task...'
            time.sleep(10*60)
        # 清除task_url记录
        for each_file in os.listdir(settings.files_dir):
            if 'task_url' in each_file:
                os.remove(os.path.join(settings.files_dir,each_file))
    except Exception, e:
        print 'check_tcp_status err',e


if __name__ == "__main__":
    while True:
        aa = Adsl()
        try:
            aa.connect()
        except:
            pass
        check_tcp_status("ip", port,'ready')
