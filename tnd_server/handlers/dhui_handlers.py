#coding=utf-8

import pdb , json , datetime , pymongo

import tornado.web

import status
import utils
from model import models

class GetGoodPartner(tornado.web.RequestHandler):
    def get(self):
        result = utils.init_response_data()

        try :
            good_id = self.get_argument("good_id")
        except Exception ,e :
            result = utils.reset_response_data(status.Status.PARMAS_ERROR, error_info=str(e))
            self.write(result)
            return


