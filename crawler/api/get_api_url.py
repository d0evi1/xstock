#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import MySQLdb.cursors


#------------------------------------------
# 遍历数据库 (每天一次. 下午3点半执行)
# 利用新浪财经接口获取股票数据
#
#------------------------------------------
class XstockApi:

    def __init__(self):
        return

    ### 
    def init(self):
        self.conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="xstock",charset="utf8")
        self.cursor = self.conn.cursor()

        return

    ###
    def close(self):
        self.conn.close()

    #-------------------------------
    ## 输出文件 还是 打印
    #-------------------------------
    def print_out(self, out_type):
        return


    ### 遍历db列表.
    def process(self, api_type, out_type):
        sql = "select * from t_stock_list"
        n = self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            id       = row[0]
            name     = row[1]
            exchange = row[2]

            if api_type == 'sina':
                request_url = "http://hq.sinajs.cn/list=%s" % (exchange)
                print request_url
            elif api_type == 'tencent':
                request_url = "http://qt.gtimg.cn/q=%s" % (exchange)
                print request_url
            elif api_type == 'xueqiu':
                request_url = "http://xueqiu.com/s/%s" % (exchange)
                print request_url

        self.cursor.close()
        return

#-----------------------------------------
# main
#-----------------------------------------
if __name__ == '__main__':
    stock = XstockApi()
    stock.init()
    stock.process(sys.argv[1], sys.argv[2])
    stock.close()
