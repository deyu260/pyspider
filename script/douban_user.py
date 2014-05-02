#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-04-28 16:04:55

from libs.pprint import pprint
from libs.base_handler import *
import MySQLdb
import re

class Handler(BaseHandler):
    '''
    douban_user
    '''
    
    def on_start(self):
        None
        #self.crawl("http://www.douban.com/people/sqss0506/", callback=self.detail_page)
  
    def on_message(self, project, message):
        self.crawl('http://www.douban.com/people/'+message, callback=self.detail_page)
        
    def detail_page(self, response):
        data={}
        data['face'] = response.doc('.userface').attr.src
        data['display_name'] = response.doc('title').text()
        data['link_name'] = re.search(r"/people/([\s\S]*)/", response.doc('.pic a').attr.href).group(1)
        data['join_at'] = re.search(r"\d{4}-\d{2}-\d{2}", response.doc('.user-info .pl').text()).group(0)
        data['location'] = response.doc('.user-info a').text()
        return data

    def save(self, data):
        conn=MySQLdb.connect(host="localhost",user="root",passwd="google",db="pyspider",charset="utf8")
        cursor = conn.cursor()
        sql = "insert into douban_user(face, display_name, link_name, location, join_at) values(%s,%s,%s,%s,%s)"
        param = (data['face'], data['display_name'], data['link_name'], data['location'], data['join_at'])
        cursor.execute(sql, param)
        cursor.close()
        conn.close()

    def on_result(self, result):
        if result:
            #pprint(result)
            self.save(result)
