#coding=utf-8

import time
import datetime
import settings

def timestamp_from_objectid(objectid):
  result = 0
  try:
    timestamp = time.mktime(objectid.generation_time.timetuple())
    temp_list = str(timestamp).split(".")
    result = int("".join(temp_list))
  except:
    pass
  return result

def load_obj(xmlrpcclient,obj):
    return xmlrpcclient.create(obj)

def has_obj(xmlrpcclient,query_params):
    count = xmlrpcclient.search_count(query_params)
    if count > 0 :
        return True
    else :
        return False

def read_obj(xmlrpcclient,query_params,*args):
    if query_params.has_key("id_list"):
        result = xmlrpcclient.read_by_ids(query_params,*args)
    else :
        result = xmlrpcclient.read(query_params,*args)
    return result

def get_product_id(pt_xmlrpcclient,pp_xmlrpcclient,good):
    product_id = None
    sku = good["sku"]
    query_params = dict(
        sku=sku,
    )
    if has_obj(pt_xmlrpcclient, query_params):
        result = pt_xmlrpcclient.search(query_params)
        product_template_id = result[0]
    else:
        print "sku=%s:this good is not exist!" % good["sku"]
        return product_id

    query_params = dict(
        product_tmpl_id=product_template_id,
    )

    if has_obj(pp_xmlrpcclient, query_params):
        result = pp_xmlrpcclient.search(query_params)
        product_id = result[0]
    else:
        return product_id

    return product_id , product_template_id

def get_report_time():
    curr_date = datetime.datetime.now()
    yester_date = curr_date - datetime.timedelta(days=1)
    end_time = str(curr_date).split(" ")[0] + " " + settings.REPORT_END_TIME
    start_time = str(yester_date).split(" ")[0] + " " + settings.REPORT_STRAT_TIME
    print start_time , end_time
    return start_time , end_time

def get_order_list(xmlrpcclient,query_params,extra_query_params):
    sale_order_list = read_obj(xmlrpcclient,query_params,extra_query_params)
    return sale_order_list

