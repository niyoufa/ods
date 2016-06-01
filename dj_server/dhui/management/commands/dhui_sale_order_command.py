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
        try :
            # 订单基本信息
            do.import_sale_order_data()
            # 订单商品信息
            dol.import_sale_order_line()
            # 记录日志
            InfoLogger.info("%s:导入订单数据到odoo." % str(datetime.datetime.now()))
        except Exception,e:
            print e
