#coding=utf-8

import pdb, sys, datetime
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

# state
# ('draft', 'Draft Quotation'),
# ('sent', 'Quotation Sent'),
# ('cancel', 'Cancelled'),
# ('waiting_date', 'Waiting Schedule'),
# ('progress', 'Sales Order'),
# ('manual', 'Sale to Invoice'),
# ('shipping_except', 'Shipping Exception'),
# ('invoice_except', 'Invoice Exception'),
# ('done', 'Done'),

def import_sale_order_data(*args, **options):
    coll = mongodb_client.get_coll("DHUI_SaleOrder")
    start_time, end_time = utils.get_report_time(delta=options.get("delta",0))
    order_list = coll.find({
        "pay_time":{"$gte":start_time, "$lte":end_time},
        "order_status":1,
        "order_goods.goods_type":{"$nin":["goldbean","profit","indiana_count"]}})
    order_log_result = []
    for order in order_list:
        order_log_result.append(order)

        try :
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiUser")
            user_id = order["user_id"]
            query_params = dict(
                user_id = user_id,
            )
            result = xmlrpcclient.search(query_params)
            dhui_user_id = result[0]
        except Exception ,e:
            continue

        order_id = str(order["_id"])
        # 普通客户
        partner_id = settings.COMMON_CUSTOMER_ID
        amount_total = order["goods_amount"]
        add_time = order["add_time"]
        # state = "draft" # 报价单
        state = "manual" # 销售订单

        sale_order_obj = dict(
            _id=order_id,
            partner_id=partner_id,
            partner_invoice_id=partner_id,
            partner_shipping_id=partner_id,
            amount_total=amount_total,
            state=state,
            date_order = add_time,
            # 东汇进销存管理员
            user_id=settings.DHUI_MANAGER_USER_ID,
            dhui_user_id = dhui_user_id,
            order_customer_id = user_id,
            order_address_id = order["address_id"],
            order_purchase_time = order["pay_time"],
        )
        query_params = dict(
            _id=order_id,
            user_id=settings.DHUI_MANAGER_USER_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        if utils.has_obj(xmlrpcclient, query_params):
            # continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], sale_order_obj)
        else:
            utils.load_obj(xmlrpcclient, sale_order_obj)

    return order_log_result

def get_sale_order_list(*args,**kwargs):
    start_time , end_time = utils.get_report_time(datetime.datetime.now(),delta=kwargs.get("delta",0))
    extra_query_params = dict(
        start_time = ("order_purchase_time",">=",start_time),
        end_tme = ("order_purchase_time","<=",end_time),
        state=("state", "=", "manual"),
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
    start_time, end_time = utils.get_report_time(delta=kwargs.get("delta",0))
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

def update_sale_order_status(*args,**kwargs):
    start_time = args[0]
    end_time = args[1]
    extra_query_params = dict(
        start_time=("order_purchase_time", ">=", start_time),
        end_tme=("order_purchase_time", "<=", end_time),
        state=("state", "=", "manual"),
    )
    query_params = dict(
        partner_id=settings.COMMON_CUSTOMER_ID,
        user_id=settings.DHUI_MANAGER_USER_ID,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
    sale_order_list = utils.get_order_list(xmlrpcclient, query_params, extra_query_params)
    obj_list = []
    for sale_order in sale_order_list:
        obj_list.append(dict(
            id=sale_order["id"],
            alter_params=dict(
                state="done",
            )
        ))
    utils.update_obj_list(xmlrpcclient, obj_list)

if __name__ == "__main__":
    import_sale_order_data()