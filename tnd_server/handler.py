# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-03-02
#

import traceback
import logging
import logging.config
import urllib
import hashlib

from tornado import escape
from tornado.options import options
from tornado.web import RequestHandler as BaseRequestHandler, HTTPError
import ods.tnd_server.exceptions as exceptions

class BaseHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        # enable GET request when enable delegate get to post
        if options.app_get_to_post:
            self.post(*args, **kwargs)
        else:
            raise exceptions.HTTPAPIError(405)

    def prepare(self):
        self.traffic_control()
        pass

    def traffic_control(self):
        # traffic control hooks for api call etc
        self.log_apicall()
        pass

    def log_apicall(self):
        pass


class RequestHandler(BaseHandler):
    pass


class APIHandler(BaseHandler):

    def get_current_user(self):
        pass

    def finish(self, chunk=None, notification=None,origin=False):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","X-Requested-With,Set-Cookie")
        self.set_header("Access-Control-Allow-Methods","PUT,DELETE,POST,GET")
        self.set_header('Content-type', 'application/x-www-form-urlencoded; charset=utf-8')
        self.set_header("Access-Control-Allow-Methods","PUT,DELETE,POST,GET")
        #设置header键值对
        if chunk is None:
            chunk = {}

        if isinstance(chunk, dict):#chunk默认情况下给chunk一个dict地址值，并执行下列步骤
            if origin != True:
                chunk = {"meta": {"code": 200}, "response": chunk}  #orgin默认情况下给chunk赋"meta"={"code":200}
                                                                        #"response"=上次的chunk的字典内容

            if notification:
                chunk["notification"] = {"message": notification}#如果notification有值则再chunk中添加notification键值对

        callback = escape.utf8(self.get_argument("callback", None))

        #self.set_header("Access-Control-Allow-Credentials",'true')

        if callback:
            self.set_header("Content-Type", "application/x-javascript; charset=utf-8;")

            if isinstance(chunk, dict):
                chunk = escape.json_encode(chunk)

            self._write_buffer = [callback, "(", chunk, ")"] if chunk else []
            super(APIHandler, self).finish()
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            super(APIHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        debug = self.settings.get("debug", False)
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]

            if isinstance(e, exceptions.HTTPAPIError):
                pass
            elif isinstance(e, HTTPError):
                e = exceptions.HTTPAPIError(e.status_code)
            else:
                e = exceptions.HTTPAPIError(500)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            if status_code == 500 and not debug:
                #self._send_error_email(exception)
                e.response["exception"] = exception

            if debug:
                e.response["exception"] = exception

            self.clear()
            self.set_status(200)  # always return 200 OK for API errors
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish(str(e))
        except Exception:
            logging.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)
'''
    def _send_error_email(self, exception):
        try:
            # send email
            subject = "[%s]Internal Server Error" % options.sitename
            body = self.render_string("errors/500_email.html",
                                      exception=exception)
            if options.send_error_email:
                email_tasks.send_email_task.delay(options.email_from,
                                                  options.admins, subject, body)
        except Exception:
            logging.error(traceback.format_exc())
'''

#带加密字段的处理器
class TokenAPIHandler(APIHandler):
    # @utils.add_token
    def __init__(self,*args,**kwargs):
        super(TokenAPIHandler,self).__init__(*args,**kwargs)

class ErrorHandler(RequestHandler):
    """Default 404: Not Found handler."""
    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise HTTPError(404)


class APIErrorHandler(APIHandler):
    """Default API 404: Not Found handler."""
    def prepare(self):
        super(APIErrorHandler, self).prepare()
        raise exceptions.HTTPAPIError(404)