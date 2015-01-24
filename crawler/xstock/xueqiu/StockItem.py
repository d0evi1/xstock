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
class StockItem(Item):
    id              = Field()   ## 股票列表. 
    cur_price       = Field()
    rise_rate       = Field()
    hk_flag         = Field()

    open_price      = Field()
    close_price     = Field()

    high            = Field()
    low             = Field()

    max_52          = Field()
    min_52          = Field()

    vol             = Field()
    amount          = Field()

    raise_limit     = Field()
    down_limit      = Field()
    avg_30          = Field()

    market_value    = Field()
    capital         = Field()
    capital_flow    = Field()

    eps             = Field()
    bvps            = Field()
    dps             = Field()

    pe_lyr          = Field()
    pe_ttm          = Field()
    pb_ttm          = Field()
    ps_ttm          = Field()

    daytime         = Field()
    pass
