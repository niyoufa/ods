#coding=utf-8

import sys, pdb, json, datetime, pymongo, urllib

import tornado.web
from tornado.httpclient import AsyncHTTPClient

import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol
import ods.dhui.dhui_product_template as dpt
import ods.dhui.dhui_product_supplierinfo as dps
import ods.dhui.dhui_stock_warehouse_orderpoint as dpwo
import ods.clients.mongodb_client as mongodb_client

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings
import ods.tnd_server.handler as handler

# 商品发货明细
class GoodPartnerDeliverDetailList(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()
        try:
            start_time = self.get_argument("start_time")
            end_time = self.get_argument("end_time")
            start_time = start_time.split(" ")[0] + " " + "00:00:00"
            end_time = end_time.split(" ")[0] + " " + "59:59:59"
            partner_id = self.get_argument("partner_id")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail_list = coll.find(
            {"partner_id":partner_id,"create_time":{"$gte":start_time,"$lte":end_time}},
            sort=[("create_time",-1)],
        )
        result["data"]["deliver_list"] = []
        for order_partner_deliver_detail in order_partner_deliver_detail_list:
            order_partner_deliver_detail["_id"] = str(order_partner_deliver_detail["_id"])
            result["data"]["deliver_list"].append(order_partner_deliver_detail)
        self.write(result)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        client = AsyncHTTPClient()
        query_params = dict(
            action = "create_dhui_invoice",
            data = {}
        )
        data = urllib.urlencode(query_params)
        response = yield tornado.gen.Task(client.fetch,
          settings.ODS_ADDRESS + settings.DHUI_URL_PREFIX + data)
        try :
            data = json.loads(response.body)
            print data
            if not data["success"] == status.Status.OK:
                self.write(data)
                self.finish()
        except Exception,e :
            trace_info = utils.get_trace_info()
            result = utils.reset_response_data(status.Status.ERROR, error_info=str(trace_info))
            self.write(result)
            self.finish()

        result["data"] = data["data"]
        self.write(result)
        self.finish()

class OrderPartnerDeliverCreate(tornado.web.RequestHandler):
    def get(self):
        import ods.dhui.dhui_product_template as dpt
        import ods.dhui.dhui_product_supplierinfo as dps
        import ods.dhui.dhui_stock_warehouse_orderpoint as dpwo

        import ods.dhui.dhui_order as do
        import ods.dhui.dhui_order_line as dol

        import ods.clients.mongodb_client as mongodb_client

        result = utils.init_response_data()
        try:
            partner_order_deliver_details = utils.manual_create_invoice(dpt=dpt, dps=dps, dpwo=dpwo, do=do, dol=dol,
                                                                        mongodb_client=mongodb_client)
        except Exception, e:
            result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))
            self.write(result)
            self.finish()
            return
        result["return_code"] = "完成创建供应商发货单发货明细!"
        result["data"] = partner_order_deliver_details
        self.write(result)
        self.finish()

class OrderPartner(tornado.web.RequestHandler):
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

