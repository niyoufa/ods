#coding=utf-8

import datetime, logging, sys, pdb

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol
import ods.dhui.dhui_product_template as dpt
import ods.clients.mongodb_client as mongodb_client
import ods.clients.xmlrpc_client as xml_rpcclient
import ods.utils as utils

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "供应商发货单发货明细"

    def handle(self, *args, **options):
        print ""
        print "开始创建或更新供应商发货单发货明细... 日期：%s"%str(utils.get_report_date()).split(" ")[0]
        InfoLogger.info("开始创建或更新供应商发货单发货明细... 日期：%s"%str(utils.get_report_date()).split(" ")[0])
        print ""
        # sale_product_detail_info 订单商品信息明细
        sale_order_list = do.get_sale_order_list()
        sale_order_line_dict = {}
        sale_order_user_dict = {}
        sale_order_count = 0
        for sale_order in sale_order_list :
            sale_order_id = sale_order["id"]
            sale_order_line_dict[sale_order_id] = dol.get_sale_order_line_list(sale_order_id)

            order_customer_id = sale_order["order_customer_id"]
            order_address_id = sale_order["order_address_id"]
            sale_order_user_dict[sale_order_id] = dict(
                order_customer_id = order_customer_id,
                order_address_id = order_address_id,
            )
            sale_order_count += 1

        # sale_product_detail_info 采购单明细
        sale_product_detail_info = {}
        for order_id in sale_order_line_dict :
            sale_order_line_list = sale_order_line_dict[order_id]
            sale_order_user_info = sale_order_user_dict[order_id]
            order_customer_id = sale_order_user_info["order_customer_id"]
            order_address_id = sale_order_user_info["order_address_id"]

            customer_coll = mongodb_client.get_coll("DHUI_User")
            address_coll = mongodb_client.get_coll("DHUI_Address")
            customer = utils.get_customer(customer_coll,order_customer_id)
            address = utils.get_address(address_coll,order_address_id)

            for sale_order_line in sale_order_line_list:
                temp_user_info = {}

                product_id, product_name = tuple(sale_order_line["product_id"])
                product_uom_qty = sale_order_line["product_uom_qty"]

                product_template_obj = dpt.get_product_template_by_id(product_id=product_id)
                if not product_template_obj :
                    continue
                sku = product_template_obj["sku"]
                name = product_template_obj["name"]
                partner_id = product_template_obj["dhui_user_id"]
                if sale_product_detail_info.has_key(product_id):
                    sale_product_detail_info[product_id]["total_count"] += product_uom_qty
                else :
                    sale_product_detail_info[product_id] = {}
                    sale_product_detail_info[product_id]["total_count"] = product_uom_qty
                    sale_product_detail_info[product_id]["partner_id"] = partner_id
                    sale_product_detail_info[product_id]["sku"] = sku
                    sale_product_detail_info[product_id]["name"] = name
                    sale_product_detail_info[product_id]["user_info"] = []

                if temp_user_info.has_key(order_customer_id):
                    temp_user_info[order_customer_id]["count"] += 1
                else:
                    temp_user_info[order_customer_id] = dict(
                        product_id=product_id,
                        partner_id=partner_id,
                        user_id=order_customer_id,
                        address_id=order_address_id,
                        count=1
                    )

                temp_user_info[order_customer_id].update(customer)
                temp_user_info[order_customer_id].update(address)

                # user_info
                for order_customer_id in temp_user_info :
                    good_user_info = temp_user_info[order_customer_id]
                    sale_product_detail_info[product_id]["user_info"].append(good_user_info)

        temp_sale_product_detail_info = []
        for product_id in sale_product_detail_info :
            sale_product_detail = sale_product_detail_info[product_id]
            temp_sale_product_detail_info.append(sale_product_detail)
        sale_product_detail_info = temp_sale_product_detail_info

        # partner_order_deliver_details  商家发货信息明细
        partner_order_deliver_details = {}
        for sale_product_detail in sale_product_detail_info :
            partner_id = sale_product_detail["partner_id"]
            if partner_order_deliver_details.has_key(partner_id):
                partner_order_deliver_details[partner_id]["detail_info"].append(sale_product_detail)
            else :
                partner_order_deliver_details[partner_id] = dict(
                    partner_id = partner_id,
                    detail_info = [sale_product_detail]
                )
        # 持久化商家发货信息明细
        start_time, end_time = utils.get_report_time()
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")

        flag = None
        for partner_id in partner_order_deliver_details:
            partner_order_deliver_detail = partner_order_deliver_details[partner_id]
            curr_time = str(utils.get_report_date()).split(" ")[0] + " 01:00:00"
            alter_time = str(utils.get_curr_time())
            result = coll.find_one({"partner_id":partner_id,"create_time":{"$gte":start_time,"$lte":end_time}})
            if not result :
                partner_order_deliver_detail.update(dict(
                    create_time = curr_time,
                    alter_time = curr_time,
                    deliver_status = 0,# stastus 0:为发货 1:已发货
                    sale_order_count = sale_order_count,
                ))
                coll.insert_one(partner_order_deliver_detail)

                flag = False

                print "创建发货订单明细"
                print  partner_order_deliver_detail
            else :
                partner_order_deliver_detail.update(dict(
                    _id = result["_id"],
                    create_time = result["create_time"],
                    alter_time = alter_time,
                    deliver_status = result["deliver_status"],
                    partner_id = result["partner_id"],
                    sale_order_count = sale_order_count
                ))
                coll.update({"_id":result["_id"]},partner_order_deliver_detail)

                flag = True

                print "更新发货订单明细"
                InfoLogger.info("更新发货订单明细")
                print partner_order_deliver_detail

        if flag == True :
            print "完成创建供应商发货单发货明细..."
            InfoLogger.info("完成创建供应商发货单发货明细...")
            print ""
        elif flag == False :
            print "完成更新供应商发货单发货明细..."
            InfoLogger.info("完成更新供应商发货单发货明细...")
            print ""
        else :
            print "当前没有发货信息..."
            InfoLogger.info("当前没有发货信息...")
            print ""

