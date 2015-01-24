#!/bin/bash

date +"%Y%m%d %H:%m:%s"
date +%s

killall -9 python

PROJ_DIR="/Users/jungle/workspace/my_proj/xstock"

### 1. quote.
#rm ./log/quote.log
#export SCRAPY_PROJECT=QuoteSpider
#scrapy crawl QuoteSpider

#-----------------------------
#
#-----------------------------
function get_api()
{
    ## 
    cd ${PROJ_DIR}/api
    ./get_api_url.py sina       > sina_apis.txt 
    ./get_api_url.py tencent    > tencent_apis.txt
    ./get_api_url.py xueqiu     > xueqiu_apis.txt
}

#-----------------------------
#
#-----------------------------
function run_sql()
{
    cd ${PROJ_DIR}
    ./mysql/create_sql.sh
}


#-----------------------------
#
#-----------------------------
function start_stock()
{
    cd ${PROJ_DIR}

    ##
    rm ${RPOJ_DIR}/log/quote.log

    ## run.
#    export SCRAPY_PROJECT=StockSpider
#    scrapy crawl StockSpider

    
    SPIDER_NAME=XueqiuSpider
    export SCRAPY_PROJECT=${SPIDER_NAME}
    scrapy crawl ${SPIDER_NAME} 

}


#----------------------------
#
#----------------------------
function main()
{
#    get_api
#    run_sql
    start_stock
}

main



#find . -name "*.pyc" -print -exec rm -rf {} \;
