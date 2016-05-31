#coding=utf-8
import os , sys , pdb
import platform

sys.path.append(os.path.dirname(os.getcwd()))
import tnd_server

BASE_DIR = os.path.dirname(tnd_server.__file__)

SERVER_HOST = "localhost"
SERVER_PORT = 8002

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

HOST = "localhost"
PORT = 27018



ODS_PARENT_PATH = '/home/dhui100/develop/'

HOST = "localhost"
PORT = 8888
DB = "dhui"
USER = "admin"
PASS = "dhui123"

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGO_DB = "dhui100"
MONGO_DB = "dhui100"

SERVER_MONGODB_HOST = "120.26.241.214"
SERVER_MONGODB_PORT = 27017
SERVER_MONGO_DB = "dhui100"
SERVER_MONGODB_USER = "dhui100"
SERVER_MONGODB_PASS = "dhui123"

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
    "default":7,
    "seckill":10,
}

#东汇商城商品 分类id
#select * from product_category where name = '东汇商品' ;
PRODUCT_CATEGRAY_ID = 3

#库存id
DHUI_STOCK_WAREHOUSE_ID = 1

# 东汇进销存管理员 id
DHUI_MANAGER_USER_ID = 5



