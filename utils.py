#coding=utf-8

import time
import datetime, logging
import json, pdb, sys, traceback
from bson.objectid import ObjectId
from bson.json_util import dumps
import ods.tnd_server.status as status
import ods.settings as settings

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

#生成objectid
def create_objectid(str):
    return ObjectId(str)

#将objectid 转换为string字符串
def objectid_str(objectid):
    return  json.loads(dumps(objectid))['$oid']

#发送跨域POST请求
def send_post_request(url,data,csrftoken,headers) :
    import urllib
    import urllib2
    import cookielib

    data = urllib.urlencode(data)

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'csrftoken=%s'%(csrftoken)))
    opener.addheaders.extend(headers.items())
    result = json.loads(opener.open(url,data).read())
    return result

#获取csrf token
def get_csrf_token(url) :
    import urllib
    import urllib2
    import cookielib
    f = urllib.urlopen(url)
    result_data = json.loads(f.read())
    result_data["headers"] = f.headers
    return result_data

#获得错误堆栈信息
def get_trace_info():
    trace_info = ""
    info = sys.exc_info()
    for file, lineno, function, text in traceback.extract_tb(info[2]):
        trace_info += "file：%s,line:%s\n in %s;\n"%(file,lineno,function)
    return trace_info

#函数异常处理器
def func_except_handler(func) :
    def _func_except_handler():
        result = {}
        try :
            result =   func()
        except Exception , e :
            result["success"] = status.Status.ERROR
            result["return_code"] = status.Status().getReason(result["success"])
            return result
        return result
    return _func_except_handler

#初始化返回参数
def init_response_data():
    result = {}
    result["success"] = status.Status.OK
    result["return_code"] = status.Status().getReason(result["success"])
    result["data"] = {}
    return result

#重置返回参数
def reset_response_data(status_code,error_info=None):
    result = {}
    result["success"] = status_code
    result["return_code"] = status.Status().getReason(result["success"])
    if error_info :
        result["error_info"] = error_info
    result["data"] = {}
    return result

#列表排序
def sort_list(list_obj,sort_key) :
    if not type(list_obj) == type([]) :
        raise Exception("type error")
    else :
        list_obj.sort(key=lambda obj :obj[sort_key])
    return list_obj

#导入项目代码
def load_project():
    # import sys , os
    # BASE_DIR = os.path.abspath(__file__)
    # _root = os.path.dirname(BASE_DIR)
    # sys.path.append(_root)

    import sys , os
    BASE_DIR = "E:\\develop\\tornado_demo\\swallow"
    sys.path.append(BASE_DIR)

def timestamp_from_objectid(objectid):
  result = 0
  try:
    timestamp = time.mktime(objectid.generation_time.timetuple())
    temp_list = str(timestamp).split(".")
    result = int("".join(temp_list))
  except:
    pass
  return result


# odoo 数据操作

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

def get_order_list(xmlrpcclient,query_params,extra_query_params):
    sale_order_list = read_obj(xmlrpcclient,query_params,extra_query_params)
    return sale_order_list

def update_obj_list(xmlrpcclient, obj_list):
    xmlrpcclient.batch_update(obj_list)


# dj_server
import re, time


def list_first_item(value):
    try:
        if not hasattr(value[0], '__iter__'):
            return [value[0]]
        else:
            return value[0]
    except Exception:
        return None


def float_equals(a, b):
    return abs(a - b) <= 1e-6


def uid(class_name):
    # 将大写字母换成小写并在字母前加前缀_
    return re.sub(r'([A-Z])', r'_\1', class_name).lower()[1:]


# 根据卡号返回消费类型,1:普通银行卡,2:加油卡,3:信用卡,1000:现金
def getPaymentTypeByCard(card, card_fromat=None):
    if card_fromat != None:
        reobj = re.compile(card_fromat)
        result = reobj.match(card)

        # 加油卡
        if result:
            return 2

    # 银行卡号最多为19位
    if len(card) > 19:
        return 1000

    # 银行卡至少为16位,信用卡至少为14位
    if len(card) >= 14:

        # 前六位为银行卡的BIN
        front = int(card[:6])

        # 信用卡BIN分配如下:
        # 威士卡（VISA）:400000—499999;万事达卡（MasterCard）:510000—559999;
        # 运通卡（American Express）:340000—349999，370000—379999;
        # 大来卡（DinersClub）:300000—305999，309500—309599,360000—369999，380000—399999;
        # JCB卡（JCB）:352800—358999
        if (front >= 300000 and front <= 305999) or (front >= 309500 and front <= 305999) or \
                (front >= 360000 and front <= 369999) or (front >= 380000 and front <= 399999) or \
                (front >= 352800 and front <= 358999) or (front >= 340000 and front <= 349999) or \
                (front >= 370000 and front <= 379999) or (front >= 510000 and front <= 559999) or \
                (front >= 400000 and front <= 499999):
            return 3

        else:
            if len(card) >= 16:
                card_front = card[:1]
                # 普通银行卡以6,9开头,多数为6
                if card_front == '6' or card_front == '9':
                    return 1
                else:
                    return 1000

    # 现金
    return 1000


