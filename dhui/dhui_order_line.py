#coding=utf-8

# order and good map

import pdb, sys
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings


def import_sale_order_line(*args,**options):
    print "start insert...\n"
    coll = mongodb_client.get_coll("DHUI_SaleOrder")
    # order_list = coll.find({"_id": ObjectId("571e45ef006f87607b834180")})
    start_time, end_time = utils.get_report_time()
    order_list = coll.find({
        "pay_time": {"$gte": start_time, "$lte": end_time},
        "order_status": 1,
        "order_goods.goods_type": {"$nin": ["goldbean", "profit", "indiana_count"]}})
    for order in order_list:
        order_id = str(order["_id"])
        query_params = dict(
            _id=order_id,
            user_id=settings.DHUI_MANAGER_USER_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            sale_order_id = result[0]
        else:
            continue

        good_list = order["order_goods"]
        for good in good_list:
            sku = good["sku"]
            query_params = dict(
                sku=sku,
                categ_id=settings.PRODUCT_CATEGRAY_ID,
            )
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
            if utils.has_obj(xmlrpcclient, query_params):
                result = xmlrpcclient.search(query_params)
                product_template_id = result[0]
            else:
                print "sku=%s:this good is not exist!" % good["sku"]
                continue

            query_params = dict(
                product_tmpl_id=product_template_id,
            )
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("Product")
            if utils.has_obj(xmlrpcclient, query_params):
                result = xmlrpcclient.search(query_params)
                product_id = result[0]
            else:
                continue
            sale_order_line_obj = dict(
                product_id=product_id,
                order_id=sale_order_id,
            )

            query_params = sale_order_line_obj
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrderLine")
            if utils.has_obj(xmlrpcclient, query_params):
                print "Has insert good : (sku)%s" % good["sku"]
                print "\n"
                continue
            else:
                utils.load_obj(xmlrpcclient, sale_order_line_obj)

    print "insert complete !"

def get_sale_order_line_list(order_id):
        query_params = dict(
            order_id = order_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrderLine")
        if utils.has_obj(xmlrpcclient,query_params):
            sale_order_line_list = utils.read_obj(xmlrpcclient,query_params)
            return sale_order_line_list
        else : 
            return []

def get_purchase_order_line_list(order_id):
    query_params = dict(
        order_id = order_id,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("PurchaseOrderLine")
    if utils.has_obj(xmlrpcclient,query_params):
        purhase_order_line_list = utils.read_obj(xmlrpcclient,query_params)
        return purhase_order_line_list
    else : 
        return []

if __name__ == "__main__":
    import_sale_order_line()