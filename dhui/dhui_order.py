#coding=utf-8

import pdb
import sys
sys.path.append("..")
import odoo_dock
import odoo_dock.xmlrpc_client as xmlrpc_client
import odoo_dock.mongodb_utils as mongodb_utils
import odoo_dock.utils as utils
import odoo_dock.settings as settings
from bson.objectid import ObjectId
import datetime

def import_sale_order_data(*args, **options):
    coll = mongodb_utils.get_coll("DHUI_SaleOrder")
    print "start load dhui sale order...\n"
    # order_list = coll.find({"order_status": 0})
    order_list = coll.find({"_id":ObjectId("571e45ef006f87607b834180")})
    for order in order_list:

        order_id = str(order["_id"])
        # 普通客户
        partner_id = 84
        amount_total = order["goods_amount"]
        state = "draft"

        sale_order_obj = dict(
            _id=order_id,
            partner_id=partner_id,
            partner_invoice_id=partner_id,
            partner_shipping_id=partner_id,
            amount_total=amount_total,
            state=state,
            # 东汇进销存管理员1
            user_id=11,
            order_customer_id = order["user_id"],
            order_address_id = order["address_id"],
            order_purchase_time = str(datetime.datetime.now()).split(".")[0],
        )
        query_params = dict(
            _id=order_id,
            user_id=11,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], sale_order_obj)
        else:
            utils.load_obj(xmlrpcclient, sale_order_obj)

    print "load complete !"

def get_sale_order(*args,**kwargs):
    start_time , end_time = utils.get_report_time()
    extra_query_params = dict(
        start_time = ("order_purchase_time",">=",start_time),
        end_tme = ("order_purchase_time","<=",end_time),
    )
    query_params = dict(
        partner_id=84,
        user_id=11,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
    sale_order_list = utils.read_obj(xmlrpcclient,query_params,extra_query_params)
    print sale_order_list
    return sale_order_list

def get_purchase_order(*args,**kwargs):
    start_time, end_time = utils.get_report_time()
    extra_query_params = dict(
        start_time=("create_time",">=", start_time),
        end_time=("create_time","<=", end_time),
    )
    query_params = dict(
        partner_id=84,
        user_id=11,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
    pdb.set_trace()
    sale_order_list = utils.read_obj(xmlrpcclient, query_params, extra_query_params)
    return sale_order_list


if __name__ == "__main__":
    get_sale_order()