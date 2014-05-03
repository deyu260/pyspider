#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-05-02 19:28:24

from __future__ import division
from libs.pprint import pprint
from libs.base_handler import *
import re,math,MySQLdb

class Handler(BaseHandler):
    '''
    http://www.rouding.com/
    '''
    def on_start(self):
        
        for page in range(1,61):
            if page == 1:
                self.crawl('http://www.rouding.com/chuantongshougong/', callback=self.index_page)
            else:
                self.crawl('http://www.rouding.com/chuantongshougong/page_'+str(page)+'.html', callback=self.index_page)
                
        for page in range(1,13):
            if page == 1:
                self.crawl('http://www.rouding.com/minjianyishu/', callback=self.index_page)
            else:
                self.crawl('http://www.rouding.com/minjianyishu/page_'+str(page)+'.html', callback=self.index_page)

    def index_page(self, response):
        for each in response.doc('.search+div div div a').items():
            self.crawl(each.attr.href, callback=self.detail_page,save=each.attr.href)

    def detail_page(self, response):
        
        # 基础信息
        data = {}
        if None == response.doc('.ct p:first').html() or None:
            return data


        #data['id'] = re.search(r"/(\d*)\.html", response.save).group(1)
        data['title'] = response.doc('.h').text()
        data['category'] = response.doc('.list2 a:eq(1)').text()
        
 
        # 以文字开头的段落
        if re.search(r"<img", response.doc('.ct p:first').html()):
            data['cover'] = response.doc('.ct p:first').html()
            data['body'] = response.doc('.ct p:eq(1)').text()
        else:
            data['body'] = response.doc('.ct p:first').text()
            data['cover'] = response.doc('.ct p:eq(1)').html()
            
        data['join_at'] = re.search(r"\d{4}-\d{2}-\d{2}", response.doc('.list2').html()).group(0)
        data['url'] = response.save
     
        # 步骤
        temp = []
        for each in response.doc('.ct p:gt(1)').items():
            # 过滤掉关键词站内链接
            if re.search(r"<img", each.html()):
                temp.append(each.html())
            elif each.text() != '':
                temp.append(each.text())
                
        # 单张图片，没有步骤
        if len(temp) == 0:
            return data
        # 内容底部站点推广信息过滤
        if re.search(r"shelterness|50810",response.doc('.ct').html()):
            temp = temp[0:-3]
            
        # (特殊类型)ttp://www.rouding.com/life-DIY/buyishijie/111146.html
        if re.search(r"shelterness|50810",temp[-1]):
            temp = temp[0:-1]
            
        if len(temp) % 2 != 0:
            temp.insert(0, "")
            
        position_count = int(math.ceil(len(temp))/2)
        photos = [{'position': i, 'content': temp[i*2], 'data': temp[i*2+1]} for i in range(position_count)]
        
        data['step'] = photos;
       
        return data
          
    def save(self, data):
        conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="google",db="pyspider",charset="utf8")
        cursor = conn.cursor()
        sql = "insert into rouding_basic(title,category, cover, body, join_at, url) values(%s,%s,%s,%s,%s,%s)"
        param = (data['title'],data['category'], data['cover'], data['body'], data['join_at'], data['url'])
        cursor.execute(sql, param)
        bid = cursor.lastrowid
        if data.get('step'):
            for item in data['step']:
                sql = "insert into rouding_step(bid, position, content, data) values(%s,%s,%s,%s)"
                param = (bid, item['position'], item['content'], item['data'])
                cursor.execute(sql, param)
     
        cursor.close()
        conn.close()    

    
    def on_result(self, result):
        if result:
            self.save(result)
            #pprint(result)