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
    help = "初始化数据"

    def handle(self, *args, **options):
        print "开始初始化数据..."
        InfoLogger.info("开始初始化数据...")
        try :
                # 更新用户
            call_command("dhui_init_user_info")

            # 更新商品
            call_command("dhui_init_product_data_command")

            for delta in range(30):
                print "#########"
                InfoLogger.info("#########")
                print "#" + " " + "日期：%s"%str(datetime.datetime.now()-datetime.timedelta(delta))
                InfoLogger.info("#" + " " + "日期：%s"%str(datetime.datetime.now()-datetime.timedelta(delta)))
                print "#########"
                InfoLogger.info("#########")
                # 刷新订单
                call_command("dhui_sale_order_command",delta=delta)
                # 刷新发货单
                call_command("partner_good_deliver_details",delta=delta)
                call_command("partner_order_deliver_details",delta=delta)

        except Exception,e:
            print e

        print "完成初始化数据!"
        InfoLogger.info("完成初始化数据!")