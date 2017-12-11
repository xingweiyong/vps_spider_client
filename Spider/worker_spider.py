#coding:utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Mythread.mythread import Thread_distribute
import crawlerCenter
import threading
import time
#from DB.MySQLDB import MySql
import json


#-----工作单元-----
class Worker(object):
    def __init__(self):
        # ---定义初始信息---
        # 爬去批次
        self.flag = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        self.result_list = []
        self.mutex = threading.Lock()

    def run(self,func_name,task):
        print u'----------parsing page----------'
        try:
            # 建立crawler名称和函数的映射关系
            func = None
            if func_name == 'crawler_tmall':
                func = crawlerCenter.crawler_tmall
            if func:
                threads = []
                thread_num = 1
                # global dl
                # dl = ''
                # global result_list
                # result_list = []
                # global mutex
                # mutex = threading.Lock()
                # total_num = len(task_l)
                for i in range(thread_num):
                    t = Thread_distribute(func,task,len(task),self.mutex,'thread-%s'%str(i),dl_type='p',temp_num=20)
                    threads.append(t)
                for i in range(thread_num):
                    threads[i].start()
                for i in range(thread_num):
                    threads[i].join()
            else:
                print 'there is no crawler named [%s]'%func_name
        except Exception, e:
            print 'Worker run err: ', e
        finally:
            print u'task done'
            json_str = json.dumps({'over': self.result_list})
            return json_str
