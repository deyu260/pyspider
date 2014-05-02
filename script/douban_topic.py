#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-04-28 16:05:27

from libs.pprint import pprint
from libs.base_handler import *
import MySQLdb
import re

class Handler(BaseHandler):
    '''
    douban topic
    '''
    def on_start(self):
        topic_params = {'q': '手工','cat': 1013,'sort': 'relevance'}
        for page in range(100,102):
            topic_params['start'] = page * 50
            self.crawl('http://www.douban.com/group/search', params=topic_params, callback=self.search_page)

    def search_page(self, response):
        for item in response.doc('.td-subject a').items():
            self.crawl(item.attr.href, callback=self.topic_page)
            
    def topic_page(self, response):
        #group
        group_id = re.search(r"group/([\s\S]*)/", response.doc('.title a').attr.href).group(1)
        self.send_message('douban_group', group_id)
        
        #user
        user_id = re.search(r"/people/([\s\S]*)/",response.doc('.topic-doc .from a').attr.href).group(1)
        self.send_message('douban_user', user_id)
        
        #topic
        topic = {}
        topic['tid'] = re.search(r"/topic/(\d*)/", response.doc('#reviews a:first').attr.href).group(1)
        topic['user'] = user_id
        topic['group'] = group_id
        topic['title'] = response.doc('.tablecc').html() or response.doc('#content h1').text()
        topic['content'] = response.doc('.topic-content:last').html()
        topic['join_at'] = response.doc('.topic-doc  .color-green').text()
        return topic
        
    def save(self, data):
        conn=MySQLdb.connect(host="localhost",user="root",passwd="google",db="pyspider",charset="utf8")
        cursor = conn.cursor()
        sql = "insert into douban_topic(tid, user_id, group_id, title, content, join_at) values(%s,%s,%s,%s,%s,%s)"
        param = (data['tid'], data['user'], data['group'], data['title'], data['content'], data['join_at'])
        cursor.execute(sql, param)
        cursor.close()
        conn.close()

    def on_result(self, result):
        if result:
            #pprint(result)
            self.save(result)
            
