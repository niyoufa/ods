#coding=utf-8

import pdb
import sys

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

free_trade_goods = ["575e6e1f09a0574776a2b226","574d0bf8006f875336deda8c","5761624c09a0570e49af74c3"]

def import_product_template_data(*args, **options):
    coll = mongodb_client.get_coll("DHUI_Product")
    partner_coll = mongodb_client.get_coll("DHUI_Partner")
    print ""
    print "update dhui product...\n"

    partner_list = partner_coll.find()
    partner_dict = {}
    for partner in partner_list :
        partner_type = partner["type"]
        partner_dict[partner_type] = {}
        dic = {}
        dic["dhui_user_id"] = partner["dhui_user_id"]
        dic["partner_id"] = partner["partner_id"]
        partner_dict[partner_type] = dic

    good_list = coll.find()
    log_result = []
    for good in good_list:
        sku = good["sku"]
        goods_name = good["goods_name"]
        box_name = good["box_name"]
        goods_brief = good["goods_brief"]
        shop_price = good["shop_price"]
        goods_name = box_name + goods_brief
        good_id = utils.objectid_str(good["_id"])

        # partner dhui user id
        if good["goods_type"] in ["seckill","normal"]:
            dhui_user_id = partner_dict[good["goods_type"]]["dhui_user_id"]
            partner_id = partner_dict[good["goods_type"]]["partner_id"]
        elif good_id in free_trade_goods :
            dhui_user_id = partner_dict["other"]["dhui_user_id"]
            partner_id = partner_dict["other"]["partner_id"]
        else:
            dhui_user_id = partner_dict["normal"]["dhui_user_id"]
            partner_id = partner_dict["normal"]["partner_id"]

        product_template_obj = dict(
            create_uid = 5,
            sku=sku,
            name=goods_name,
            type="product",
            list_price=shop_price,
            categ_id=settings.PRODUCT_CATEGRAY_ID,
            dhui_user_id = dhui_user_id,
            partner_id = partner_id,
            weight_net = 0.0,
            weight = 0.0,
        )

        query_params = dict(
            sku=sku,
            categ_id=settings.PRODUCT_CATEGRAY_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
        if utils.has_obj(xmlrpcclient, query_params):
            #continue
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
