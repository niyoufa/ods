#coding=utf-8

import sys,pdb
import datetime,logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_product_supplierinfo as dps
import ods.dhui.dhui_init_partner_info as dipi

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "初始化供应商数据"

    def handle(self, *args, **options):
        print "开始导入供应商数据..."
        InfoLogger.info("开始导入供应商数据...")

        try :
            # 初始化供应商数据
            dipi.init_partner_info()
        except Exception,e:
            print "错误信息：%s"%str(e)
            ErrorLogger.error("错误信息：%s"%str(e))

        print "完成供应商数据导入!"
        InfoLogger.info("完成供应商数据导入!")
