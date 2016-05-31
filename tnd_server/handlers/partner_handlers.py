#coding=utf-8

import sys, pdb, json, datetime, pymongo

import tornado.web
import status
import utils
import settings

import sys,pdb
sys.path.append(settings.ODS_PARENT_PATH)
import ods.dhui.dhui_product_template as dpt
import ods.clients.mongodb_client as mongodb_client


class GoodPartner(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()

        try :
            sku = self.get_argument("sku")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        good = dpt.get_product_template(sku=sku)
        if not good :
            result = utils.reset_response_data(status.Status.ERROR, error_info=str("query error,good not exist"))
            self.write(result)
            return
        else :
            partner_id = good["dhui_user_id"]
        result["data"]["partner_id"] = partner_id
        self.write(result)


class OrderPartnerDeliverDetailList(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()
        try:
            start_time = self.get_argument("start_time")
            end_time = self.get_argument("end_time")
            start_time = start_time.split(".")[0]
            end_time = end_time.split(".")[0]
            partner_id = self.get_argument("partner_id")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail_list = coll.find({"partner_id":partner_id,"create_time":{"$gte":start_time,"$lte":end_time}})
        result["data"]["deliver_list"] = []
        for order_partner_deliver_detail in order_partner_deliver_detail_list:
            order_partner_deliver_detail["_id"] = str(order_partner_deliver_detail["_id"])
            result["data"]["deliver_list"].append(order_partner_deliver_detail)
        self.write(result)

handlers = [
    (r"/odoo/api/good_partner",GoodPartner),
    (r"/odoo/api/order_partner_deliver_detail",OrderPartnerDeliverDetailList),
]


