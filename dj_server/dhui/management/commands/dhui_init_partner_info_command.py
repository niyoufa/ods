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
import ods.dhui.dhui_init_partner_info as dipi

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "初始化供应商数据"

    def handle(self, *args, **options):
        try :
            # 初始化供应商数据
            dipi.init_partner_info()
            # 记录日志
            InfoLogger.info("%s:初始化供应商数据."%str(datetime.datetime.now()))
        except Exception,e:
            print e
            # 打印错误信息
            ErrorLogger.error("错误信息：%s"%str(e))