#coding=utf-8

import pdb, sys, datetime,json
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings


def import_good_invoice(*args,**options):
    start_time, end_time = utils.get_report_time(delta=options.get("delta",0))
    coll = mongodb_client.get_coll("DHUI_PartnerGoodDeliverDetail")
    query_params = {
        "create_time" : {"$gte":start_time,"$lte":end_time}
    }
    partner_order_deliver_detail_list = coll.find(query_params)
    log_result = []
    for partner_order_deliver_detail in partner_order_deliver_detail_list :

        _id = utils.objectid_str(partner_order_deliver_detail["_id"])
        create_time = partner_order_deliver_detail["create_time"]
        sale_order_count = partner_order_deliver_detail["sale_order_count"]
        partner_id = partner_order_deliver_detail["partner_id"]
        deliver_status = partner_order_deliver_detail["deliver_status"]
        invoice_detail_info = partner_order_deliver_detail["detail_info"]

        invoice_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiInvoice")
        purchase_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiPurchase")
        purchase_user_line_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiPurchaseUserLine")

        user_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiUser")
        product_template_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")

        if settings.DHUI_PARTNER_DICT.has_key(partner_id):
            odoo_partner_id = settings.DHUI_PARTNER_DICT[partner_id][1]
        else :
            return

        query_params = dict(
            _id = _id
        )
        dhui_invoice_obj = dict(
            _id = _id,
            create_time = create_time,
            sale_order_count = sale_order_count,
            partner_id = odoo_partner_id,
            deliver_status = deliver_status,
        )
        try :
            if utils.has_obj(invoice_xmlrpcclient, query_params):
                result = invoice_xmlrpcclient.search(query_params)
                invoice_id = result[0]
                invoice_xmlrpcclient.update(result[0], dhui_invoice_obj)
            else:
                invoice_id = utils.load_obj(invoice_xmlrpcclient, dhui_invoice_obj)
        except Exception ,e:
            return
        for purchase_obj in invoice_detail_info:
            sku = purchase_obj["sku"]
            total_count = purchase_obj["total_count"]
            partner_id = purchase_obj["partner_id"]
            name = purchase_obj["name"]
            purchase_user_info = purchase_obj["user_info"]

            query_params = dict(
                sku = sku,
                name = name,
                partner_id = odoo_partner_id,
                invoice_id = invoice_id,
            )
            dhui_purchase_obj = dict(
                sku=sku,
                name=name,
                partner_id= odoo_partner_id,
                invoice_id= invoice_id,
                total_count = total_count,
            )

            try :
                if utils.has_obj(purchase_xmlrpcclient, query_params):
                    result = purchase_xmlrpcclient.search(query_params)
                    purchase_id = result[0]
                    purchase_xmlrpcclient.update(result[0], dhui_purchase_obj)
                else:
                    purchase_id = utils.load_obj(purchase_xmlrpcclient, dhui_purchase_obj)
            except Exception,e :
                continue
            for user_info in purchase_user_info :
                count = user_info["count"]
                product_id = user_info["product_id"]
                user_id = user_info["user_id"]

                try:
                    query_params = dict(
                        user_id=user_id
                    )
                    if utils.has_obj(user_xmlrpcclient, query_params):
                        result = user_xmlrpcclient.search(query_params)
                    else:
                        continue
                    odoo_user_id = result[0]
                except Exception, e:
                    continue

                query_params = dict(
                    user_id = odoo_user_id,
                    product_id = product_id,
                    purchase_id = purchase_id,
                )
                dhui_purchase_user_info_obj = dict(
                    user_id=odoo_user_id,
                    product_id=product_id,
                    purchase_id=purchase_id,
                    count = count,
                )
                try :
                    if utils.has_obj(purchase_user_line_xmlrpcclient,query_params):
                        result = purchase_user_line_xmlrpcclient.search(query_params)
                        purchase_user_line_xmlrpcclient.update(result[0],dhui_purchase_user_info_obj)
                    else:
                        utils.load_obj(purchase_user_line_xmlrpcclient, dhui_purchase_user_info_obj)
                except Exception ,e :
                    print e
                    continue
        log_result.append(partner_order_deliver_detail)

    return log_result

def get_good_invoice_data(*args,**options):
    start_time, end_time = utils.get_report_time(delta=options.get("delta", 0))
    # coll = mongodb_client.get_coll("DHUI_PartnerGoodDeliverDetail")
    # query_params = {
    #     # "create_time": {"$gte": start_time, "$lte": end_time}
    # }

    # partner_good_deliver_detail_list = coll.find(query_params)
    # for partner_good_deliver_detail in partner_good_deliver_detail_list:
    #     _id = utils.objectid_str(partner_good_deliver_detail["_id"])
    #     create_time = partner_good_deliver_detail["create_time"]
    #     sale_order_count = partner_good_deliver_detail["sale_order_count"]
    #     partner_id = partner_good_deliver_detail["partner_id"]
    #     deliver_status = partner_good_deliver_detail["deliver_status"]
    #     invoice_detail_info = partner_good_deliver_detail["detail_info"]
    #     if settings.DHUI_PARTNER_DICT.has_key(partner_id):
    #         odoo_partner_id = settings.DHUI_PARTNER_DICT[partner_id][1]
    #     else:
    #         return
    #
    #     dhui_invoice_obj = dict(
    #         _id=_id,
    #         create_time=create_time,
    #         sale_order_count=sale_order_count,
    #         partner_id=odoo_partner_id,
    #         deliver_status=deliver_status,
    #     )
    #
    #     good_invoice_data.append(dhui_invoice_obj)

    invoice_xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiInvoice")
    extra_query_params = dict(
        start_time=("create_time", ">=", start_time),
        end_tme=("create_time", "<=", end_time),
    )
    query_params = {}
    good_invoice_list = utils.read_obj(invoice_xmlrpcclient, query_params, extra_query_params)

    good_invoice_data = []
    for good_invoice in good_invoice_list :
        good_invoice_data.append(dict(
            _id=good_invoice["_id"],
            create_time=good_invoice["create_time"],
            partner_id=good_invoice["partner_id"][1],
            deliver_status=u'未发货' if good_invoice["deliver_status"] == False else u'已发货'
        ))
    return good_invoice_data

if __name__ == "__main__":
    import_good_invoice()