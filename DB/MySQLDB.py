#coding:utf-8
import MySQLdb
class MySql():
    def __init__(self,host,port,user,password,db):
        self.conn = MySQLdb.connect(host=host,port=port,user=user,passwd=password,db=db,charset="utf8")
        self.cursor = self.conn.cursor()
    def insert(self,dic):
        try:
            self.cursor.execute("""INSERT INTO yy(title,
            num, data_period,cat_url,cat_name,plat,room_id,room_url)
         VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s')"""%(dic['title'],dic['num'],dic['crawl_time'],dic['cat_url'],dic['cat_name'],
                dic['plat'],dic['room_id'],dic['room_url']))
            self.conn.commit()
            #self.conn.close()
        except Exception,e:
            self.cursor.execute("""INSERT INTO yy(title,
               num, data_period,cat_url,cat_name,plat,room_id,room_url)
            VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s')""" % (
            'emoji_name', dic['num'], dic['crawl_time'], dic['cat_url'], dic['cat_name'],
            dic['plat'], dic['room_id'],dic['room_url']))
            self.conn.commit()
            #self.conn.close()
            print 'insert err: ',e
    def insert_momo_item(self,dic):
        try:
            self.cursor.execute("""INSERT INTO zb(title,
            num, data_period,room_id,plat,star,follow,room_url)
         VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"""%(dic['title'],dic['num'],dic['crawl_time'],
            dic['room_id'],dic['plat'],dic['star'],dic['follow'],dic['room_url']))
            self.conn.commit()
        except Exception,e:
            self.cursor.execute("""INSERT INTO zb(title,
            num, data_period,room_id,plat,star,follow,room_url)
             VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"""%('emoji_name',dic['num'],dic['crawl_time'],
            dic['room_id'],dic['plat'],dic['star'],dic['follow'],dic['room_url']))
            self.conn.commit()

            print 'insert err: ',e
    def insert_momoid_list(self,dic):
        if not self.select('select * from momoid_list WHERE momoid = %s'%dic['momoid']):
            try:
                self.cursor.execute("""INSERT INTO momoid_list(momoid)
                 VALUES ('%s')""" % (
                dic['momoid']))
                self.conn.commit()
                #self.conn.close()
            except Exception,e:
                print 'insert err: ',e
        #else:
            #print 'id exists...'
    def insert_eastmoney_item(self,dic):
        try:
            self.cursor.execute("""INSERT INTO eastmoney_kw(code,title,block,flag)
         VALUES ('%s','%s','%s','%s')"""%(dic['code'],dic['title'],dic['block'],dic['flag']))
            self.conn.commit()
        except Exception,e:
            print 'insert_eastmoney_item error: ',e
    def insert_xueqiu_freq(self,dic):
        try:
            self.cursor.execute("""INSERT INTO xueqiu_freq(stk_name,freq,flag)
         VALUES ('%s','%s','%s')"""%(dic['stk_name'],dic['freq'],dic['flag']))
            self.conn.commit()
        except Exception,e:
            print 'insert_eastmoney_item error: ',e
    def insert_ftp_etl(self,dic):
        try:
            self.cursor.execute("""INSERT INTO jd_index_3_etl(f1,f2,f3,f4,f5)
                VALUES ('%s','%s','%s','%s','%s')""" % (dic[0], dic[1], dic[2], dic[3], dic[4]))
            self.conn.commit()
        except Exception,e:
            print 'insert jd_index_3_etl error: ',e
    def insert_ftp(self,dic):
        try:
            self.cursor.execute("""INSERT INTO jd_index_2(f1,f2,f3,f4,f5)
                VALUES ('%s','%s','%s','%s','%s')""" % (dic[0], dic[1], dic[2], dic[3], dic[4]))
            self.conn.commit()
        except Exception,e:
            print 'insert jd_index_e error: ',e
    def insert_airbnb(self,item):
        try:
            self.cursor.execute("""INSERT INTO airbnb(flag,room_id,room_url,title,locate,comment_num,room_type,room_mate_num,bedroom_num,bed_num,left_room,bathroom_num,bed_type,bedroom_num_1,bed_num_1,in_time,out_time,room_res_type,extra,break_rule,clean,deposit,weekends_price,last_day,price,address,owner_url,owner_id,view_num,save_num)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19],item[20],item[21],item[22],item[23],item[24],item[25],item[26],item[27],item[28],item[29]))
            self.conn.commit()
        except Exception,e:
            print 'insert airbnb error: ',e

    def insert_airbnb_comment(self, field_list):
        try:
            self.cursor.executemany("INSERT INTO airbnb_comment(flag,room_id,comment_id,comment,comment_date)VALUES (%s, %s, %s,%s,%s)",field_list)
            self.conn.commit()
        except Exception, e:
            print 'insert err: ', str(e)

    def insert_airbnb_owner(self, field_list):
        try:
            self.cursor.executemany("INSERT INTO airbnb_owner(owner_id,user_url,user_name,comment_from,comment_date,comment)VALUES (%s,%s, %s, %s,%s,%s)",field_list)
            self.conn.commit()
        except Exception, e:
            print 'insert err: ', str(e)

    def insert_single(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception ,e:
            print 'insert single error: ',e
            
    def insert_many(self,sql,items):
        try:
            self.cursor.executemany(sql,items)
            self.conn.commit()
        except Exception ,e:
            print 'insert many error: ',e


    def select(self,sel_str):
        try:
            self.cursor.execute(sel_str)
            data = self.cursor.fetchall()
            return data
        except Exception,e:
            print 'select err: ',e
            return None
    def update(self,up_str):
        try:
            self.cursor.execute(up_str)
            self.conn.commit()
            #print 'update success'
        except Exception,e:
            print 'update err: ',e

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = MySql(host='ip', port=3307, user="username", password="pwd", db="db")
    # db =MySql('localhost','root','1111','jdjr_data')
    dic = {'title':'eee','num':'233','crawl_time':'2016-09-06 11:17:32.000000'}
    #db.insert(dic)
    #db.insert_momoid_list({'momoid':'11'})
    #print db.select('select * from momoid_list WHERE momoid = 11')
    # db.insert_momoid_list({'momoid':'395786651'})
    db.insert_airbnb(['2017-01-10', u'11212829', u'https://zh.airbnb.com/rooms/11212829?checkin=2017-01-09&checkout=&guests=1&adults=1&children=0&infants=0', u'\u9633\u5149\u5c0f\u820d | \u5730\u94c18\u53f7\u7ebf\u80b2\u65b013\u53f7\u7ebf\u970d\u8425 | \u5965\u5317\u6e05\u65b0\u4e00\u5c45', u'\u5317\u4eac, Beijing Shi, \u4e2d\u56fd', '4', u'\u6574\u5957\u623f\u5b50/\u516c\u5bd3', u'3\u4f4d\u623f\u5ba2', u'1\u95f4\u5367\u5ba4', u'2\u5f20\u5e8a', '3', '1', 'None', '1', '2', u'14:00 \uff0d 00:00', '12:00', u'\u516c\u5bd3', u'\u65e0\u9700\u4ed8\u8d39', u'\u7075\u6d3b', u'\uffe535', u'\uffe5800', 'None', u'\u661f\u671f\u4e94\u548c\u661f\u671f\u516d 2\u665a ', u'\uffe5256', u'\u6e05\u6cb3', 'https://zh.airbnb.com/users/show/33012664', '33012664', 'None', u'\n        104\u4f4d\u65c5\u884c\u8005\u4fdd\u5b58\u4e86\u8be5\u623f\u6e90\n      '])
    db.close()
