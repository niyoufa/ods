#coding=utf-8

import pdb, sys, datetime,json

import ods.clients.xmlrpc_client as xmlrpc_client
import ods.utils as utils
import ods.settings as settings

def get_task_list(*args,**options):
    user_id = options.get("user_id","571e98dd006f87607b83418b")
    if user_id == None :
        return []
    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ResUsers")
    query_params = dict(
        user_id = user_id,
    )
    if utils.has_obj(xmlrpcclient,query_params):
        [uid] = xmlrpcclient.search(query_params)
    else:
        return []

    xmlrpcclient = xmlrpc_client.get_xmlrpcclient("DhuiTask")
    task_id_list = []

    query_params = dict(
        create_uid = uid,
    )
    create_id_task_list = xmlrpcclient.search(query_params)

    query_params = dict(
        user_id = uid,
    )
    part_id_task_list = xmlrpcclient.search(query_params)

    query_params = dict(
        reviewer_id = uid,
    )
    review_id_task_list = xmlrpcclient.search(query_params)

    task_id_list.extend(create_id_task_list)
    task_id_list.extend(part_id_task_list)
    task_id_list.extend(review_id_task_list)
    task_id_list = list(set(task_id_list))

    query_params = dict(
        id_list = task_id_list,
        field_list = ["id","create_date","date_end","create_uid","user_id",
                      "data_start","progress","project_id","description",
                      "active","name","date_deadline","reviewer_id",
                      "total_hours","remaining_hours","group_type"]
    )
    task_list = utils.read_obj(xmlrpcclient,query_params)
    return task_list

if __name__ == "__main__":
    get_task_list()
