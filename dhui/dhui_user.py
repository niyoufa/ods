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
<<<<<<< HEAD
    user_list = customer_coll.find({}).skip(12800)
=======
    user_list = customer_coll.find({}).skip(12900)
>>>>>>> 035433d90d71ee634af151eb036b349c7a59432a
    for user in user_list :
        user_id = utils.objectid_str(user["_id"])
        address = address_coll.find_one({"user_id":user_id})
        if address == None :
            address_id = ""
        else :
            address_id = utils.objectid_str(address["_id"])
        try :
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
        except Exception ,e:
            continue

        query_params = dict(
            user_id= user_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiUser")
        if utils.has_obj(xmlrpcclient, query_params):
            print 'continue'
            continue
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], dhui_user_obj)
        else:
            utils.load_obj(xmlrpcclient, dhui_user_obj)
            print dhui_user_obj

if __name__ == "__main__":
    import_user_data()
