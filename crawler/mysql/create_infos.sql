
create database if not exists xstock charset=utf8;

use xstock;

-- ------------------------------
-- 股票列表 (sina_version).
-- ------------------------------
drop table if exists t_stock_info1_tpl;
create table if not exists t_stock_info1_tpl (
    id              varchar(36) not null comment '股票代码',

    today_opening_price         double  comment '今日开盘价',
    yesterday_closing_price     double  comment '昨日收盘价',
    cur_price               double      comment '当前价',
    today_max_price         double      comment '今日最高价',
    today_min_price         double      comment '今日最低价',
    bids_price              double      comment '竞买价，买一报价',
    auction_price           double      comment '竞卖价，卖一报价',
    total_trade_shares      bigint      comment '成交股票数, 单位:手(1/100)',
    total_trade_price       bigint      comment '成交金额，单位:万元(/1w)',


    buy1_shares             int         comment '买一, 股数: 单位:股',
    buy1_price              double      comment '买一, 价格: 单位:元', 
    buy2_shares             int         comment '买二，xxx', 
    buy2_price              double      comment '买二, xxx',
    buy3_shares             int         comment '买三, xxx',
    buy3_price              double      comment '买三, xxx',
    buy4_shares             int         comment '买四，xxx',
    buy4_price              double      comment '买四, xxx',
    buy5_shares             int         comment '买五, xxx',
    buy5_price              double      comment '买五, xxx',  
   
    sell1_shares            int         comment '卖一, 股数, 单位: 股',
    sell1_price             double      comment '卖一，价格, 单位: 价格',
    sell2_shares            int         comment '卖二, xxx',
    sell2_price             double      comment '卖二, xxx',
    sell3_shares            int         comment '卖三, xxx',
    sell3_price             double      comment '卖三，xxx',
    sell4_shares            int         comment '卖四, xxx',
    sell4_price             double      comment '卖四, xxx',
    sell5_shares            int         comment '卖五，xxx',
    sell5_price             double      comment '卖五, xxx',

    day                 date not null comment '当前日期',
    time                time not null comment '日期时间: 2008-11-11 11:11:11'
) engine=MyISAM charset=utf8;
