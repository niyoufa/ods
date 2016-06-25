# coding=utf-8
import pdb,json,datetime,logging,math,re , base64
from django.http import *
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.core.management import call_command
from django.core.cache import cache
from django.utils import timezone
from django.core.context_processors import csrf
from django.shortcuts import *
from django.http import *

import ods.dj_server.dj_server.status as status
import ods.dj_server.dhui.ajax_views as ajax_views
import ods.utils as utils

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

#参数异常处理装饰器
def param_except_handler(func) :
    def _param_except_handler(self,request,params) :
        result = utils.init_response_data()
        try :
            result =   func(self,request,params)
        except Exception , e :
            result['success'] = status.Status.ERROR
            result['return_code'] = status.Status().getReason(result['success'])
            ErrorLogger.error( result['return_code'] + " 错误信息 : %s"%e)
            return result
        return result
    return _param_except_handler

# 定义api view的路由类
class API_ROUTER:
    def __init__(self):
        self.name = 'xieli'

    #创建发货单
    @param_except_handler
    def __create_dhui_invoice(self,request,params) :
        return ajax_views.create_dhui_invoice(request)


# 初始化一个 API_ROUTER的对象
SERVER_API_ROUTER = API_ROUTER()

# api view 的路由参数
def api_router(request) :
    try:
        result = utils.init_response_data()
        result["success"] = status.Status.ERROR
        result["return_code"] = status.Status().getReason(result["success"])
        action,data = checkRequestMethod(request)
        data = getattr(SERVER_API_ROUTER,"_API_ROUTER__%s"%action,"default")(request,data)
    except Exception,e:
        ErrorLogger.error(str(e))
        trace_info = utils.get_trace_info()
        result["return_code"] = trace_info
        return HttpResponse(json.dumps(result),content_type="application/json")

    result.update(data)
    response = HttpResponse(json.dumps(result),content_type="application/json")
    return response

# 检查请求方法取得参数信息
def checkRequestMethod(request):
    #检查请求的方法类型
    if request.method == 'GET':
        action = request.GET['action']
        if request.GET.has_key("data"):
            params = request.GET['data']
        else :
            params = "{}"
        #模拟加密
        # param_list = [ ("password" in i ,i) for i in params.keys() ]
        # for param_tuple in param_list :
        #     if param_tuple[0] :
        #         params[param_tuple[1]] = encrypto(params[param_tuple[1]])
    elif request.method == 'POST':
        action = request.POST['action']
        if request.POST.has_key("data"):
            params = request.POST['data']
        else :
            params = "{}"
    params=json.loads(params)
    return action,params

#对指定函数进行用户在线状态检查
def check_user_status_by_views(request,action):
    keywords = [
            "login",
            "register",
            "logout",
            "get_service_version" ,
            "get_csrf_token" ,
            "send_vercode" ,
            "check_vercode" ,
            "receive_task" ,
            "check_user_exist" ,
            "reset_user_password" ,
            "init_reset_user_password" ,
            "reset_user_password_ver_code" ,
            "get_home_data" ,
            "get_object_list" ,
            "get_object_info",
            "get_comment_list",
            "get_idea_list",
            "get_clap_list",
            "get_mock_list",
            "get_vote_content",
            "get_activity_info",
            "get_sodality_info",
            "third_party_login",
            "get_user_basic_information" ,
            "collect_geography"
        ]
    for keyword in keywords :
        if action.find(keyword) != -1 :
            return Status.OK
        else:
            continue
    username = request.session.get('username',None)
    ret=checkUserOnlineStatus(request)
    if ret!=Status.OK:
        return ret
    else :
        return Status.OK

check_keyword_list = ['username', 'phone', 'email', 'user_id_info', 'friend_name']
def check_params_content_illegal(params):
    #屏蔽所有特殊字符
    #1.所有的sha1，type 字符串进行检测  保留字母或者数字
    #2.对username, password, phone, email, old_password, new_password, user_id_info, friend_name
    #3未处理接口 alter_user_info
    try:
        pattern_1 = re.compile('[^a-zA-Z0-9.]')
        pattern_2 = re.compile('[`~!#$%^&*]|(\.{2})|(\s{2})')
        for key,value in params.items():
            if 'sha1' in key or 'type' in key and type(value) == str:
                params[key] = pattern_1.sub("",value)
            elif key in check_keyword_list:
                params[key] = pattern_2.sub("",value)
            else:
                pass
        return params
    except:
        return params

#生成随机数
def createNoncestr():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    strs = []
    import random
    for x in range(16):
        strs.append(chars[random.randrange(0, len(chars))])
    return "".join(strs)

#比较函数
def compare_sign(x,y):
    if x[0]>y[0]:
        return 1
    elif x[0]<y[0]:
        return -1
    else:
        return 0
