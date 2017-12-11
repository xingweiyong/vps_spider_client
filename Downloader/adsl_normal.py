#! coding:utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
import settings
import requests
from selenium import webdriver

username = settings.username
password = settings.password


g_adsl_account = {"name": "adsl",
                  "username": username,
                  "password":password}



class Adsl(object):
    #==============================================================================
    # __init__ : name: adsl名称
    #==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]


    #==============================================================================
    # set_adsl : 修改adsl设置
    #==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]


    #==============================================================================
    # connect : 宽带拨号
    #==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(15)


    #==============================================================================
    # disconnect : 断开宽带连接
    #==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(3)


    #==============================================================================
    # reconnect : 重新进行拨号
    #==============================================================================
    def reconnect(self):
        try:
            self.disconnect()
            self.connect()
        except Exception,e:
            print 'reconnect err ',str(e)

            

if __name__ == "__main__":
    aa = Adsl()
    aa.reconnect()


