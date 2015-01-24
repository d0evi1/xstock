
create database if not exists stock_xueqiu charset=utf8;

use stock_xueqiu;

-- ------------------------------
-- 股票列表 (xueqiu).
-- ------------------------------
drop table if exists t_stock_info_tpl;
create table if not exists t_stock_info_tpl (
    id              varchar(36) not null primary key comment '股票代码',

    cur_price               double      comment '当前价',
    rise_rate               double      comment '涨跌幅',
    hk_flag                 int         comment '0-正常 1-沪港通 2-深港通',

    open_price              double      comment '今开: 特指今日',
    close_price             double      comment '昨收: 特指昨天',
    
    high                    double      comment '最高',
    low                     double      comment '最低',
    
    max_52                  double      comment '52周最高',
    min_52                  double      comment '52周最低',

    vol                     double      comment '成交量, 单位:万股(1手＝100股)',
    amount                  double      comment '成交金额，单位:万元(/1w)',

    raise_limit             double      comment '涨停',
    down_limit              double      comment '跌停',    
    avg_30                  double      comment '30日均量',

    market_value            double      comment '总市值：单位: 亿',
    capital                 double      comment '总股本: 单位: 亿',
    capital_flow            double      comment '流通股本: 单位：亿',

    eps                     double      comment '每股收益: Earnings Per Share',
    bvps                    double      comment '每股净收益: Book Value Per Share',
    dps                     double      comment '每股股息: Dividend Per Share',

    pe_lyr                  double      comment '市盈率(P/E=每股价格/每股收益)  LYR:Last Year Rate',
    pe_ttm                  double      comment '市盈率  TTM: Trailing Twelve Months',
    pb_ttm                  double      comment '市净率(P/B=每股股价/每股净资产) TTM',
    ps_ttm                  double      comment '市销率(PS=总市值+主营业务收入=股价+每股销售额)TTM',

    daytime                datetime not null comment '日期时间: 2008-11-11 11:11:11'
) engine=MyISAM charset=utf8;
