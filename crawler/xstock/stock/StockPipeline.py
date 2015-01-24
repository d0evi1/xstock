# -*- coding: utf-8 -*-

#-----------------------------------------------
# StockPipeline 
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
class StockPipeline(object):
    
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

        cur_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        self.table_name = "t_stock_info1_%s" % (cur_time)


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
        stock = item['stocks']
        [content,] = re.findall(r'=\"(.*?)\"', stock)
        stock_info = content.split(",")
        if len(stock_info) < 31:
            log.msg("stock len: %d" % len(stock_info))
            return

        tx.execute("insert into " + self.table_name + "\
                (id,\
                today_opening_price,        \
                yesterday_closing_price,    \
                cur_price,                  \
                today_max_price,            \
                today_min_price,            \
                bids_price,                 \
                auction_price,              \
                total_trade_shares,         \
                total_trade_price,          \
                buy1_shares,                \
                buy1_price,                 \
                buy2_shares,                \
                buy2_price,                 \
                buy3_shares,                \
                buy3_price,                 \
                buy4_shares,                \
                buy4_price,                 \
                buy5_shares,                \
                buy5_price,                 \
                sell1_shares,               \
                sell1_price,                \
                sell2_shares,               \
                sell2_price,                \
                sell3_shares,               \
                sell3_price,                \
                sell4_shares,               \
                sell4_price,                \
                sell5_shares,               \
                sell5_price,                \
                day,                        \
                time)   \
                values (%s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s)",  \
            ( \
            stock_info[0],      \
            stock_info[1],      \
            stock_info[2],      \
            stock_info[3],      \
            stock_info[4],      \
            stock_info[5],      \
            stock_info[6],      \
            stock_info[7],      \
            stock_info[8],      \
            stock_info[9],      \
            stock_info[10],     \
            stock_info[11],     \
            stock_info[12],     \
            stock_info[13],     \
            stock_info[14],     \
            stock_info[15],     \
            stock_info[16],     \
            stock_info[17],     \
            stock_info[18],     \
            stock_info[19],     \
            stock_info[20],     \
            stock_info[21],     \
            stock_info[22],     \
            stock_info[23],     \
            stock_info[24],     \
            stock_info[25],     \
            stock_info[26],     \
            stock_info[27],     \
            stock_info[28],     \
            stock_info[29],     \
            stock_info[30],     \
            stock_info[31]))

        #log.msg(content, level=log.INFO)

    ###
    def handle_error(self, e):
        log.err(e)
