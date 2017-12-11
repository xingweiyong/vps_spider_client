#coding:utf-8
# 封装的多线程类
import threading
import inspect
import ctypes
from Downloader.Downloader_phatomjs import downloader as downloader_p
from Downloader.Downloader_requets import downloader as downloader_r
from Downloader.Downloader_phatomjs_normal import downloader as downloader_p_n
import time
from random import randint

# 线程级别初始化downloader
class Thread(threading.Thread):
    def __init__(self,func,arg1,arg2,name='my_thread',start_url='',dl_type='r',temp_num=None):
        time.sleep(randint(1,10)*0.1)
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.func = func
        self.list = arg1
        self.task_num = arg2
        self.name = name
        self.temp_num = temp_num
        if dl_type == 'r':
            self.dl = downloader_r(start_url)
        elif dl_type == 'p':
            self.dl = downloader_p(start_url,temp_num)
        elif dl_type == 'n':
            self.dl = downloader_p_n(start_url,temp_num)

    def run(self):
        while isinstance(self.list,list) and len(self.list) > 0:
            # print self.isAlive()
            if self.isAlive():
                print self.name
                #apply(self.func,self.list)
                self.func(self.list,self.task_num,self.dl)
            else:
                # self.stop_thread(self)
                break
        try:
            self.dl.delete()
        except Exception,e:
            print 'dl delete err: ',e

# 函数级别初始化downloader
class Thread_url(threading.Thread):
    def __init__(self,func,arg1,arg2,name='my_thread',start_url='',dl_type='r',temp_num=None):
        time.sleep(randint(1,10)*0.1)
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.func = func
        self.list = arg1
        self.task_num = arg2
        self.name = name
        self.dl_type = dl_type
        self.start_url = start_url
        self.temp_num = temp_num
    def run(self):
        while isinstance(self.list,list) and len(self.list) > 0:
            if self.dl_type == 'r':
                self.dl = downloader_r(self.start_url)
            elif self.dl_type == 'p':
                self.dl = downloader_p(self.start_url,self.temp_num)
            print self.name
            self.func(self.list,self.task_num,self.dl)
            try:
                self.dl.delete()
            except Exception,e:
                print 'dl delete err: ',e

# 线程结束需要返回结果的情况
class Thread_distribute(threading.Thread):
    def __init__(self,func,arg1,arg2,mutex,name='my_thread',start_url='',dl_type='r',temp_num=None):
        time.sleep(randint(1,10)*0.1)
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.func = func
        self.list = arg1
        self.task_num = arg2
        self.mutex = mutex
        #self.result_list = result_list
        self.name = name
        if dl_type == 'r':
            self.dl = downloader_r(start_url)
        elif dl_type == 'p':
            self.dl = downloader_p(start_url,temp_num)

    def run(self):
        while isinstance(self.list,list) and len(self.list) > 0:
            # print self.isAlive()
            if self.isAlive():
                print self.name
                #apply(self.func,self.list)
                self.func(self.list,self.task_num,self.dl,self.mutex)
            else:
                # self.stop_thread(self)
                break
        try:
            self.dl.delete()
        except:
            pass
