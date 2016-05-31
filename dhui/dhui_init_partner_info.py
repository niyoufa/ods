#coding=utf-8

import pdb
import sys
sys.path.append("..")
import odoo_dock
import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import odoo_dock.utils as utils
import settings

def init_partner_info(*args,**kwargs):
    coll = mongodb_client.get_coll("DHUI_Partner")
    partner_list = coll.find()
    if not partner_list.count():
        partner_list = [
            dict(
                contact_name="dhui_partner",
                address="dhui_street",
                city="dhui_city",
                display_name="东汇城",
                zip=222000,
                email="dhui@qq.com",
                phone='15996458299',
                # dhui100 user_id
                # partner_id = '571dbf0c006f874b52b126aa',
            ),
        ]
    for partner in partner_list :
        name = partner["contact_name"]
        street = partner["address"]
        city = partner["city"]
        display_name = partner["display_name"]
        # 邮政编码
        zip = partner["zip"]
        country_id = 49
        email = partner["email"]
        phone = partner["phone"]
        supplier = True
        # partner_id = partner["partner_id"]

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
            # partner_id = partner_id,
        )

        query_params = dict(
            email = email,
            phone = phone,
            supplier = supplier,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ResPartner")
        if utils.has_obj(xmlrpcclient, query_params):
            result = xmlrpcclient.search(query_params)
            xmlrpcclient.update(result[0], res_partner_obj)
        else:
            utils.load_obj(xmlrpcclient, res_partner_obj)

    print "init complete !"


if __name__ == "__main__":
    init_partner_info()
