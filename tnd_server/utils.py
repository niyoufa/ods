#coding=utf-8

import json , pdb
from bson.objectid import ObjectId
from bson.json_util import dumps

import status
import models
from models import Collections

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
