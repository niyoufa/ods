#coding=utf-8

import sys,pdb
import datetime,logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from optparse import make_option

import ods.clients.report_client as report_client

import ods.dhui.dhui_invoice as di

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "导入用户数据到odoo"

    def handle(self, *args, **options):
        print ""
        print "开始导出商品发货单..."
        InfoLogger.info("开始导出商品发货单...")

        report_invoice()

        print "完成导出商品发货单！"
        InfoLogger.info("完成导出商品发货单！")




def __data(*args ,**options):
    columns = []
    data_set = []
    invoice_data = di.get_good_invoice_data(delta=1)
    columns = [u'发货单编号' ,u'创建时间' ,u'供应商' ,u'发货单状态']
    if len(invoice_data):
        for invoice in invoice_data:
            data_set.append([
                invoice['_id'],
                invoice['create_time'],
                invoice['partner_id'],
                invoice['deliver_status'],
            ])

    print "表头:"
    print columns
    print "表体:"
    print data_set
    return columns, data_set

# 每日生成发货单xlsx报表到指定目录
def report_invoice():
    columns, data_set = __data()
    xlsx_reporter = report_client.Xlsx_Reporter(filename="物流单")
    worksheet = xlsx_reporter.get_worksheet()
    xlsx_reporter.export_xlsx(columns=columns ,data_set=data_set ,worksheet=worksheet)