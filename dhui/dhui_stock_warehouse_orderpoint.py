#coding=utf-8

# 重订货规则

import pdb
import sys

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def update_stock_warehouse_orderpoint(*args,**options):
    coll = mongodb_client.get_coll("DHUI_Product")

    print "update stock warehouse order point ...\n"
    good_list = coll.find()
    log_result = []
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

        stock_warehouse_orderpoint_obj = dict(
            location_id=12,
            product_min_qty=1,
            product_id=product_id,
            product_max_qty=0,
        )

        query_params = stock_warehouse_orderpoint_obj
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("StockWarehouseOrderpoint")
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], stock_warehouse_orderpoint_obj)
        else:
            log_result.append(stock_warehouse_orderpoint_obj)
            utils.load_obj(xmlrpcclient, stock_warehouse_orderpoint_obj)
    return log_result

if __name__ == "__main__":
    update_stock_warehouse_orderpoint()