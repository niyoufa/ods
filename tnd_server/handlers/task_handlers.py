#coding=utf-8

import sys, pdb, json, datetime, pymongo, urllib

import tornado.web
from tornado.httpclient import AsyncHTTPClient

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings
import ods.tnd_server.handler as handler

import ods.dhui.dhui_task as dt


class DhuiTaskList(handler.APIHandler):
    def get(self,*args,**options):
        result = utils.init_response_data()
        try:
            user_id = self.get_argument("user_id")
        except Exception, e:
            result = utils.reset_response_data(status.Status.PARMAS_ERROR)
            self.finish(result)
            return
        task_list = dt.get_task_list(user_id=user_id)
        result["data"] = []
        for task in task_list :
            result["data"].append(task)
        self.finish(result)


handlers = [
    (r"/odoo/api/task/list",DhuiTaskList),
]