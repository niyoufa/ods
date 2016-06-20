#coding=utf-8

import pdb, sys, datetime,json
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def import_address_data(*args,**kwargs):

    address_coll = mongodb_client.get_coll("DHUI_Address")
    address_list = address_coll.find({}).skip(1548)

    log_result = []
    for address in address_list :

        if address.has_key("user_id"):
            user_id = address["user_id"]
        else :
            continue

        #查询用户id
        try :
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiUser")
            query_params = dict(
                user_id = user_id,
            )
            result = xmlrpcclient.search(query_params)
            user_id = result[0]
        except Exception ,e :
            continue

        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiAddress")
        query_params = dict(
            _id=utils.objectid_str(address["_id"]),
        )
        dhui_address_obj = dict()
        address["_id"] = utils.objectid_str(address["_id"])
        dhui_address_obj.update(address)
        if utils.has_obj(xmlrpcclient, query_params):
            continue
            dhui_address_obj['mod_time'] = str(datetime.datetime.now()).split(".")[0]
            dhui_address_obj['user_id'] = user_id
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], dhui_address_obj)
        else:
            dhui_address_obj['add_time'] = str(datetime.datetime.now()).split(".")[0]
            dhui_address_obj['mod_time'] = str(datetime.datetime.now()).split(".")[0]
            dhui_address_obj['user_id'] = user_id
            utils.load_obj(xmlrpcclient, dhui_address_obj)
            log_result.append(dhui_address_obj)
            print dhui_address_obj
    return log_result

if __name__ == "__main__" :
    import_address_data()
