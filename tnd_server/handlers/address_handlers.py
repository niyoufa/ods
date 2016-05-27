#coding=utf-8

import pdb , json , datetime , pymongo

import tornado.web

import status
import utils
from model import models


#测试
class IndexHandler(tornado.web.RequestHandler) :
    def get(self) :
        self.render(
            "index.html",
            page_title = "user address",
            header_text = "用户地址列表",
        )

#获取用户地址列表
class UserAddressListHandler(tornado.web.RequestHandler) :
    def get(self):

        result = utils.init_response_data()

        try :
            user_id = self.get_argument("user_id")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return

        coll = models.get_coll("UserAddress")

        user_address_list = []
        temp_user_address_list = []
        query_params = dict(
            user_id = int(user_id) ,
        )

        [ temp_user_address_list.append(address) for address in coll.find(query_params)\
        .sort([("is_default_flag",pymongo.DESCENDING) , ("add_time",pymongo.DESCENDING)])]

        for address in temp_user_address_list :
            address["_id"] = utils.objectid_str(address["_id"])

        [ user_address_list.append(address) for address in temp_user_address_list ]

        result["data"]["user_address_list"] = user_address_list

        self.write(result)

#设置用户指定地址为默认地址
class UserAddressDefaultHandler(tornado.web.RequestHandler) :
    def put(self) :

        result = utils.init_response_data()

        try :
            user_id = self.get_argument("user_id")
            address = self.get_argument("address")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return

        coll = models.get_coll("UserAddress")

        query_params = dict(
            user_id = int(user_id) ,
            address = address ,
        )
        address = coll.find_one(query_params)
        if not address :
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return
        else :
            default_address_query_param = dict(
                is_default_flag = True ,
            )
            default_address_list = coll.find(default_address_query_param)
            for default_address in default_address_list :
                default_address["is_default_flag"] = False
                coll.save(default_address)

            address["is_default_flag"] = True
            coll.save(address)

        self.write(result)

#用户地址操作
class UserAddressHandler(tornado.web.RequestHandler) :
    def post(self) :
        result = utils.init_response_data()

        try :
            user_id = self.get_argument("user_id")
            province = self.get_argument("province")
            city = self.get_argument("city")
            area = self.get_argument("area")
            address = self.get_argument("address")
            is_default_flag = self.get_argument("is_default_flag")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return

        add_time = str(datetime.datetime.now()).split(".")[0]

        coll = models.get_coll("UserAddress")

        address = dict(
            user_id = int(user_id) ,
            province = province ,
            city = city ,
            area = area ,
            address = address ,
            is_default_flag = bool(is_default_flag) ,
            add_time = add_time ,
        )
        if not coll.find({"user_id":address["user_id"] , "address":address["address"]}).count():
            coll.insert(address)

            if address.has_key("_id") :
                address["_id"] = utils.objectid_str(address["_id"])
            else :
                pass

            result["data"] = address
        else :
            result = utils.reset_response_data(status.Status.EXIST)
            self.write(result)
            return

        self.write(result)

    def delete(self) :

        result = utils.init_response_data()

        try :
            address_id = self.get_argument("address_id")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return

        obj_id = utils.create_objectid(address_id)

        coll = models.get_coll("UserAddress")

        address = coll.find_one({"_id":obj_id})
        if address :
            coll.remove(address)
        else :
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return

        self.write(result)

    def put(self) :

        result = utils.init_response_data()

        coll = models.get_coll("UserAddress")

        try :
            alter_params = self.get_argument("alter_params")
            alter_params = json.loads(alter_params)
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return

        if not alter_params.has_key("_id") :
            result = utils.reset_response_data(status.Status.NOT_ID)
            self.write(result)
            return
        else :
            obj_id = utils.create_objectid(alter_params["_id"])
            query_params = dict(
                _id = obj_id ,
            )
            address = coll.find_one(query_params)
            if not address :
                result = utils.reset_response_data(status.Status.NOT_EXIST)
                self.write(result)
                return
            else :
                alter_params["_id"] = obj_id
                if alter_params.has_key("user_id") :
                    del alter_params["user_id"]
                if alter_params.has_key("is_default_flag") :
                    del alter_params["is_default_flag"]

                coll.update(query_params,{"$set":alter_params})

        self.write(result)

    def get(self) :

        result = utils.init_response_data()

        coll = models.get_coll("UserAddress")

        try :
            address_id = self.get_argument("address_id")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info=str(e))
            self.write(result)
            return
        obj_id = utils.create_objectid(address_id)
        query_params = dict(
            _id = obj_id ,
        )
        address = coll.find_one(query_params)
        if not address :
            result = utils.reset_response_data(status.Status.NOT_EXIST)
            self.write(result)
            return
        else :
            address["_id"] = address_id
            result["data"] = address

        self.write(result)


handlers = [
    (r"/",IndexHandler),
    (r"/api/address/list",UserAddressListHandler),
    (r"/api/address/default",UserAddressDefaultHandler),
    (r"/api/address",UserAddressHandler),
]
