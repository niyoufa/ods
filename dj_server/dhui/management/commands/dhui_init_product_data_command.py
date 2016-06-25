#coding=utf-8

import sys,pdb
import datetime,logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_product_supplierinfo as dps
import ods.dhui.dhui_stock_warehouse_orderpoint as dpwo
import ods.dhui.dhui_init_partner_info as dipi

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入商品数据到odoo"

    def handle(self, *args, **options):
        print ""
        print "开始导入商品数据到odoo..."
        InfoLogger.info("开始导入商品数据到odoo...")

        try :
            # 商品供应商信息
            result = dipi.init_partner_info()
            InfoLogger.info(result)
            # 商品基本信息
            result = dpt.import_product_template_data(*args, **options)
            InfoLogger.info(result)
            # 更新商品供应商信息
            result = dps.update_product_supplierinfo(*args, **options)
            InfoLogger.info(result)
            # 更新商品重订货规则
            result = dpwo.update_stock_warehouse_orderpoint(*args, **options)
            InfoLogger.info(result)
        except Exception,e:
            print e
            # 打印错误信息
            ErrorLogger.error("错误信息：%s."%(str(e)))
            print "日期：%s 错误信息：%s."%(str(datetime.datetime.now()),str(e))

        print "完成导入商品数据到odoo！"
        InfoLogger.info("完成导入商品数据到odoo！")
