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

class LinkHandler(handler.APIHandler):
    def post(self):
        result = utils.init_response_data()
        try:
            categ = self.get_argument("categ","")
            name = self.get_argument("name","")
            url = self.get_argument("url","")
        except Exception, e:
            error_info = traceback.format_exc()
            result = utils.reset_response_data(status.Status.PARMAS_ERROR,error_info)
            self.finish(result)
            return
        link_coll = mongodb_client.get_coll("links")
        query_params = {
            "url" : url
        }
        link = link_coll.find_one(query_params)
        if link:
            link["name"] = name
            link["categ"] = categ
            link_coll.save(link)
        else:
            link = dict(
                name = name,
                categ = categ,
                url = url,
            )
            link_coll.insert_one(link)
        self.finish(result)

class LinkListHandler(handler.APIHandler):
    def get(self):
        result = utils.init_response_data()
        result["data"] = []
        link_coll = mongodb_client.get_coll("links")
        links = link_coll.find()
        for link in links :
            result["data"].append(dict(
                name = link["name"],
                categ = link["categ"],
                url = link["url"],
            ))
        self.finish(result)




handlers = [
    (r"/newbie/api/link/post",LinkHandler),
    (r"/newbie/api/link/list",LinkListHandler),
]
