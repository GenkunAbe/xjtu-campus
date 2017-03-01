# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
from model.ssfw import Ssfw

class NetCtrl(tornado.web.RequestHandler):

  def get(self):
    self.write('Not Finish!')

  def post(self):
    self.write('Not Finish!')
