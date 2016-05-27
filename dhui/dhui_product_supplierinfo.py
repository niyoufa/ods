#coding=utf-8

# 商品供应商

import pdb
import sys
sys.path.append("..")
import odoo_dock
import odoo_dock.xmlrpc_client as xmlrpc_client
import odoo_dock.mongodb_utils as mongodb_utils
import odoo_dock.utils as utils
import odoo_dock.settings as settings


def update_product_supplierinfo(*args,**options):
    coll = mongodb_utils.get_coll("DHUI_Product")

    print "start update product supplierinfo ...\n"

    good_list = coll.find()[0:1]
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
            name=90,
            min_qty=1,
            product_tmpl_id=product_template_id,
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