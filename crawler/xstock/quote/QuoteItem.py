# -*- coding: utf-8 -*-

#----------------------------------------------- 
# 股票列表. 
#
# author:   d0evi1
# date:     2014.12.30
#-----------------------------------------------

from scrapy.item import Item, Field 

#-----------------------------
# 股票列表. 
#-----------------------------
class QuoteItem(Item):
    stocks   = Field()   ## 股票列表. 

    pass