# 序列化交易编号
def compute_trans_id(data_time, shard_id, site_id, gun_id, money):
    # 交易时间,32位
    data_time = long(int(data_time))
    data_time = data_time << 32

    # 服务器编号，6位，最多64台
    shard_id = shard_id << 26

    # 油站编号,10位，最多每个服务器上1024个
    site_id = site_id << 16

    # 油枪号，7位，一个油站最多128个
    gun_id = gun_id << 9

    # 金额 9位
    result = data_time + shard_id + site_id + gun_id + money

    return result


# 反序列化交易编号
def deserialize_trans_id(long_trans_id):
    num = long(long_trans_id)
    # 获取高32位的时间
    time = int(num >> 32)
    # 获取低32 位
    num = num & 0xFFFFFFFF
    shard_id = num >> 26
    # 取出低26位
    num = num & 0x3FFFFFF
    site_id = num >> 16
    # 取出低16位
    num = num & 0xFFFF
    gun_id = num >> 9
    # 获取金额
    money = num & 0x1FF
    return (time, shard_id, site_id, gun_id, money)


# 字典支持点操作类
class easyaccessdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        n = easyaccessdict()
        super(easyaccessdict, self).__setitem__(name, n)
        return n

    def __getitem__(self, name):
        if name not in self:
            super(easyaccessdict, self).__setitem__(name, nicedict())
        return super(easyaccessdict, self).__getitem__(name)

    def __setattr__(self, name, value):
        super(easyaccessdict, self).__setitem__(name, value)


# 字典支持点操作
def tran_dict_to_obj(dict_data):
    obj = easyaccessdict()
    for item in dict_data:
        obj[item] = dict_data[item]
    return obj


# 把object对象转化为可json序列化的字典
def convert_to_dict(obj):
    dic = {}
    if not isinstance(obj, dict):
        dic.update(obj.__dict__)
    else:
        dic = obj
    for key, value in dic.items():
        if isinstance(value, datetime.datetime):
            dic[key] = str(value)
        elif key[0] == '_':
            dic.pop(key)

    return dic

# mongodb 相关处理

#获取东汇商城用户名
def get_customer(coll,user_id):
    result = {}
    try :
        user = coll.find_one({"_id":ObjectId(user_id)})
    except :
        return result
    if user:
        result.update(user["wx_info"])
    else :
        result = {}
    return result

#返回地址信息
def get_address(coll,address_id):
    result = {}
    try :
        address = coll.find_one({"_id":ObjectId(address_id)})
    except:
        return result

    if address :
        result["district"] = address["district"]
        result["area"] = address["area"]
        result["city"] = address["city"]
        result["detailed_address"] = address["detailed_address"]
        result["contact_mobile"] = address["contact_mobile"]
        result["contact_name"] = address["contact_name"]
        result["remark"] = address["remark"]
    else:
        result = {}
    return result

#python time时间处理相关工具

def get_report_date(time=datetime.datetime.now(),delta=0):
    curr_date = time - datetime.timedelta(days=delta)
    return curr_date

def get_curr_time(delta=0):
    curr_date = datetime.datetime.now() - datetime.timedelta(days=delta)
    curr_time = str(curr_date).split(".")[0]
    return curr_time

