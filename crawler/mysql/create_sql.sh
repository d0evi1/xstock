#!/bin/bash

cur_date=`date +%Y%m%d`

t1_prefix="t_stock_info1"
tpl_table="${t1_prefix}_tpl"
cur_table="${t1_prefix}_${cur_date}"

DB_NAME="xstock"


function exec_mysql()
{
    echo "$1" | mysql -uroot ${DB_NAME} -N
}


#-------------------------------
#
#-------------------------------
function create_infos()
{
    exec_mysql "drop table if exists ${cur_table};
        create table if not exists ${cur_table} like ${tpl_table}"
}


#--------------------------------
#
#--------------------------------
function main()
{
    create_infos
}

main
