#coding=utf-8

import sys,pdb
import datetime,logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.clients.report_client as report_client

import ods.dhui.dhui_shipping as ds

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入用户数据到odoo"

    def handle(self, *args, **options):
        print ""
        print "开始导出物流单..."
        InfoLogger.info("开始导出物流单...")

        report_shipping()

        print "完成导出物流单！"
        InfoLogger.info("完成导出物流单！")




def __get_data(*args ,**options):
    columns = []
    data_set = []
    shipping_list = ds.get_shippping_data()
    columns = [u'物流单编号' ,u'物流公司' ,u'编号' ,u'创建时间']
    if len(shipping_list):
        for shipping in shipping_list:
            data_set.append([
                shipping['_id'],
                shipping['company'],
                shipping['number'],
                shipping['add_time'],
            ])
            track = shipping['track']
            orders = shipping['orders']

    print "表头:"
    print columns
    print "表体:"
    print data_set
    return columns, data_set

# 每日生成发货单xlsx报表到指定目录
def report_shipping():
    columns, data_set = __get_data()
    xlsx_reporter = report_client.Xlsx_Reporter(filename="物流单")
    worksheet = xlsx_reporter.get_worksheet()
    xlsx_reporter.export_xlsx(columns=columns ,data_set=data_set ,worksheet=worksheet)