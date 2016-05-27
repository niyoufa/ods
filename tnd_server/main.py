#coding=utf-8

import pdb , platform
import sys , os , pdb
BASE_DIR = os.path.abspath(__file__)
_root = os.path.dirname(BASE_DIR)
sys.path.append(_root)

import tornado.httpserver
import tornado.ioloop
import tornado.options

import app
import lib.options
from lib.options import parse_options

from tornado.options import define, options

if __name__ == "__main__":
    parse_options()
    http_server = tornado.httpserver.HTTPServer(app.Application())
    http_server.listen(options.SERVER_PORT)
    print "\nserver start ! \n"
    tornado.ioloop.IOLoop.instance().start()