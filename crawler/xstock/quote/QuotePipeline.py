# -*- coding: utf-8 -*-

#-----------------------------------------------
# QuotePipeline 
# @author   d0evi1
# @date     2014.12.30
#-----------------------------------------------

from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector


from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

import re
import time

#-----------------------------------
# 电影pipeline.
#-----------------------------------
class QuotePipeline(object):
    
    #------------------------------
    # mysql/redis.
    #------------------------------
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'xstock',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    
    #-----------------------------
    # 将一个list列表做拼接.
    #-----------------------------
    def get_items(self, item_list):
        ret = ''
        length = len(item_list)
        for n in xrange(length):
            ret += item_list[n]
            if n < length-1:
                ret += '/'

        return ret.strip()

    #-----------------------------
    # 获取list的第一个元素, 如果不存在，返回空.
    #-----------------------------
    def get_first(self, item_list, is_none=False):
        ret = ''
        length = len(item_list)
        if length > 0:
            ret = item_list[0].strip()
        else:
            if is_none:
                ret = None 
        return ret

    #-----------------------------
    # 处理主逻辑.
    #-----------------------------
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)
        return item

    #------------------------------
    ### insert into db.
    #------------------------------
    def insert_data(self, tx, item):
        stocks = item['stocks']  
        
        for stock in stocks:
            csel = Selector(text=stock)
            
            id      = csel.xpath('//a/text()').re('\((.*?)\)')
            name    = csel.xpath('//a/text()').re('(.*?)\(')
            exchange = csel.xpath('//a/@href').re('http://quote.eastmoney.com/(.*?).html')
            #exchange = re.findall(r'(.*?)\d+', exchange)
            log.msg('id=%s, name=%s, url=%s' % (id, name, exchange), level=log.INFO)
         
            update_time  = int(time.time())

            tx.execute(\
                "insert ignore into t_stock_list (id,\
                    name,       \
                    exchange)   \
                    values (%s, %s, %s)",\
                (id,        \
                name,       \
                exchange))

    ###
    def handle_error(self, e):
        log.err(e)