class OrderPartnerDeliverDetailList(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()
        try:
            start_time = self.get_argument("start_time")
            end_time = self.get_argument("end_time")
            start_time = start_time.split(" ")[0] + " " + "00:00:00"
            end_time = end_time.split(" ")[0] + " " + "59:59:59"
            partner_id = self.get_argument("partner_id")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail_list = coll.find(
            {"partner_id":partner_id,"create_time":{"$gte":start_time,"$lte":end_time}},
            sort=[("create_time",-1)],
        )
        result["data"]["deliver_list"] = []
        for order_partner_deliver_detail in order_partner_deliver_detail_list:
            order_partner_deliver_detail["_id"] = str(order_partner_deliver_detail["_id"])
            result["data"]["deliver_list"].append(order_partner_deliver_detail)
        self.write(result)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        client = AsyncHTTPClient()
        query_params = dict(
            action = "create_dhui_invoice",
            data = {}
        )
        data = urllib.urlencode(query_params)
        response = yield tornado.gen.Task(client.fetch,
          settings.ODS_ADDRESS + settings.DHUI_URL_PREFIX + data)
        try :
            data = json.loads(response.body)
            print data
            if not data["success"] == status.Status.OK:
                self.write(data)
                self.finish()
        except Exception,e :
            trace_info = utils.get_trace_info()
            result = utils.reset_response_data(status.Status.ERROR, error_info=str(trace_info))
            self.write(result)
            self.finish()

        result["data"] = data["data"]
        self.write(result)
        self.finish()

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

    # 同步发货状态
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        result = utils.init_response_data()
        try:
            deliver_id = self.get_argument("deliver_id")
            deliver_status = self.get_argument("deliver_status")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))

        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail = coll.find_one({"_id": utils.create_objectid(deliver_id)})
        if not order_partner_deliver_detail:
            result = utils.reset_response_data(status.Status.NOT_EXIST)

        else:
            deliver_status = int(deliver_status)
            if deliver_status == 0 :# 取消发货
                pass

            elif deliver_status == 1 :# 发货
                create_time = order_partner_deliver_detail["create_time"]
                curr_time = utils.get_curr_time()
                if curr_time.split(" ")[0] <= create_time.split(" ")[0]:
                    result = utils.reset_response_data(status.Status.ERROR, error_info="当前不可发货,请联系后端开发人员！")
                else:
                    create_time = order_partner_deliver_detail["create_time"]
                    start_time, end_time = utils.get_date_time(create_time)
                    try:
                        # 更新odoo中订单状态
                        do.update_sale_order_status(start_time, end_time)
                    except Exception, e:
                        result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))

                    try:
                        # 更新mongodb中订单状态
                        query_params = {
                            "pay_time": {"$gte": start_time, "$lte": end_time},
                            "order_status": 1,  # 订单已支付
                            "order_goods.goods_type": {"$nin": ["goldbean", "profit", "indiana_count"]}}
                        update_params = {
                            "$set": {
                                "order_status": 3,  # 订单已完成
                            }
                        }
                        # coll = mongodb_client.get_coll("DHUI_SaleOrder")
                        # coll.update_many(query_params,update_params)
                        #response = yield client.fetch(url, method=POST, body=json.dumps(data))
                        client = AsyncHTTPClient()
                        data=dict(
                            coll_name = "order",
                            query_params = json.dumps(query_params),
                            update_params = json.dumps(update_params),
                        )
                        data = urllib.urlencode(data)
                        response = yield tornado.gen.Task(client.fetch,"http://%s/api/odoo?"%settings.DHUI100_ADDRESS + data)
                        try:
                            data = json.loads(response.body)["response"]
                            if not data["success"] == status.Status.OK:
                                self.finish(result)
                            else :
                                # 更新发货单
                                order_partner_deliver_detail["deliver_status"] = deliver_status
                                try:
                                    coll.save(order_partner_deliver_detail)
                                except Exception, e:
                                    result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))
                        except Exception, e:
                            trace_info = utils.get_trace_info()
                            result = utils.reset_response_data(status.Status.ERROR, error_info=str(trace_info))

                    except Exception, e:
                        result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))
            else :
                result = utils.reset_response_data(status.Status.ERROR)

        self.finish(result)

    # 同步发货
    def __deliver(self,*args,**options):
        result = utils.init_response_data()
        order_partner_deliver_detail = args[0]
        create_time = order_partner_deliver_detail["create_time"]
        start_time , end_time = utils.get_date_time(create_time)
        try:
            # 更新odoo中订单状态
            do.update_sale_order_status(start_time, end_time)
        except Exception, e:
            result = utils.reset_response_data(status.Status.ERROR, error_info=str(e))

        # try :
        #     # 更新mongodb中订单状态
        #     query_params = {
        #     "pay_time":{"$gte":start_time, "$lte":end_time},
        #     "order_status":1, # 订单已支付
        #     "order_goods.goods_type":{"$nin":["goldbean","profit","indiana_count"]}}
        #     update_params = {
        #         "$set" : {
        #             "order_status":3,# 订单已完成
        #         }
        #     }
        #     coll = mongodb_client.get_coll("DHUI_SaleOrder")
        #     coll.update_many(query_params,update_params)
        # except Exception ,e :
        #     result = utils.reset_response_data(status.Status.ERROR,error_info=str(e))

    # 取消发货
    def __cancel_deliver(self,*args,**options):
        pass

