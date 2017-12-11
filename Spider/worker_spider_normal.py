#coding:utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Mythread.mythread import Thread_distribute
import crawlerCenter_normal
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

    def run(self,task_pool):
        print u'----------parsing page----------'
        try:
            func = None
            func_dic = {}
            # 聚合task中，func和task_item
            for each_task in task_pool:
                if each_task[0] not in func_dic.keys():
                    func_dic[each_task[0]] = [each_task[1]]
                else:
                    func_dic.get(each_task[0]).append(each_task[1])
            # 建立crawler名称和函数的映射关系
            for key in func_dic.keys():
                if key == 'crawler_tmall':
                    func = crawlerCenter_normal.crawler_tmall
                elif key == 'crawler_tmall_shop_ultra':
                    func = crawlerCenter_normal.crawler_tmall_shop_ultra
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
                        t = Thread_distribute(func,func_dic[key],len(func_dic[key]),self.mutex,'thread-%s'%str(i),dl_type='p',temp_num=20)
                        threads.append(t)
                    for i in range(thread_num):
                        threads[i].start()
                    for i in range(thread_num):
                        threads[i].join()
                else:
                    print 'there is no crawler named [%s]'%func
        except Exception, e:
            print 'Worker run err: ', e
        finally:
            print u'task done'
            json_str = json.dumps({'over': self.result_list})
            return json_str
