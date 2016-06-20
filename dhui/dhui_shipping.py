#coding=utf-8

import pdb, sys, datetime
from bson.objectid import ObjectId

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def import_shipping_data(*args,**kwargs):
    shipping_coll = mongodb_client.get_coll("DHUI_Shipping")
    start_time, end_time = utils.get_time_range()
    shipping_list = shipping_coll.find({
        "add_time":{
            "$gte":start_time,
            "$lte":end_time,
        }
    })
    for shipping in shipping_list[1:2]:
        _id = utils.objectid_str(shipping['_id'])
        company = shipping['company']
        number = shipping['number']
        add_time = shipping['add_time']
        address = shipping['address']
        orders = shipping['orders']
        track = shipping['track']

        query_params = dict(
            _id = _id ,
        )
        shipping_obj = dict(
            _id=_id,
            company=company,
            number=number,
            add_time=add_time,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiShipping")
        if utils.has_obj(xmlrpcclient,query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0],shipping_obj)
            shipping_id = result[0]
        else :
            shipping_id = utils.load_obj(xmlrpcclient,shipping_obj)

        contact_name = address["contact_name"]
        contact_mobile = address["contact_mobile"]
        detailed_address = address["detailed_address"]
        query_params = dict(
            contact_name = contact_name,
            contact_mobile = contact_mobile,
        )
        shipping_address_obj = dict()
        shipping_address_obj.update(address)
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiShippingAddress")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], shipping_address_obj)

        else:
            utils.load_obj(xmlrpcclient, shipping_address_obj)

        order_id_list = []
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("SaleOrder")
        for order in orders :
            order_id = order["_id"]
            query_params = dict(
                _id=order_id,
            )
            try :
                result = xmlrpcclient.search(query_params)
                if len(result):
                    order_id_list.append(result[0])
                else:
                    continue
            except Exception ,e :
                continue

        obj_list = []
        for order_id in order_id_list:
            obj_list.append(dict(
                id=order_id,
                alter_params=dict(
                    shipping_id=shipping_id,
                )
            ))
        utils.update_obj_list(xmlrpcclient,obj_list)

        # kuaidi
        status = track['status']
        last_result = track['lastResult']
        message = track['message']
        billstatus = track['billstatus']
        auto_check = track['autoCheck']
        com_old = track['comOld']
        query_params = dict(
            shipping_id = shipping_id,
        )
        shipping_kuaidi_obj = dict(
            status = status,
            message = message,
            billstatus = billstatus,
            auto_check = auto_check,
            com_old = com_old,
            shipping_id = shipping_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiShippingKuaidi")
        if utils.has_obj(xmlrpcclient,query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0],shipping_kuaidi_obj)
            kuaidi_id = result[0]
        else :
            kuaidi_id = utils.load_obj(xmlrpcclient,shipping_kuaidi_obj)

        status = last_result['status']
        state = last_result['state']
        ischeck = last_result['ischeck']
        message = last_result['message']
        com = last_result['com']
        nu = last_result['nu']
        condition = last_result['condition']
        data = last_result['data']

        query_params = dict(
            kuaidi_id = kuaidi_id,
        )
        shipping_last_result_obj = dict(
            status = status,
            state = state,
            ischeck = ischeck,
            message = message,
            com = com,
            nu = nu,
            condition = condition,
            kuaidi_id = kuaidi_id,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiShippingKuaidiLastresult")
        if utils.has_obj(xmlrpcclient,query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0],shipping_last_result_obj)
            lastresult_id = result[0]
        else:
            lastresult_id = utils.load_obj(xmlrpcclient,shipping_last_result_obj)

        for last_result_line in data :
            ftime = last_result_line['ftime']
            context = last_result_line['context']
            time = last_result_line['time']
            query_params = dict(
                lastresult_id = lastresult_id,
                ftime=ftime,
                context=context,
                time=time,
            )
            last_result_line_obj = dict(
                ftime = ftime,
                context = context,
                time = time,
                lastresult_id = lastresult_id,
            )
            xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiShippingKuaidiLastresultLine")
            if utils.has_obj(xmlrpcclient,query_params):
                result = xmlrpcclient.search(query_params)
                xmlrpcclient.update(result[0],last_result_line_obj)
            else :
                utils.load_obj(xmlrpcclient,last_result_line_obj)

if __name__ == "__main__":
    import_shipping_data()



