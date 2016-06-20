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
        # "pay_time":{"$gte":start_time, "$lte":end_time},
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
        except Exception,e :
            pass

        # 普通客户
        partner_id = settings.COMMON_CUSTOMER_ID
        amount_total = order["goods_amount"]
        add_time = order["add_time"]
        # state = "draft" # 报价单
        state = "manual" # 销售订单

        _id = utils.objectid_str(order["_id"])
        address_id = order["address_id"]
        goldbean = order["goldbean"]
        pay_time = order["pay_time"]
        promotion_id = order["promotion_id"]
        contact_name = order["contact_name"]
        receive_wx_notify = order["receive_wx_notify"]
        pay_type = str(order["pay_type"])
        customer_user_id = order["user_id"]
        goods_amount = order["goods_amount"]
        order_status = str(order["order_status"])
        pay_status = str(order["pay_status"])
        money_paid = order["money_paid"]
        order_id = order["order_id"]
        origin_code = order["origin_code"]
        discount = order["discount"]
        shipping_status = str(order["shipping_status"])
        order_invoice = str(order["order_invoice"])
        add_time = str(order["add_time"])
        delivery_time = order["delivery_time"]
        remark = order["remark"]
        mobile = order["mobile"]
        order_goods = order["order_goods"]
        edit_times = order["edit_times"]
        shipping_fee = order["shipping_fee"]

        sale_order_obj = dict(

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
            #东汇订单信息
            _id= _id,
            address_id = address_id,
            goldbean = goldbean,
            pay_time = pay_time ,
            promotion_id = promotion_id,
            contact_name = contact_name,
            receive_wx_notify = receive_wx_notify,
            pay_type = pay_type,
            customer_user_id = customer_user_id,
            goods_amount = goods_amount,
            order_status = order_status,
            pay_status = pay_status,
            money_paid = money_paid,
            order_id = order_id,
            origin_code = origin_code,
            discount = discount,
            shipping_status = shipping_status,
            order_invoice = order_invoice,
            add_time = add_time,
            delivery_time = delivery_time,
            remark = remark,
            mobile = mobile,
            order_goods = order_goods,
            edit_times = edit_times,
            shipping_fee = shipping_fee,
        )

        #订单发货地址
        order_address = order["order_address"]
        if order["address_id"] :
            address = {
                'contact_name':order_address.get("contact_name",""),
                'contact_mobile':order_address.get("contact_mobile",""),
                'area':order_address.get("area",""),
                'city':order_address.get("city",""),
                'district':order_address.get("district",""),
                'remark':order_address.get("remark",""),
                'detailed_address':order_address.get("detailed_address",""),
                'lng':order_address.get("lng",""),
                'lat':order_address.get("lat",""),
                'add_time':order_address.get("add_time",""),
                'mod_time':order_address.get("mod_time",""),
                'is_default_flag':order_address.get("is_default_flag",""),
                'order_id':order_id,
            }
            query_params = dict(
                order_id= order_id,
            )
            sale_order_address_obj = address

            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrderAddress")
            if utils.has_obj(xmlrpcclient,query_params):
                result = xmlrpcclient.search(query_params)
                order_address_id = result[0]
            else :
                order_address_id = utils.load_obj(xmlrpcclient,sale_order_address_obj)
            sale_order_obj["odoo_address_id"] = order_address_id
        else :
            pass

        query_params = dict(
            order_id=order_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        if utils.has_obj(xmlrpcclient, query_params):
            # continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], sale_order_obj)
            sale_order_id = result[0]
        else:
            sale_order_id = utils.load_obj(xmlrpcclient, sale_order_obj)

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
