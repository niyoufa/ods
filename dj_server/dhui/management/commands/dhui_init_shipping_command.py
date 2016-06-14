#coding=utf-8

import datetime,logging
import sys,pdb

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_shipping as ds

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入物流数据"

    def handle(self, *args, **options):
        print "开始导入物流数据..."
        InfoLogger.info("开始导入物流数据...")
        try :
            # 更新用户
            ds.import_shipping_data()
        except Exception,e:
            print e

        print "完成导入物流数据!"
        InfoLogger.info("完成导入物流数据!")