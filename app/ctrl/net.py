# -*- coding: utf-8 -*-

from tornado.web
import sys
import json
sys.path.append('..')
from model.ssfw import Ssfw

class NetCtrl(tornado.web.RequestHandler):

  def get(self):
    self.write('Not Finish!')

  def post(self):
    self.write('Not Finish!')
