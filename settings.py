# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 15:08:39 2016

@author: zhangmingjin
"""

import time
import os

# adsl usr & pwd
username = '05549709609'
password = '425112'

#---定义初始信息---
base_url = 'https://list.tmall.com/search_product.htm?cat=%s&sort=d&style=l&start_price=%s&end_price=%s' #&sort=d &style=l/g

#---定义容器---
#记录下载失败的url
download_failed = []

#记录二分出来的url
split_cat_ids = []
#记录最终的url

final_url = []
#异常记录

err_log = ''

#linesep
linesep = '\n'#os.linesep

#爬去批次
flag = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))

#定义根目录
root = os.path.split(os.path.realpath(__file__))[0]

#定义文件存储路径
files_dir = os.path.join(root ,'Files')

#define port 
port = '20041'
