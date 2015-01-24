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
                db = 'stock_xueqiu',
                user = 'root',
                passwd = '',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )

        cur_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        self.table_name = "t_stock_info_%s" % (cur_time)


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
        if isinstance(item_list, int):
            return item_list
        
        length = len(item_list)
        if length > 0:
            ret = item_list[0].strip()
        else:
            if is_none:
                ret = None
        return ret

    #----------------------------
    #
    #---------------------------
    def get_num(self, item_list, is_none=False):
        item = self.get_first(item_list, is_none)
        if item is not None:
            if item == "-":
                return None
            else:
                return item

        return item

    #-----------------------------
    # 获取香港通标志位
    #----------------------------
    def get_hkflag(self, hkflag):
        if hkflag == u"沪港通":
            return 1
        elif hkflag == u"深港通":
            return 2
        else:
            return 0

    #-------------------------------
    # 爬虫过滤所需，判断一个值是否存在. 
    #------------------------------
    def is_not_exists(self, val):
        if val is None or val == "":
            return True 
        else:
            return False 

    #-----------------------------
    # 亿元  => 万股
    # 亿股  => 万股
    # @is_yi   0: 万为单位   1:亿为单位
    #-----------------------------
    def get_money(self, money, is_yi=0):
        unit_w = u"万"
        unit_y = u"亿"

        num = re.findall(r'(\d+\.\d+)', money)

        if len(num) == 0:
            return None

        if is_yi:
            if money.find(unit_w) >=0:
                return float(num[0])/10000

            if money.find(unit_y) >=0:
                return  float(num[0])

            return float(num[0])/100000000

        else:
            if money.find(unit_w) >=0:
                return float(num[0])

            if money.find(unit_y) >=0:
                return  float(num[0]) * 10000

            return float(num[0])/10000

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
        stock_id        = self.get_first(item['id'])
        cur_price       = self.get_num(item['cur_price'])
        rise_rate       = self.get_num(item['rise_rate'])
        hk_flag         = self.get_hkflag(item['hk_flag'])
        open_price      = self.get_num(item['open_price'])
        close_price     = self.get_num(item['close_price'])

        high            = self.get_num(item['high'])
        low             = self.get_num(item['low'])

        max_52          = self.get_first(item['max_52'])
        min_52          = self.get_first(item['min_52'])

        vol             = self.get_money(self.get_first(item['vol']))
        amount          = self.get_money(self.get_first(item['amount']))

        raise_limit     = self.get_first(item['raise_limit'])
        down_limit      = self.get_first(item['down_limit'])
        avg_30          = self.get_money(self.get_first(item['avg_30']))

        market_value    = self.get_money(self.get_first(item['market_value']), 1)
        capital         = self.get_money(self.get_first(item['capital']), 1)
        capital_flow    = self.get_money(self.get_first(item['capital_flow']), 1)

        eps             = self.get_first(item['eps'])
        bvps            = self.get_first(item['bvps'])
        dps             = self.get_num(item['dps'])

        pe_lyr          = self.get_first(item['pe_lyr'])
        pe_ttm          = self.get_first(item['pe_ttm'])
        pb_ttm          = self.get_first(item['pb_ttm'])
        ps_ttm          = self.get_first(item['ps_ttm'])

        daytime         = self.get_first(item['daytime'])

        if self.is_not_exists(daytime) or self.is_not_exists(cur_price):
            log.msg("[no-process] id=%s" % stock_id, level=log.INFO)
            return


        log.msg(self.table_name, level=log.INFO)
        tx.execute("insert into " + self.table_name + "\
                (id,\
                cur_price,          \
                rise_rate,          \
                hk_flag,            \
                open_price,             \
                close_price,            \
                high,                   \
                low,                    \
                max_52,                 \
                min_52,                 \
                vol,                    \
                amount,                 \
                raise_limit,            \
                down_limit,             \
                avg_30,                 \
                market_value,           \
                capital,                \
                capital_flow,           \
                eps,                    \
                bvps,                   \
                dps,                    \
                pe_lyr,                 \
                pe_ttm,                 \
                pb_ttm,                 \
                ps_ttm,                 \
                daytime)   \
                values (%s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s, %s, %s, %s, %s, \
                        %s)",  \
            (stock_id,                 \
            cur_price,          \
            rise_rate,          \
            hk_flag,            \
            open_price,         \
            close_price,        \
            high,               \
            low,                \
            max_52,             \
            min_52,             \
            vol,                \
            amount,             \
            raise_limit,        \
            down_limit,         \
            avg_30,             \
            market_value,       \
            capital,            \
            capital_flow,       \
            eps,                \
            bvps,               \
            dps,                \
            pe_lyr,             \
            pe_ttm,             \
            pb_ttm,             \
            ps_ttm,             \
            daytime))

        #log.msg(content, level=log.INFO)

    ###
    def handle_error(self, e):
        log.err(e)
