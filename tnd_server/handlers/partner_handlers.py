#coding=utf-8

import sys, pdb, json, datetime, pymongo
import sys,pdb

import tornado.web

import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_order as do
import ods.clients.mongodb_client as mongodb_client

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings

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

class OrderPartnerDeliverDetail(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()
        try :
            deliver_id = self.get_argument("deliver_id")
        except Exception,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail = coll.find_one({"_id":utils.create_objectid(deliver_id)})
        if not order_partner_deliver_detail :
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return
        else :
            order_partner_deliver_detail["_id"] = str(order_partner_deliver_detail["_id"])
            result["data"] = order_partner_deliver_detail
        self.write(result)

class OrderPartnerDeliverStatus(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()
        try :
            deliver_id = self.get_argument("deliver_id")
        except Exception,e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail = coll.find_one({"_id": utils.create_objectid(deliver_id)})
        if not order_partner_deliver_detail:
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return
        else:
            deliver_status = order_partner_deliver_detail["deliver_status"]
            result["data"] = dict(
                deliver_status = deliver_status,
            )
        self.write(result)

    def post(self):
        result = utils.init_response_data()
        try:
            deliver_id = self.get_argument("deliver_id")
            deliver_status = self.get_argument("deliver_status")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail = coll.find_one({"_id": utils.create_objectid(deliver_id)})
        if not order_partner_deliver_detail:
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return
        else:
            deliver_status = int(deliver_status)
            if deliver_status == 0 :# 取消发货
                pass

            elif deliver_status == 1 :# 发货
                create_time = order_partner_deliver_detail["create_time"]
                curr_time = utils.get_curr_time()
                if curr_time.split(" ")[0] <= create_time.split(" ")[0]:
                    result = utils.reset_response_data(status.Status.ERROR, error_info="当前不可发货,请联系后端开发人员！")
                    self.write(result)
                    return
                else:
                    deliver_result = self.__deliver(order_partner_deliver_detail)
                    if deliver_result["success"] != status.Status.OK:
                        result = deliver_result
                        self.write(result)
                        return
                    else:
                        # 不做处理
                        pass

            else :
                result = utils.reset_response_data(status.Status.ERROR)
                self.write(result)
                return
            #更新发货单
            order_partner_deliver_detail["deliver_status"] = deliver_status
            try :
                coll.save(order_partner_deliver_detail)
            except Exception,e:
                result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))
                self.write(result)
                return

        self.write(result)

    # 发货
    def __deliver(self,*args,**options):
        result = utils.init_response_data()
        order_partner_deliver_detail = args[0]
        create_time = order_partner_deliver_detail["create_time"]
        start_time , end_time = utils.get_date_time(create_time)
        try :
            # 更新mongodb中订单状态
            coll = mongodb_client.get_coll("DHUI_SaleOrder")
            query_params = {
            "pay_time":{"$gte":start_time, "$lte":end_time},
            "order_status":1, # 订单已支付
            "order_goods.goods_type":{"$nin":["goldbean","profit","indiana_count"]}}
            update_params = {
                "$set" : {
                    "deliver_status":3,# 订单已完成
                }
            }
            coll.update(query_params,update_params)
        except Exception ,e :
            result = utils.reset_response_data(status.Status.ERROR,error_info=str(e))

        try :
            # 更新odoo中订单状态
            do.update_sale_order_status(start_time,end_time)
        except Exception ,e :
            result = utils.reset_response_data(status.Status.ERROR,error_info=str(e))

        return result

    # 取消发货
    def __cancel_deliver(self,*args,**options):
        pass

handlers = [
    (r"/odoo/api/good_partner",GoodPartner),
    (r"/odoo/api/order_partner_deliver_detail_list",OrderPartnerDeliverDetailList),
    (r"/odoo/api/order_partner_deliver_detail/get",OrderPartnerDeliverDetail),
    (r"/odoo/api/order_partner_deliver_status/get",OrderPartnerDeliverStatus),
    (r"/odoo/api/order_partner_deliver_status/post",OrderPartnerDeliverStatus),
]


