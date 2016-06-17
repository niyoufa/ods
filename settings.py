#coding=utf-8

from local_settings import *

#东汇商城数据库
DHUI_ODOO_DATABASE = "dhui"

REPORT_STRAT_TIME = "18:00:01"
REPORT_END_TIME = "18:00:00"

# res.partner
# id |          name
# ----+------------------------
#   1 | 东汇商城
#   3 | Administrator
#   4 | Public user
#   5 | Template User
#   6 | 普通客户
#   7 | 东汇商城供应商
#   8 | 供应商
#   9 | 东汇商城进销存管理员
#  10 | 东汇商城秒拍商品供应商
#  11 | 秒拍供应商
COMMON_CUSTOMER_ID = 6
COMPANY_ID = 1
DHUI_PARTNER_ID = 7

DHUI_PARTNER_DICT = {
    "default":["571dbf0c006f874b52b126aa",7,"default"],
    "seckill":["57330c6c006f877f57fcc4e7",10,"seckill"],
    "other":["5720201c006f873b606394fb",13,"other"],

    "7":["571dbf0c006f874b52b126aa",7,"default"],
    "10":["57330c6c006f877f57fcc4e7",10,"seckill"],
    "13":["5720201c006f873b606394fb",13,"other"],

    "571dbf0c006f874b52b126aa":["571dbf0c006f874b52b126aa",7,"default"],
    "57330c6c006f877f57fcc4e7":["57330c6c006f877f57fcc4e7",10,"seckill"],
    "5720201c006f873b606394fb":["5720201c006f873b606394fb",13,"other"]

}

#东汇商城商品 分类id
#select * from product_category where name = '东汇商品' ;
PRODUCT_CATEGRAY_ID = 3

#库存id
DHUI_STOCK_WAREHOUSE_ID = 1

# 东汇进销存管理员 id
DHUI_MANAGER_USER_ID = 5

DHUI_URL_PREFIX = "dhui/api?"
ODS_ADDRESS = "http://120.26.226.63:8085/"
