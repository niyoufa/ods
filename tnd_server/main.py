#coding=utf-8

import pdb , platform
import sys , os , pdb

import tornado.httpserver
import tornado.ioloop
import tornado.options

# 加载ods系统根路径
BASE_DIR = os.path.abspath(__file__)
_root = os.path.dirname(BASE_DIR)
sys.path.append(_root.split("/ods/")[0])

import ods.tnd_server.app as app
from ods.tnd_server.lib.options import parse_options
parse_options()

from tornado.options import define,options
define("port" , default=9090 , help="tornado server service port setting" , type=int)
# supervisorctl stop all

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(app.Application())
    http_server.listen(options.port)
    print "\nserver start ! \n"
    tornado.ioloop.IOLoop.instance().start()
