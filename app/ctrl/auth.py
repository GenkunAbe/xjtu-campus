# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.cas import Cas

class AuthCtrl(tornado.web.RequestHandler):

    def get(self):
        usr = self.get_argument('usr')
        psw = self.get_argument('psw')

        cas = Cas(usr, psw)
        if cas.link and len(cas.link) == 1:
            self.write(json.dumps(['True']))
        else:
            self.write(json.dumps(['False']))
    
    def post(self):
        self.write('Not Finish!')