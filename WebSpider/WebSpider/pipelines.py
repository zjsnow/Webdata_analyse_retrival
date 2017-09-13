#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

import codecs
import json

#数据保存到数据库
class WebSpiderPipeline(object):
    #连接数据库，必须先创建好数据库和数据表，并在数据表中设定好与item属性对应的各个数据项的名称和数据类型
    def __init__(self,dbpool_):
        self.dbpool=dbpool_
        #将连接数据库的设置写死在代码中
        # self.dbpool = adbapi.ConnectionPool('MySQLdb',
        #         host='127.0.0.1',
        #         db = 'moviedb', #数据库的名称
        #         user = 'root',
        #         passwd = 'toorzjs',
        #         cursorclass = MySQLdb.cursors.DictCursor,
        #         charset = 'utf8',
        #         use_unicode = False
        # )

    #从setting中读取，更加灵活
    # @classmethod声明一个类方法，平常我们定义的是实例方法。
    #类方法的第一个参数是cls,指类本身，而实例方法的第一个参数是self,指类的实例。
    #类方法直接通过类进行调用。
    @classmethod
    def from_settings(cls,settings):
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            use_unicode=False,
        )
        dbpool_=adbapi.ConnectionPool('MySQLdb',**dbparams) #**dbparams将字典dbparams转为关键字参数，即参数名=参数值的形式
        return cls(dbpool_) #cls相当于类WebSpiderPipeline，这里返回一个类的实例

    #数据写入数据库
    def _conditonal_insert(self,tx,item):
        # 用python将数据写入mysql时，不论数据的类型，SQL语句中都用%s表示格式，在存储时会转为表中设置的格式
        sql="insert into tomatoes(name,year,link,tomatometer,audience_score,runtime,genre,director,writer,cast,movie_info) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params=(item["name"],item['year'],item['link'],item['tomatometer'],item['audience_score'],item['runtime'],item['genre'],item['director'],item['writer'],item['cast'],item['movie_info'])
        tx.execute(sql,params) #tx拥有和游标类似的API，可以操作execute方法写入sql语句

    #错误处理方法
    def _handle_error(self,failure):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failure)

    #pipeline默认调用，调用了上面两种方法
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditonal_insert,item) #dbpool.runInteraction方法是把回调的函数_conditonal_insert并在连接池中，当某个连接的Transaction对象（即tx）可用时，调用回调函数
        query.addErrback(self._handle_error)
        return item

# #数据保存到json文件
# class JsonPipeline(object):
#     def __init__(self):
#         self.file=codecs.open('tomatoes.json','w',encoding='utf-8') #引入codecs模块，指定文件的编码方式utf-8
#     def process_item(self,item,spider):
#         line=json.dumps(dict(item),ensure_ascii=False)+'\n' #.dumps是将python的字典对象转为json对象
#         self.file.write(line)
#     def spider_closed(self): #爬虫结束时spider_closed会自动被调用
#         self.file.close() #爬虫结束时，关闭文件

#数据保存到txt文件
# class TextPipeline(object):
#     def __init__(self):
#         self.file=codecs.open('tomatoes.txt','w',encoding='utf-8') #引入codecs模块，指定文件的编码方式utf-8
#         self.file.write("name\tyear\tlink\ttomatometer\taudience_score\truntime\tgenre\tdirector\twriter\tcast\tmovie_info\n")
#     def process_item(self,item,spider):
#         self.file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(item['name'],item['year'],item['link'],item['tomatometer'],item['audience_score'],item['runtime'],item['genre'],item['director'],item['writer'],item['cast'],item['movie_info']))
#     def spider_closed(self): #爬虫结束时spider_closed会自动被调用
#         self.file.close() #爬虫结束时，关闭文件

