#coding:utf-8
import pymongo

pymongo.ASCENDING = 1
pymongo.DESCENDING = -1
class mongo_djl():
    def __init__(self,host='localhost',port=27017):
        self.con=pymongo.MongoClient(host,port)

    def insert(self,dbname,table_name,item):
        try:
            db = self.con[dbname]
            table=db[table_name]
            table.insert(item)
            return True
        except Exception,e:
            print 'insert error： ',e
            return False

    def find(self,dbname,table_name,sql):
        db = self.con[dbname]
        table=db[table_name]
        return  table.find(sql)

    def update(self,dbname,table_name,sql,a):
        db = self.con[dbname]
        table=db[table_name]
        table.update(sql,a,multi=True)

    def find_one(self,dbname,table_name,sql):
        db = self.con[dbname]
        table=db[table_name]
        return table.find_one(sql)
    def delete(self):
        self.con.close()