def get_report_time(query_time=datetime.datetime.now(),*args,**options):
    report_date = get_report_date(query_time,delta=options.get("delta",0))
    report_time = str(report_date).split(".")[0]
    cmp_time = str(report_date).split(" ")[0] + " " +"00:00:00"
    if report_time < cmp_time :
        yester_date = report_date - datetime.timedelta(days=1)
        end_time = str(report_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(yester_date).split(" ")[0] + " " + "00:00:00"
    else :
        tormo_date = report_date + datetime.timedelta(days=1)
        end_time = str(tormo_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(report_date).split(" ")[0] + " " + "00:00:00"
    return start_time, end_time

def get_time_range(query_time=datetime.datetime.now(),*args,**options):
    range_date = get_report_date(query_time,delta=options.get("delta",0))
    range_time = str(range_date).split(".")[0]
    cmp_time = str(range_date).split(" ")[0] + " " + "00:00:00"
    if range_time < cmp_time:
        yester_date = range_date - datetime.timedelta(days=1)
        end_time = str(range_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(yester_date).split(" ")[0] + " " + "00:00:00"
    else:
        tormo_date = range_date + datetime.timedelta(days=1)
        end_time = str(tormo_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(range_date).split(" ")[0] + " " + "00:00:00"
    return start_time, end_time

def get_date_time(date_time_str):
    date_time_str = str(date_time_str).split(".")[0]
    date_time_arr = time.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    this_date = datetime.datetime(date_time_arr[0],date_time_arr[1],date_time_arr[2],date_time_arr[3],
                                  date_time_arr[4],date_time_arr[5])
    this_time = str(this_date).split(".")[0]
    cmp_time = str(this_date).split(" ")[0] + " " + "00:00:00"
    if this_time < cmp_time:
        yester_date = this_date - datetime.timedelta(days=1)
        end_time = str(this_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(yester_date).split(" ")[0] + " " + "00:00:00"
    else:
        tormo_date = this_date + datetime.timedelta(days=1)
        end_time = str(tormo_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(this_date).split(" ")[0] + " " + "00:00:00"
    return start_time, end_time

# utc 与本地时间转换
def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def local2utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

def str2datetime(timestr):
    t = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    d = datetime.datetime(*t[:6])
    return d

# ods 调用 dj_server

#生成商品发货单
def create_good_invoice(*args,**kwargs):
    mongodb_client = kwargs.get("mongodb_client")
    do = kwargs.get("do")
    dol = kwargs.get("dol")
    dpt = kwargs.get("dpt")
    di = kwargs.get("di")
    print ""
    print "开始创建或更新供应商商品发货单发货明细... 日期：%s" % str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0]
    InfoLogger.info("开始创建或更新供应商商品发货单发货明细... 日期：%s" % str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0])
    print ""
    # sale_product_detail_info 订单商品信息明细
    sale_order_list = do.get_sale_order_list()
    sale_order_line_dict = {}
    sale_order_user_dict = {}
    sale_order_count = 0

    for sale_order in sale_order_list:
        sale_order_id = sale_order["id"]
        sale_order_line_dict[sale_order_id] = dol.get_sale_order_line_list(sale_order_id)

        order_customer_id = sale_order["order_customer_id"]
        order_address_id = sale_order["order_address_id"]
        sale_order_user_dict[sale_order_id] = dict(
            order_customer_id=order_customer_id,
            order_address_id=order_address_id,
        )
        sale_order_count += 1

    # sale_product_detail_info 采购单明细
    sale_product_detail_info = {}
    for order_id in sale_order_line_dict:
        sale_order_line_list = sale_order_line_dict[order_id]
        sale_order_user_info = sale_order_user_dict[order_id]
        order_customer_id = sale_order_user_info["order_customer_id"]
        order_address_id = sale_order_user_info["order_address_id"]

        customer_coll = mongodb_client.get_coll("DHUI_User")
        address_coll = mongodb_client.get_coll("DHUI_Address")
        customer = get_customer(customer_coll, order_customer_id)
        address = get_address(address_coll, order_address_id)

        for sale_order_line in sale_order_line_list:
            temp_user_info = {}

            product_id, product_name = tuple(sale_order_line["product_id"])
            product_uom_qty = sale_order_line["product_uom_qty"]

            product_template_obj = dpt.get_product_template_by_id(product_id=product_id)
            if not product_template_obj:
                continue
            sku = product_template_obj["sku"]
            name = product_template_obj["name"]
            partner_id = product_template_obj["dhui_user_id"]
            if sale_product_detail_info.has_key(product_id):
                sale_product_detail_info[product_id]["total_count"] += product_uom_qty
            else:
                sale_product_detail_info[product_id] = {}
                sale_product_detail_info[product_id]["total_count"] = product_uom_qty
                sale_product_detail_info[product_id]["partner_id"] = partner_id
                sale_product_detail_info[product_id]["sku"] = sku
                sale_product_detail_info[product_id]["name"] = name
                sale_product_detail_info[product_id]["user_info"] = []

            if temp_user_info.has_key(order_customer_id):
                temp_user_info[order_customer_id]["count"] += 1
            else:
                temp_user_info[order_customer_id] = dict(
                    product_id=product_id,
                    partner_id=partner_id,
                    user_id=order_customer_id,
                    address_id=order_address_id,
                    count=1
                )

            temp_user_info[order_customer_id].update(customer)
            temp_user_info[order_customer_id].update(address)

            # user_info
            for order_customer_id in temp_user_info:
                good_user_info = temp_user_info[order_customer_id]
                sale_product_detail_info[product_id]["user_info"].append(good_user_info)

    temp_sale_product_detail_info = []
    for product_id in sale_product_detail_info:
        sale_product_detail = sale_product_detail_info[product_id]
        temp_sale_product_detail_info.append(sale_product_detail)
    sale_product_detail_info = temp_sale_product_detail_info

    # partner_order_deliver_details  商家发货信息明细
    partner_order_deliver_details = {}
    for sale_product_detail in sale_product_detail_info:
        partner_id = sale_product_detail["partner_id"]
        if partner_order_deliver_details.has_key(partner_id):
            partner_order_deliver_details[partner_id]["detail_info"].append(sale_product_detail)
        else:
            partner_order_deliver_details[partner_id] = dict(
                partner_id=partner_id,
                detail_info=[sale_product_detail]
            )
    # 持久化商家发货信息明细
    start_time, end_time = get_report_time(delta=kwargs.get("delta",0))
    coll = mongodb_client.get_coll("DHUI_PartnerGoodDeliverDetail")

    flag = None
    log_result = []
    for partner_id in partner_order_deliver_details:
        partner_order_deliver_detail = partner_order_deliver_details[partner_id]
        curr_time = str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0] + " 01:00:00"
        alter_time = str(get_curr_time())
        result = coll.find_one({"partner_id": partner_id, "create_time": {"$gte": start_time, "$lte": end_time}})
        if not result:
            partner_order_deliver_detail.update(dict(
                create_time=curr_time,
                alter_time=curr_time,
                deliver_status=0,  # stastus 0:为发货 1:已发货
                sale_order_count=sale_order_count,
            ))
            coll.insert_one(partner_order_deliver_detail)

            flag = False

            print "创建发货订单明细"
            print  partner_order_deliver_detail
        else:
            partner_order_deliver_detail.update(dict(
                _id=result["_id"],
                create_time=result["create_time"],
                alter_time=alter_time,
                deliver_status=result["deliver_status"],
                partner_id=result["partner_id"],
                sale_order_count=sale_order_count
            ))
            coll.update({"_id": result["_id"]}, partner_order_deliver_detail)

            flag = True

            print "更新发货订单明细"
            InfoLogger.info("更新发货订单明细")
            print partner_order_deliver_detail

        log_result.append(partner_order_deliver_detail)

    try:
        # 发货信息
        result = di.import_invoice()
        InfoLogger.info(result)
    except Exception, e:
        print e

    if flag == True:
        print "完成创建供应商商品发货单发货明细..."
        InfoLogger.info("完成创建供应商商品发货单发货明细...")
        print ""
    elif flag == False:
        print "完成更新供应商商品发货单发货明细..."
        InfoLogger.info("完成更新供应商商品发货单发货明细...")
        print ""
    else:
        print "当前没有商品发货信息..."
        InfoLogger.info("当前没有商品发货信息...")
        print ""

    return log_result

#生成订单发货单
def create_order_invoice(*args,**kwargs):
    mongodb_client = kwargs.get("mongodb_client")
    xmlrpc_client = kwargs.get("xmlrpc_client")
    do = kwargs.get("do")
    dol = kwargs.get("dol")
    dpt = kwargs.get("dpt")
    di = kwargs.get("di")
    print ""
    print "开始创建或更新供应商订单发货单发货明细... 日期：%s" % str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0]
    InfoLogger.info("开始创建或更新供应商订单发货单发货明细... 日期：%s" % str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0])
    print ""
    # sale_product_detail_info 订单商品信息明细
    coll = mongodb_client.get_coll("DHUI_SaleOrder")
    
    start_time, end_time = get_report_time(delta=kwargs.get("delta",0))
    sale_order_list = coll.find({
        "pay_time": {"$gte": start_time, "$lte": end_time},
        "order_status": 1,
        "order_goods.goods_type": {"$nin": ["goldbean", "profit", "indiana_count"]}})

    partner_sale_order_dict = {}
    for sale_order in sale_order_list:
        sale_order["_id"] = objectid_str(sale_order["_id"])
        order_goods = sale_order["order_goods"]
        if len(order_goods):
            good = order_goods[0]
        else :
            continue

        sku = good["sku"]
        query_params = dict(
            sku=sku,
            categ_id=settings.PRODUCT_CATEGRAY_ID,
        )
        xmlrpcclient = xmlrpc_client.get_xmlrpcclient("ProductTemplate")
        if has_obj(xmlrpcclient, query_params):
            [good_obj] = read_obj(xmlrpcclient,query_params)
        else:
            continue
        partner_id = good_obj['dhui_user_id']

        if partner_sale_order_dict.has_key(partner_id):
            partner_sale_order_dict[partner_id].append(sale_order)
        else :
            partner_sale_order_dict[partner_id] = [sale_order]

    # 持久化商家订单发货信息明细
    flag = None
    log_result = []
    coll = mongodb_client.get_coll("DHUI_PartnerOrderDeliverDetail")
    for partner_id in  partner_sale_order_dict:
        partner_order_deliver_detail = dict()

        curr_time = str(get_report_date(delta=kwargs.get("delta",0))).split(" ")[0] + " 01:00:00"
        alter_time = str(get_curr_time())
        result = coll.find_one({"partner_id": partner_id, "create_time": {"$gte": start_time, "$lte": end_time}})
        if not result:
            partner_order_deliver_detail.update(dict(
                create_time=curr_time,
                alter_time=curr_time,
                deliver_status=0,  # stastus 0:未开始发货 1:发货中 2:已全部完成发货
                partner_id = partner_id,
                order_list = partner_sale_order_dict[partner_id]
            ))
            coll.insert_one(partner_order_deliver_detail)

            flag = False

            print "创建发货订单明细"
            print  partner_order_deliver_detail
        else:
            partner_order_deliver_detail.update(dict(
                _id=result["_id"],
                create_time=result["create_time"],
                deliver_status=result["deliver_status"],
                alter_time=alter_time,
                partner_id=partner_id,
                order_list=partner_sale_order_dict[partner_id]
            ))
            coll.update({"_id": result["_id"]}, partner_order_deliver_detail)

            flag = True

            print "更新发货订单明细"
            InfoLogger.info("更新发货订单明细")
            print partner_order_deliver_detail

    if flag == True:
        print "完成创建供应商订单发货单发货明细..."
        InfoLogger.info("完成创建供应商订单发货单发货明细...")
        print ""
    elif flag == False:
        print "完成更新供应商订单发货单发货明细..."
        InfoLogger.info("完成更新供应商订单发货单发货明细...")
        print ""
    else:
        print "当前没有订单发货信息..."
        InfoLogger.info("当前没有订单发货信息...")
        print ""

    return log_result


# 手动生成发货单操作
def manual_create_invoice(*args,**options):
    dpt = options.get("dpt")
    dps = options.get("dps")
    dpwo = options.get("dpwo")
    print ""
    print "开始导入商品数据到odoo..."
    # InfoLogger.info("开始导入商品数据到odoo...")

    try:
        # 商品基本信息
        result = dpt.import_product_template_data()
        # InfoLogger.info(result)
        # 更新商品供应商信息
        result = dps.update_product_supplierinfo()
        # InfoLogger.info(result)
        # 更新商品重订货规则
        result = dpwo.update_stock_warehouse_orderpoint()
        # InfoLogger.info(result)
    except Exception, e:
        print e
        # 打印错误信息
        ErrorLogger.error("错误信息：%s." % (str(e)))
        print "日期：%s 错误信息：%s." % (str(datetime.datetime.now()), str(e))

    print "完成导入商品数据到odoo！"
    # InfoLogger.info("完成导入商品数据到odoo！")

    do = options.get("do")
    dol = options.get("dol")
    print "\n"
    print "开始导入订单数据到odoo..."
    # InfoLogger.info("开始导入订单数据到odoo...")

    try:
        # 订单基本信息
        result = do.import_sale_order_data()
        # InfoLogger.info(result)
        # 订单商品信息
        result = dol.import_sale_order_line()
        # 记录日志
        # InfoLogger.info(result)
    except Exception, e:
        print e

    print "完成导入订单数据到odoo!"
    # InfoLogger.info("完成导入订单数据到odoo!")

    mongodb_client = options.get("mongodb_client")
    log_result = create_invoice(do=do,dol=dol,dpt=dpt,mongodb_client=mongodb_client)
    for deliver_detail in log_result :
        deliver_detail["_id"] = str(deliver_detail["_id"])
    return log_result

# 测试timestr
if __name__ == "__main__":
    pass
