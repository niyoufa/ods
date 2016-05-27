#coding=utf-8

# order and good map

import pdb
import sys
sys.path.append("..")
import odoo_dock
import odoo_dock.xmlrpc_client as xmlrpc_client
import odoo_dock.mongodb_utils as mongodb_utils
import odoo_dock.utils as utils
import odoo_dock.settings as settings
from bson.objectid import ObjectId

def import_sale_order_line(*args,**options):
    print "start insert...\n"
    coll = mongodb_utils.get_coll("DHUI_SaleOrder")
    # order_list = coll.find({"order_status": 0})[0:1]
    order_list = coll.find({"_id": ObjectId("571e45ef006f87607b834180")})
    for order in order_list:
        order_id = str(order["_id"])
        query_params = dict(
            _id=order_id,
            user_id=11,
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

if __name__ == "__main__":
    import_sale_order_line()