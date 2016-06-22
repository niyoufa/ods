#coding=utf-8

import pdb, sys, datetime,json
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def import_user_data(*args,**options):
    customer_coll = mongodb_client.get_coll("DHUI_User")
    address_coll = mongodb_client.get_coll("DHUI_Address")
    user_list = customer_coll.find({})
    for user in user_list :
        user_id = utils.objectid_str(user["_id"])
        address = address_coll.find_one({"user_id":user_id})
        if address == None :
            address_id = ""
        else :
            address_id = utils.objectid_str(address["_id"])
        if user.has_key("wx_info"):
            wx_info = user["wx_info"]
            dhui_user_obj = dict(
                user_id=user_id,
                address_id=address_id,
                nickname= wx_info.get("nickname",""),
                province = wx_info.get("province",""),
                language = wx_info.get("language",""),
                openid = wx_info.get("openid",""),
                unionid = wx_info.get("unionid",""),
                sex = wx_info.get("sex",0),
                country = wx_info.get("country",""),
                privilege = json.dumps(wx_info.get("privilege",[])),
                headimgurl= wx_info.get("headimgurl",""),
                city = wx_info.get("city",""),
            )
        else :
            dhui_user_obj = dict(
                user_id=user_id,
                address_id=address_id,
            )

        query_params = dict(
            user_id= user_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ResUsers")
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], dhui_user_obj)
        else:
            utils.load_obj(xmlrpcclient, dhui_user_obj)
            print dhui_user_obj

def import_dhuitask_user(*args,**options):
    customer_coll = mongodb_client.get_coll("DHUI_User")
    address_coll = mongodb_client.get_coll("DHUI_Address")
    user_list = customer_coll.find({})
    for user in user_list:
        user_id = utils.objectid_str(user["_id"])
        address = address_coll.find_one({"user_id": user_id})
        if address == None:
            address_id = ""
        else:
            address_id = utils.objectid_str(address["_id"])
        if user.has_key("wx_info"):
            wx_info = user["wx_info"]
            dhui_user_obj = dict(
                user_id=user_id,
                nickname=wx_info.get("nickname", ""),
                province=wx_info.get("province", ""),
                language=wx_info.get("language", ""),
                openid=wx_info.get("openid", ""),
                unionid=wx_info.get("unionid", ""),
                sex=wx_info.get("sex", 0),
                country=wx_info.get("country", ""),
                privilege=json.dumps(wx_info.get("privilege", [])),
                headimgurl=wx_info.get("headimgurl", ""),
                city=wx_info.get("city", ""),

                #res.users
                company_id = 1,
                name = wx_info.get("nickname", u"东汇用户"),
                login = wx_info.get("nickname", u"东汇用户") + "@dhui.com",

            )
        else:
            dhui_user_obj = dict(
                user_id=user_id,
                address_id=address_id,
            )

        query_params = dict(
            user_id=user_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ResUsers")
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], dhui_user_obj)
        else:
            utils.load_obj(xmlrpcclient, dhui_user_obj)
            print dhui_user_obj

        #修改用户权限（修改所属群组)
        # res_groups_users_rel
        # self.write
        # self = res.users
        # cr = < openerp.sql_db.Cursor
        # object
        # at
        # 0x7f94480ee5d0 >
        # uid = 1
        # fields = [151]
        # args = ({'sel_groups_9_28_10': False, 'sel_groups_53_54': 53},)
        # options = {
        #     'context': {'lang': 'zh_CN', 'params': {'action': 76}, 'search_default_no_share': 1, 'tz': 'Asia/Shanghai',
        #                 'uid': 1}}


def get_user_list(*args,**options):
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiUser")
    user_list = xmlrpcclient.read({})

if __name__ == "__main__":
    import_dhuitask_user()
