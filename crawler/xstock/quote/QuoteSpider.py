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
from xstock.quote.QuoteItem import QuoteItem


#----------------------------------
# 只抓取电影数据.
#----------------------------------
class QuoteSpider(CrawlSpider):
    name="QuoteSpider"
    allowed_domains=["eastmoney.com"]

    start_urls=["http://quote.eastmoney.com/stocklist.html"]
    rules=[
        ## 解析item
        Rule(SgmlLinkExtractor(allow=(r'^http://quote.eastmoney.com/stocklist.html$')),callback="parse_list", follow=True),      
        ]

    #-------------------------------------
    # 处理股票列表.
    #-------------------------------------
    def process_list(self, response, sel):
        item = QuoteItem()
      
        ## 电影物殊部分 
        item['stocks'] = sel.xpath('//div[@id="quotesearch"]/ul/li').extract()
        
        #log.msg("stocks: %s" % item, level=log.INFO)
        return item

    #--------------------------------------
    # 解析html元素.
    #--------------------------------------
    def parse_list(self,response):
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)

        return self.process_list(response, sel) 
