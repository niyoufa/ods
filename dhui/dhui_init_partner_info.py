#coding=utf-8

import pdb, logging
import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

# 供应商列表
partner_list = [
    dict(
        contact_name="东汇商城供应商",
        address="dhui_street",
        city="dhui_city",
        display_name="东汇商城供应商",
        zip=222000,
        email="dhui0@qq.com",
        phone='15996458299',
        dhui_user_id = "571dbf0c006f874b52b126aa",
        type="normal",

    ),
    dict(
        contact_name="东汇商城秒拍商品供应商",
        address="dhui_street",
        city="dhui_city",
        display_name="东汇商城秒拍商品供应商",
        zip=222000,
        email="dhui0@qq.com",
        phone='15996458299',
        dhui_user_id = "57330c6c006f877f57fcc4e7",
        type="seckill",
    ),
    dict(
        contact_name="东汇其他供应商",
        address="dhui_street",
        city="dhui_city",
        display_name="东汇其他供应商",
        zip=222000,
        email="dhui0@qq.com",
        phone='15996458299',
        dhui_user_id = "5720201c006f873b606394fb",
        type="other",
    ),
]

DHUI_PARTNER_DICT = {
    "default":["571dbf0c006f874b52b126aa",7,"default"],
    "seckill":["57330c6c006f877f57fcc4e7",10,"seckill"],
    "other":["5720201c006f873b606394fb",13,"other"],
}

def init_partner_info(*args,**kwargs):
    """
    创建并更新供应商，更新商品和供应商关系
    :param args:
    :param kwargs:
    :return:
    """

    coll = mongodb_client.get_coll("DHUI_Partner")
    print
    print "start update dhui partner...\n"

    for partner in partner_list :
        name = partner["contact_name"]
        dhui_user_id = partner["dhui_user_id"]
        type = partner["type"]
        street = partner["address"]
        city = partner["city"]
        display_name = partner["display_name"]
        # 邮政编码
        zip = partner["zip"]
        country_id = 49
        email = partner["email"]
        phone = partner["phone"]
        supplier = True

        res_partner_obj = dict(
            name = name,
            street = street,
            city = city,
            display_name = display_name,
            zip = zip,
            country_id = country_id,
            email = email,
            phone = phone,
            supplier = supplier,
        )

        query_params = dict(
            name = name,
            supplier = supplier,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ResPartner")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], res_partner_obj)
            partner_id = result[0]
        else:
            partner_id = utils.load_obj(xmlrpcclient, res_partner_obj)

        dhui_partner = coll.find_one({"name":name})
        if dhui_partner:
            dhui_partner["partner_id"] = partner_id
            coll.save(dhui_partner)
        else:
            dhui_partner = {}
            dhui_partner["name"] = name
            dhui_partner["dhui_user_id"] = dhui_user_id
            dhui_partner["partner_id"] = partner_id
            dhui_partner["type"] = type
            coll.insert_one(dhui_partner)

    return  partner_list

if __name__ == "__main__":
    init_partner_info()
