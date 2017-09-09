#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

class WebSpiderPipeline(object):
    #连接数据库
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                host='127.0.0.1',
                db = 'moviedb',
                user = 'root',
                passwd = 'toorzjs',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )

    #数据写入数据库
    def _conditonal_insert(self,tx, item):
        sql="insert into tomatoes(name,year,link,tomatometer,audience_score,runtime,genre,director,writer,cast,movie_info) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" #用python将数据写入mysql时，不论数据的类型，SQL语句中都用%s表示格式，在存储时会转为表中设置的格式
        params=(item["name"],item['year'],item['link'],item['tomatometer'],item['audience_score'],item['runtime'],item['genre'],item['director'],item['writer'],item['cast'],item['movie_info'])
        tx.execute(sql,params)

    #错误处理方法
    def _handle_error(self,failure):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failure)

    #pipeline默认调用，调用了上面两种方法
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditonal_insert,item) #调用插入的方法
        query.addErrback(self._handle_error)
        return item
