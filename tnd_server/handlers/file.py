#coding=utf-8

"""
    author : niyoufa
    date : 2016-07-06

"""

import sys, pdb, json, datetime, pymongo, urllib
import traceback

import tornado.web
from tornado.httpclient import AsyncHTTPClient

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings
import ods.tnd_server.handler as handler

import ods.clients.mongodb_client as mongodb_client

class FileListHandler(handler.APIHandler):
    def get(self,*args,**options):
        result = utils.init_response_data()
        try:
            categ = self.get_argument("categ","")
        except Exception, e:
            error_info = traceback.format_exc()
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info)
            self.finish(result)
            return
        files_coll = mongodb_client.get_coll("files")
        query_params = {}
        if categ :
            query_params = {
                "categ" : categ,
            }
        files = files_coll.find(query_params)[0:10]
        data = []
        for file in files:
            del file["_id"]
            data.append(dict(
                files = file["files"],
                categ = file["categ"],
                create_time = file["create_time"],
            ))
        result["data"] = data
        self.finish(result)

handlers = [
    (r"/newbie/api/file/list",FileListHandler),
]
