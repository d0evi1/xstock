#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------------------------------------
# 用于抓取页面.
# @author   d0evi1 
# @date     2014.11.8
#---------------------------------------

import re
from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xstock.stock.StockItem import StockItem

file_name="/Users/jungle/workspace/my_proj/xstock/api/sina_apis.txt"

#----------------------------------
# 只抓取电影数据.
#----------------------------------
class StockSpider(CrawlSpider):
    name="StockSpider"
    allowed_domains=["sinajs.cn"]

    rules = [
            ## 解析item
            Rule(SgmlLinkExtractor(allow=(r'hq.sinajs.cn')), callback="parse_list", follow=None),
        ]

    #----------------------------
    # .
    #----------------------------
    def __init__(self):
        self.start_urls = []
        f = open(file_name)
        for line in f.xreadlines():
            log.msg(line, level=log.INFO)
            self.start_urls.append(line.strip())
            print line

        f.close()

#        self.rules = [
#            ## 解析item
#            Rule(SgmlLinkExtractor(allow=(r'hq.sinajs.cn')),callback="parse_list", follow=True),
#        ]
#'''


    #--------------------------------------
    # 处理当前页.
    #--------------------------------------
    def parse_start_url(self,response):
        item = StockItem()
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)

        item['stocks'] = sel.extract()
        log.msg(item['stocks'], level=log.INFO)
        return item
