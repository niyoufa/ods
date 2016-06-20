#coding=utf-8

import pdb
from django.shortcuts import render

import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_product_supplierinfo as dps
import ods.dhui.dhui_stock_warehouse_orderpoint as dpwo

import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol

import ods.clients.mongodb_client as mongodb_client

import ods.utils  as utils
import ods.dj_server.dj_server.status as status

def create_dhui_invoice(request):
    result = utils.init_response_data()
    try :
        deliver_details = utils.manual_create_invoice(dpt=dpt, dps=dps, dpwo=dpwo, do=do, dol=dol,mongodb_client=mongodb_client)
    except Exception,e:
        result["success"] = status.Status.ERROR
        trace_info = ""
        result["return_code"] = status.Status().getReason(result["success"] + str(e))
        return result
    result["data"] = deliver_details
    return result
