#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-04-28 16:05:15


from libs.pprint import pprint
from libs.base_handler import *
import MySQLdb
import re


class Handler(BaseHandler):
    '''
    douban_group
    '''
    def on_start(self):
        None
        #self.crawl('http://www.douban.com/group/wakao/?ref=sidebar', callback=self.detail_page)

    def on_message(self, project, message):
        self.crawl('http://www.douban.com/group/'+message + '?ref=sidebar', callback=self.detail_page)
        
    def detail_page(self, response):
        group = {}
        group['gid'] = re.search(r"/group/([\s\S]*)/", response.doc('.feed-link a').attr.href).group(1)
        group['face'] = response.doc('#group-info img').attr.src
        group['name'] = response.doc('#group-info h1').text()
        group['leader'] = user_id = re.search("/people/([\s\S]*)/", response.doc(".group-board a").attr.href).group(1)
        group['content'] = response.doc('.group-intro').html()
        group['join_at'] = re.search(r"\d{4}-\d{2}-\d{2}",response.doc('.group-board p').text()).group(0)
        self.send_message('douban_user', user_id)
        return group

    def save(self, data):
        conn=MySQLdb.connect(host="localhost",user="root",passwd="google",db="pyspider",charset="utf8")
        cursor = conn.cursor()
        sql = "insert into douban_group(gid,face, name, leader, content, join_at) values(%s,%s,%s,%s,%s,%s)"
        param = (data['gid'],data['face'], data['name'], data['leader'], data['content'], data['join_at'])
        cursor.execute(sql, param)
        cursor.close()
        conn.close()
        
    def on_result(self, result):
        if result:
            #pprint(result)
            self.save(result)
