#coding=utf-8

import sys,pdb
import datetime,logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_user as du
import ods.dhui.dhui_address as dadd

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入用户数据到odoo"

    def handle(self, *args, **options):
        print ""
        print "开始导入用户及地址数据到odoo..."
        InfoLogger.info("开始导入用户及地址数据到odoo...")

        try :
            # 用户基本信息
            result = du.import_user_data(*args,**options)
            InfoLogger.info(result)

            # 用户地址信息
            result = dadd.import_address_data(*args,**options)
            InfoLogger.info(result)
        except Exception,e:
            print e
            # 打印错误信息
            ErrorLogger.error("错误信息：%s."%(str(e)))
            print "日期：%s 错误信息：%s."%(str(datetime.datetime.now()),str(e))

        print "完成导入用户及地址数据到odoo！"
        InfoLogger.info("完成导入用户及地址数据到odoo！")
