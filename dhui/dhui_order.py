#coding=utf-8

import pdb
import sys
sys.path.append("..")
import odoo_dock
import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings
from bson.objectid import ObjectId
import datetime

def import_sale_order_data(*args, **options):
    print "start load dhui sale order...\n"
    coll = mongodb_client.get_coll("DHUI_SaleOrder")
    # order_list = coll.find({"_id":ObjectId("571e45ef006f87607b834180")})
    start_time, end_time = utils.get_report_time()
    order_list = coll.find({
        "pay_time":{"$gte":start_time, "$lte":end_time},
        "order_status":1,
        "order_goods.goods_type":{"$nin":["goldbean","profit","indiana_count"]}})

    for order in order_list:

        order_id = str(order["_id"])
        # 普通客户
        partner_id = settings.COMMON_CUSTOMER_ID
        amount_total = order["goods_amount"]
        state = "draft"
        # state = "manual"
        # state = "progress"

        sale_order_obj = dict(
            _id=order_id,
            partner_id=partner_id,
            partner_invoice_id=partner_id,
            partner_shipping_id=partner_id,
            amount_total=amount_total,
            state=state,
            # 东汇进销存管理员
            user_id=settings.DHUI_MANAGER_USER_ID,
            order_customer_id = order["user_id"],
            order_address_id = order["address_id"],
            order_purchase_time = order["pay_time"],
        )
        query_params = dict(
            _id=order_id,
            user_id=settings.DHUI_MANAGER_USER_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], sale_order_obj)
        else:
            utils.load_obj(xmlrpcclient, sale_order_obj)

    print "load complete !"

def get_sale_order_list(*args,**kwargs):
    start_time , end_time = utils.get_report_time()
    extra_query_params = dict(
        start_time = ("order_purchase_time",">=",start_time),
        end_tme = ("order_purchase_time","<=",end_time),
    )
    query_params = dict(
        partner_id=settings.COMMON_CUSTOMER_ID,
        user_id=settings.DHUI_MANAGER_USER_ID,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
    sale_order_list = utils.read_obj(xmlrpcclient,query_params,extra_query_params)
    # print sale_order_list
    return sale_order_list

def get_purchase_order_list(*args,**kwargs):
    start_time, end_time = utils.get_report_time()
    extra_query_params = dict(
        start_time=("create_date",">=", start_time),
        end_time=("create_date","<=", end_time),
    )
    query_params = dict(
        partner_id=settings.DHUI_PARTNER_ID,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("PurchaseOrder")
    purchase_order_list = utils.read_obj(xmlrpcclient, query_params, extra_query_params)
    print purchase_order_list
    return purchase_order_list


if __name__ == "__main__":
    get_sale_order_list()
    get_purchase_order_list()