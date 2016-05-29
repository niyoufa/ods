#coding=utf-8

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import datetime, logging, sys, pdb
pdb.set_trace()
sys.path.append(settings.ODS_PARENT_PATH)
import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol
import ods.clients.mongodb_client as mongodb_client

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "供应商发货单发货明细"

    def handle(self, *args, **options):
        # sale_product_detail_info 订单商品信息明细
        sale_order_list = do.get_sale_order_list()
        sale_product_detail_info = {}
        sale_order_line_list = []
        sale_order_user_info = {}
        for sale_order in sale_order_list :
            sale_order_id = sale_order.id
            sale_order_line_list.extends(dol.get_sale_order_line_list(sale_order_id))
            sale_order_user_info[sale_order_id]["order_customer_id"] = sale_order.order_customer_id
            sale_order_user_info[sale_order_id]["order_address_id"] = sale_order.order_address_id

        for sale_order_line in sale_order_line_list:
            order_id = sale_order_line.order_id
            product_id = sale_order_line.product_id
            query_params = dict(
                id = product_id,
            )
            xmlrpcclient = xml_rpcclient.get_xmlrpcclient("Product")
            if utils.has_obj(xmlrpcclient,query_params):
                product_obj = utils.read_obj(xmlrpcclient,query_params)
                product_tmpl_id = product_obj.product_tmpl_id
            else :
                continue
            query_params = dict(
                id = product_tmpl_id,
            )
            xmlrpcclient = xml_rpcclient.get_xmlrpcclient("ProductTemplate")
            if utils.has_obj(xmlrpcclient,query_params):
                product_template_obj = utils.read_obj(xmlrpcclient,query_params)
            else :
                continue

            if sale_product_detail_info.has_key(product_id):
                sale_product_detail_info[product_id]["product_uom_qty"] += sale_order_line.product_uom_qty
            else :
                sale_product_detail_info[product_id]["product_uom_qty"] = sale_order_line.product_uom_qty
                sale_product_detail_info[product_id]["sku"] = product_template_obj.sku
                sale_product_detail_info[product_id]["user_info"] = sale_order_user_info[order_id]

        # partner_order_deliver_details  采购单商家发货信息明细
        partner_order_deliver_details = {}
        purchase_order_list = do.get_purchase_order_list()
        for purchase_order in purchase_order_list :
            order_id = purchase_order.id
            purchase_order_detail = {}
            purchase_order_detail["basic_info"] = utils.convert_to_dict(purchase_order)
            purchase_order_detail["product_list"] = []
            partner_order_deliver_details[order_id] = purchase_order_detail

            purchase_order_line_list = get_purchase_order_line_list(order_id)
            for purchase_order_line in purchase_order_line_list :
                product_id = purchase_order_line.product_id
                product_detail_info = utils.convert_to_dict(purchase_order_line)
                product_detail_info.update(sale_product_detail_info[product_id])
                purchase_order_detail["product_list"].append(product_detail_info)

        # 持久化商家发货信息明细
        coll = mongodb_utils.get_coll("DHUI_PartnerOrderDeliverDetail")
        coll.insert_one(partner_order_deliver_details)
        print "发货订单明细"
        print  partner_order_deliver_details