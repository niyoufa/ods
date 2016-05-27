#coding=utf-8

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option
import datetime,logging

import sys,pdb
sys.path.append(settings.ODS_PARENT_PATH)
import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_product_supplierinfo as dps
import ods.dhui.dhui_stock_warehouse_orderpoint as dpwo

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入商品数据到odoo"

    def handle(self, *args, **options):
        try :
            # 商品基本信息
            dpt.import_product_template_data()
            # 更新商品供应商信息
            dps.update_product_supplierinfo()
            # 更新商品重订货规则
            dpwo.update_stock_warehouse_orderpoint()
            # 记录日志
            InfoLogger.info("%s:导入商品数据到odoo."%str(datetime.datetime.now()))
        except Exception,e:
            print e
            # 打印错误信息
            ErrorLogger.error("错误信息：%s"%str(e))