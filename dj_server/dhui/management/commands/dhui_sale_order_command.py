#coding=utf-8

import datetime,logging
import sys,pdb

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入订单数据到odoo"

    def handle(self, *args, **options):
        print "\n"
        print "开始导入订单数据到odoo..."
        InfoLogger.info("开始导入订单数据到odoo...")

        try :
            # 订单基本信息
            result = do.import_sale_order_data(*args, **options)
            InfoLogger.info(result)
            # 订单商品信息
            result = dol.import_sale_order_line(*args, **options)
            # 记录日志
            InfoLogger.info(result)
        except Exception,e:
            print e

        print "完成导入订单数据到odoo!"
        InfoLogger.info("完成导入订单数据到odoo!")
