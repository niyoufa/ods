#coding=utf-8

"""
    author : niyoufa
    date : 2016-06-25
"""

import sys, pdb, json, datetime, pymongo, urllib

import tornado.web
from tornado.httpclient import AsyncHTTPClient

import ods.tnd_server.status as status
import ods.utils as utils
import ods.tnd_server.settings as settings
import ods.tnd_server.handler as handler
import ods.clients.curl as curl

articel_cache = {}
class ArticelHandler(tornado.web.RequestHandler):
    def get(self, *args):
        url = self.get_argument("url","")
        if articel_cache.has_key(url):
            response = articel_cache[url]
        else:
            response = curl.CURL.get(url=url)
            articel_cache[url] = response
        params = {
            "page_title":"page_title",
            "header_text":"",
            "content_text":response,
        }
        self.render('newbie/articel.html',**params)

handlers = [
    (r"/newbie/articel/get",ArticelHandler),
]