#coding:utf-8
import re

class Filter():
    def __init__(self,str_temp):
        self.str = str_temp

    @classmethod
    def remove(self,str):
        str = str.replace(' ','')
        str = str.replace('\n', '')
        return str

    @classmethod
    def filter_emoji(self,desstr, restr=''):
        '''''
        过滤表情
        '''
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        try:
            return co.sub(restr, desstr)
        except:
            return desstr
    @classmethod
    def replace(self,str,oriStr,desStr):
        return str.replace(oriStr,desStr)

    @classmethod
    def get_data(self,list,index):
        if list != None and len(list) > index and len(list)!=0:
            return list[index]
        else:
            return 'None'
    @classmethod
    def combine_data(self,list):
        if list!=None:
            temp = ''
            for each_value in list:
                temp += each_value + ' '
            return temp
        else:
            return 'None'

if __name__ == '__main__':
    fl = Filter('   \n 12324')
    #print fl.remove()
    str = u'.龙啸(依赖）分'
    f2 = Filter(str)
    str1 = f2.filter_emoji(str)
    print str1
    #print f2.filter_emoji(str1)
    f3 = Filter(u'329在看')
    #res = f3.replace(u'329在看',u'在看','')
