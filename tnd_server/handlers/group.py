#coding=utf-8

"""
    author : niyoufa
    date : 2016-06-30

"""

import sys, pdb, json, datetime, pymongo, urllib

import tornado.web

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings
import ods.tnd_server.handler as handler

import ods.clients.curl as curl
import ods.clients.rong as rong

import ods.dhui.dhui_task as dt

class DhuiGroupJoinHandler(handler.APIHandler):
    #加入群组
    def post(self):
        result = utils.init_response_data()
        try:
            user_id=self.get_argument('user_id')
            group_id=self.get_argument('group_id')
            group_name=self.get_argument('group_name')
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,str(e))
            self.finish(result)
            return
      
        self.finish(result)

class DhuiGroupQuitHandler(handler.APIHandler):
    #退出群组
    def post(self):
        result = utils.init_response_data()
        try:
            user_id=self.get_argument('user_id')
            group_id=self.get_argument('group_id')
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,str(e))
            self.finish(result)
            return
        
        self.finish(result)

class DhuiGroupUserQueryHandler(handler.APIHandler):
    #查询群成员
    def get(self):
        result = utils.init_response_data()
        try:
            group_id=self.get_argument('group_id')
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,str(e))
            self.finish(result)
            return

        self.finish(result)

class DhuiGroupUserDetailQueryHandler(handler.APIHandler):
    #查询群组内所有用户的user表中的信息
    def get(self):
        result = utils.init_response_data()
        try:
            group_id=self.get_argument('group_id','')
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,str(e))
            self.finish(result)
            return

        self.finish(result)

class DhuiUserGroupQueryHandler(handler.APIHandler):
    #获取某用户所在所有群组的group_id和group_name
    def get(self):
        result = utils.init_response_data()
        try:
            user_id = self.get_argument('user_id','')
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,str(e))
            self.finish(result)
            return

        self.finish(result)


handlers = [
    (r"/odoo/api/group/join",DhuiGroupJoinHandler),
    (r"/odoo/api/group/quit",DhuiGroupQuitHandler),
    (r"/odoo/api/group/user/query",DhuiGroupUserQueryHandler),
    (r"/odoo/api/group/user/detail/query",DhuiGroupUserDetailQueryHandler),
    (r"/odoo/api/user/group",DhuiUserGroupQueryHandler),
]
