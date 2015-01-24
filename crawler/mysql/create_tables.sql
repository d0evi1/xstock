
create database if not exists xstock charset=utf8;

use xstock;

-- ------------------------------
-- 股票列表.
-- ------------------------------
drop table if exists t_stock_list;
create table if not exists t_stock_list (
    id          varchar(36) not null primary key    comment '股票代码',
    name        varchar(36) not null                comment '股票名',
    exchange    varchar(36) not null                comment '交易所'
) engine=MyISAM charset=utf8;

