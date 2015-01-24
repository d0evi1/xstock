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

from xstock.xueqiu.StockItem import StockItem

file_name="/Users/jungle/workspace/my_proj/xstock/api/xueqiu_apis.txt"

#----------------------------------
# 只抓取电影数据.
#----------------------------------
class StockSpider(CrawlSpider):
    name="XueqiuSpider"
    allowed_domains=["xiuqiu.com"]

    rules = [
            ## 解析item
            #Rule(SgmlLinkExtractor(allow=(r'xiuqiu.com')), callback="parse_stock", follow=None),
        ]

    #----------------------------
    # .
    #----------------------------
    def __init__(self):
        self.start_urls = []
        f = open(file_name)
        for line in f.xreadlines():
            self.start_urls.append(line.strip())
            print line

        f.close()

    #--------------------------------------
    # 处理当前页.
    #--------------------------------------
    def parse_start_url(self,response):
        item = StockItem()
        sel = Selector(response)
        log.msg(response.url, level=log.INFO)
        log.msg(response.encoding, level=log.INFO)

        item['id']          = re.findall(r'^http://xueqiu.com/s/(.*)', response.url)
        item['cur_price']   = sel.xpath('//div[@class="currentInfo"]/strong/text()').re('\d+\.?\d*')
        item['rise_rate']   = sel.xpath('//span[@class="quote-percentage"]/text()').re('([+-]\d+\.?\d*)')
        item['hk_flag']     = sel.xpath('//div/span[@class="stockType"]/text()').extract()

        open_price = u"今开"
        item['open_price']  = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % open_price).extract()

        close_price = u"昨收"
        item['close_price'] = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % close_price).extract()

        high = u"最高"
        item['high']        = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % high).extract()

        low = u"最低"
        item['low']         = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % low).extract()

        max_52 = u"52周最高"
        item['max_52']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % max_52).extract()

        min_52 = u"52周最低"
        item['min_52']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % min_52).extract()

        vol = u"成交量"
        item['vol']         = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % vol).extract()

        amount = u"成交额"
        item['amount']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % amount).extract()

        raise_limit = u"涨停价"
        item['raise_limit'] = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % raise_limit).extract()

        down_limit = u"跌停价"
        item['down_limit']  = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % down_limit).extract()

        avg_30 = u"30日均量"
        item['avg_30']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % avg_30).extract()

        market_value = u"总市值"
        item['market_value']= sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % market_value).extract()

        capital = u"总股本"
        item['capital']     = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % capital).extract()

        capital_flow = u"流通股本"
        item['capital_flow']= sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % capital_flow).extract()

        eps = u"每股收益"
        item['eps']         = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % eps).extract()

        bvps = u"每股净资产"
        item['bvps']        = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % bvps).extract()

        dps = u"每股股息"
        item['dps']         = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % dps).extract()

        pe = u"市盈率LYR/TTM"
        pe2 = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % pe).re(r"(\d+\.\d+)")

        item['pe_lyr']      = pe2[0] if len(pe2)>=1 else []
        item['pe_ttm']      = pe2[1] if len(pe2)>=2 else []

        pb_ttm = u"市净率TTM"
        item['pb_ttm']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % pb_ttm).extract()

        ps_ttm = u"市销率TTM"
        item['ps_ttm']      = sel.xpath('//td[contains(text(),"%s")]/text()/following-sibling::span[1]/text()' % ps_ttm).extract()

        item['daytime']     = sel.xpath('//span[@id="timeInfo"]/text()').re(r'\d+-\d+-\d+ \d+:\d+:\d+')

        log.msg("pe2=%s, %s" % (pe2, item), level=log.INFO)
        return item
