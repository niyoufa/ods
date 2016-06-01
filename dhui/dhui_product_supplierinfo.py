#coding=utf-8

# 商品供应商

import pdb
import sys

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings


def update_product_supplierinfo(*args,**options):
    coll = mongodb_client.get_coll("DHUI_Product")

    print "start update product supplierinfo ...\n"

    good_list = coll.find()
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
            print "continue\n"
            continue

        product_supplierinfo_obj = dict(
            # 东汇其他供应商
            name=settings.DHUI_PARTNER_ID,
            min_qty=1,
            product_tmpl_id=product_template_id,
            # dhui100 user_id
            # dhui_user_id = "571dbf0c006f874b52b126aa",
        )

        query_params = dict(
            product_tmpl_id=product_template_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductSupplierInfo")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], product_supplierinfo_obj)
        else:
            utils.load_obj(xmlrpcclient, product_supplierinfo_obj)

if __name__ == "__main__":
    update_product_supplierinfo()