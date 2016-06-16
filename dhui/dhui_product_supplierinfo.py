#coding=utf-8

# 商品供应商

import pdb
import sys

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

free_trade_goods = ["575e6e1f09a0574776a2b226","574d0bf8006f875336deda8c","5761624c09a0570e49af74c3"]

def update_product_supplierinfo(*args,**options):
    coll = mongodb_client.get_coll("DHUI_Product")

    print "update product supplierinfo ...\n"

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
            print "continue\n"
            continue

        # partner dhui user id
        if good["goods_type"] == settings.DHUI_PARTNER_DICT["seckill"][2]:
            dhui_user_id = settings.DHUI_PARTNER_DICT["seckill"][1]
        else:
            dhui_user_id = settings.DHUI_PARTNER_DICT["default"][1]

        good_id = utils.objectid_str(good["_id"])
        if good_id in free_trade_goods :
            dhui_user_id = settings.DHUI_PARTNER_DICT["other"][1]

        product_supplierinfo_obj = dict(
            # 东汇商城供应商
            name = dhui_user_id,
            min_qty=1,
            product_tmpl_id=product_template_id,
        )

        query_params = dict(
            product_tmpl_id=product_template_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductSupplierInfo")
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], product_supplierinfo_obj)
        else:
            log_result.append(product_supplierinfo_obj)
            utils.load_obj(xmlrpcclient, product_supplierinfo_obj)
    return log_result

if __name__ == "__main__":
    update_product_supplierinfo()