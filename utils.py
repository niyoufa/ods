#coding=utf-8

import time
import datetime
import json , pdb
from bson.objectid import ObjectId
from bson.json_util import dumps

#生成objectid
def create_objectid(str):
    return ObjectId(str)

#将objectid 转换为string字符串
def objectid_str(objectid):
    return  json.loads(dumps(objectid))['$oid']

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
    if not type(list_param) == type([]) :
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

def get_report_date():
    curr_date = datetime.datetime.now() - datetime.timedelta(days=0)
    return curr_date

def get_report_time():
    curr_date = get_report_date()
    curr_time = str(curr_date).split(".")[0]
    cmp_time = str(curr_date).split(" ")[0] + " " +"00:00:00"
    if curr_time < cmp_time :
        yester_date = curr_date - datetime.timedelta(days=1)
        end_time = str(curr_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(yester_date).split(" ")[0] + " " + "00:00:00"
    else :
        tormo_date = curr_date + datetime.timedelta(days=1)
        end_time = str(tormo_date).split(" ")[0] + " " + "00:00:00"
        start_time = str(curr_date).split(" ")[0] + " " + "00:00:00"
    return start_time, end_time