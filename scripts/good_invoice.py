#!/usr/bin/env python
#coding=utf-8
import sys
sys.path.append("/home/dhui100/develop/")
# python /home/dhui100/develop/ods/scripts/good_invoice.py

import ods.clients.report_client as report_client
import ods.utils as utils

if __name__ == "__main__":
    filename = utils.get_invoice_report_name()
    xlsx_reporter = report_client.Xlsx_Reporter(filename=filename)
    xlsx_reporter.report_invoice_xlsx()
    print "生成：%s" % filename
