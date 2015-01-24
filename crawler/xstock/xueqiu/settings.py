# -*- coding: utf-8 -*-

# Scrapy settings for xstock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stock'

SPIDER_MODULES = ['xstock.xueqiu']
NEWSPIDER_MODULE = 'xstock.xueqiu'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xspider (+http://www.yourdomain.com)'

ITEM_PIPELINES={
    'xstock.xueqiu.StockPipeline.StockPipeline':400,
}

DOWNLOAD_DELAY = 2

## 随机下载
RANDOMIZE_DOWNLOAD_DELAY = True


## 伪造浏览器 user_agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

## 开启cookie.
COOKIES_ENABLED = True

#这是爬虫中间件，， 543是运行的优先级
#SPIDER_MIDDLEWARES = {
#    'xspider.movie.MovieMiddleware.MovieMiddleware': 543,
#}



## 深度优先 or 宽度优先
#SCHEDULER_DISK_QUEUE = ’scrapy.squeue.PickleFifoDiskQueue’
#SCHEDULER_MEMORY_QUEUE = ’scrapy.squeue.FifoMemoryQueue’


## 日志
LOG_ENABLED     = True
LOG_ENCODING    = 'utf-8'
LOG_FILE        = '/Users/jungle/workspace/my_proj/xstock/log/xueqiu.log'
LOG_LEVEL       = 'INFO'
LOG_STDOUT      = True
