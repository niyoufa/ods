# -*- coding: utf-8 -*-
import model.models as Mongo_Utils

class BaseModel(object):
    def __init__(self):
        super.__init__(self)

class UserAddressModel(BaseModel):
    COLL_NAME = "UserAddress"
    columns = dict(
        user_id = dict(
            column_name = "user_id" ,
            column_type = "Integer" ,
            nullable = False ,
        ) ,
        province = dict(
                column_name = "province" ,
                column_type = "String" ,
                nullable = False ,
        ) ,
        city = dict(
                column_name = "city" ,
                column_type = "String" ,
                nullable = False ,
        ) ,
        area = dict(
                column_name = "area" ,
                column_type = "String" ,
                nullable = False ,
        ) ,
        address = dict(
                column_name = "address" ,
                column_type = "String" ,
                nullable = False ,
        ) ,
        is_default_flag = dict(
                column_name = "is_default_flag" ,
                column_type = "Boolean" ,
                nullable = False ,
        ) ,
        add_time = dict(
                column_name = "add_time" ,
                column_type = "String" ,
                nullable = False ,
        ) ,
    )

    @classmethod
    def check_column_define(cls,document) :
        if type(document) != type({}) :
            raise Exception("ValueError")
        else :
            for item in document :
                if not item in cls.columns.keys() :
                    raise Exception("Column Not Exist")
                else :
                    pass

    @classmethod
    def init_test_data(cls) :
        coll = Mongo_Utils.get_coll(cls.COLL_NAME)
        test_user_address_info_list = [
            dict(
                user_id = 1 ,
                province = u"江苏" ,
                city = u"南京" ,
                area = u"六合区" ,
                address = u"金牛湖村" ,
                is_default_flag = False ,
                add_time = u"2016-05-04 17:45:50" ,
            ) ,
            dict(
                user_id = 1 ,
                province = u"江苏" ,
                city = u"南京" ,
                area = u"六合区" ,
                address = u"金牛湖街道" ,
                is_default_flag = False ,
                add_time = u"2016-05-04 17:45:50" ,
            ) ,
            dict(
                user_id = 2 ,
                province = "江苏" ,
                city = u"无锡" ,
                area = u"XX区" ,
                address = u"XXX村" ,
                is_default_flag = False ,
                add_time = u"2016-05-04 17:45:50" ,
            ) ,
            dict(
                user_id = 3 ,
                province = u"江苏" ,
                city = u"镇江" ,
                area = u"XX区" ,
                address = u"XXX村" ,
                is_default_flag = False ,
                add_time = u"2016-05-04 17:45:50" ,
            ) ,
        ]

        count = 0
        for address in test_user_address_info_list :
            cls.check_column_define(address)
            flag = False
            if not coll.find({"user_id":address["user_id"] , "address":address["address"]}).count() :
                coll.insert(address)
                print address
                flag = True
                count += 1
        if flag == False :
            print u"没有新增数据！"
        else :
            print u"新增 %s 条数据\n"%(count)