# 发货订单列表
class PartnerDeliverOrderList(handler.APIHandler):
    def get(self,*args, **kwargs):
        result = utils.init_response_data()
        query_params = {}

        try:
            partner_id = self.get_argument("partner_id",None)
            if not partner_id:
                result = utils.reset_response_data(status.Status.PARMAS_ERROR)
                self.finish(result)
                return

            _start_time = self.get_argument("start_time","")
            _end_time = self.get_argument("end_time","")
            if _start_time and _end_time :
                start_time = _start_time.split(" ")[0] + " " + "00:00:00"
                end_time = _end_time.split(" ")[0] + " " + "59:59:59"
                query_params = {
                    "partner_id": partner_id,
                    "create_time": {"$gte": start_time, "$lte": end_time},
                }
            else :
                query_params = {
                    "partner_id": partner_id,
                }

            _shipping_status = self.get_argument("shipping_status",None)
            if _shipping_status:
                shipping_status = [int(_shipping_status)]
            else :
                shipping_status = [1,10,20,30]
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.finish(result)
            return
        coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
        order_partner_deliver_detail_list = coll.find(
            query_params,
            sort=[("create_time", -1)],
        )
        result["data"] = []
        order_list = []
        for order_partner_deliver_detail in order_partner_deliver_detail_list:
            for order in order_partner_deliver_detail["order_list"]:
                if order['shipping_status'] in shipping_status:
                    order_list.append(order)
        order_list.sort(key=lambda obj: obj["pay_time"])
        order_list.reverse()
        result["data"] = order_list
        self.finish(result)

class PartnerDeliverOrderStatus(handler.APIHandler):
    def post(self, *args, **kwargs):
        result = utils.init_response_data()
        try :
            order_id = self.get_argument("order_id")
            shipping_status = self.get_argument("shipping_status")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR)
            self.finish(result)
            return

        try:
            coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
            query_params = {
                "order_list._id":{
                    "$in":[order_id]
                }
            }

            partner_deliver_order = coll.find_one(query_params)
            index = 0
            for order in partner_deliver_order["order_list"]:
                if order["_id"] == order_id :
                    partner_deliver_order["order_list"][index]["shipping_status"] = int(shipping_status)
                    break
                index += 1
            coll.save(partner_deliver_order)

        except Exception ,e :
            result = utils.reset_response_data(status.Status.ERROR)
            self.finish(result)
            return

        #同步到odoo
        try :
            pass
        except Exception,e:
            print e

        self.finish(result)



handlers = [
    (r"/odoo/api/good_partner",OrderPartner),
    (r"/odoo/api/order_partner_deliver_detail_list",OrderPartnerDeliverDetailList),
    (r"/odoo/api/order_partner_deliver_detail_list/post",OrderPartnerDeliverDetailList),
    (r"/odoo/api/order_partner_deliver_detail/get",OrderPartnerDeliverDetail),
    (r"/odoo/api/order_partner_deliver_status/get",OrderPartnerDeliverStatus),
    (r"/odoo/api/order_partner_deliver_status/post",OrderPartnerDeliverStatus),
    (r"/odoo/api/partner_deliver_order_list",PartnerDeliverOrderList),
    (r"/odoo/api/partner_deliver_order_status/post",PartnerDeliverOrderStatus),
]


