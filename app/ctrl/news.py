# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.ssfw import Ssfw

class NewsCtrl(tornado.web.RequestHandler):

  def get(self):
    self.write('Not Finish!')

  def post(self):
    self.write('Not Finish!')
