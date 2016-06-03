#coding=utf-8

import pdb
import sys

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def import_product_template_data(*args, **options):
    coll = mongodb_client.get_coll("DHUI_Product")

    print ""
    print "update dhui product...\n"

    good_list = coll.find()
    log_result = []
    for good in good_list:
        sku = good["sku"]
        goods_name = good["goods_name"]
        box_name = good["box_name"]
        goods_brief = good["goods_brief"]
        shop_price = good["shop_price"]
        goods_name = box_name + goods_brief

        # partner dhui user id
        if good["goods_type"] == settings.DHUI_PARTNER_DICT["seckill"][2]:
            dhui_user_id = settings.DHUI_PARTNER_DICT["seckill"][0]
        else :
            dhui_user_id = settings.DHUI_PARTNER_DICT["default"][0]
        product_template_obj = dict(
            create_uid = 5,
            sku=sku,
            name=goods_name,
            type="product",
            list_price=shop_price,
            categ_id=settings.PRODUCT_CATEGRAY_ID,
            dhui_user_id = dhui_user_id,
            weight_net = 0.0,
            weight = 0.0,
        )

        query_params = dict(
            sku=sku,
            categ_id=settings.PRODUCT_CATEGRAY_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], product_template_obj)
        else:
            log_result.append(good)
            utils.load_obj(xmlrpcclient, product_template_obj)

        # update good cost
        result = xmlrpcclient.search(query_params)
        res_id = 'product.template,' + str(result[0])
        cost = good["cost"]

        query_params = dict(
            res_id=res_id,
            name='standard_price',
            type='float',
        )

        ir_property_obj = dict(
            value_float=cost,
            name="standard_price",
            type='float',
            company_id=settings.COMPANY_ID,
            res_id=res_id,
            fields_id=2041,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("IrProperty")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], ir_property_obj)
        else:
            utils.load_obj(xmlrpcclient, ir_property_obj)

    return log_result


def get_product_template(*args,**kwargs):
    sku = kwargs["sku"]
    query_params = dict(
        sku = sku,
        categ_id=settings.PRODUCT_CATEGRAY_ID,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
    if utils.has_obj(xmlrpcclient, query_params):
        result = utils.read_obj(xmlrpcclient,query_params)
    else:
        good = None
    return result[0]

def get_product_template_by_id(*args,**kwargs):
    product_id = kwargs["product_id"]
    query_params = dict(
        id = product_id,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("Product")
    if utils.has_obj(xmlrpcclient,query_params):
        [product_obj] = utils.read_obj(xmlrpcclient,query_params)
        product_tmpl_id = tuple(product_obj["product_tmpl_id"])[0]
    else :
        return None
    query_params = dict(
        id = product_tmpl_id,
    )
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
    if utils.has_obj(xmlrpcclient,query_params):
        product_template_obj = utils.read_obj(xmlrpcclient,query_params)
    else :
        return None
    return product_template_obj[0]

if __name__ == "__main__":
    import_product_template_data()