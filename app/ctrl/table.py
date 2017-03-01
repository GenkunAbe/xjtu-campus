# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
from model.ssfw import Ssfw

class TableCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    ssfw = Ssfw(usr, psw)
    table = ssfw.get_table()
    self.write(json.dumps(table))
    # f = open('tmptable.json', 'r')
    # self.write(f.read())

  def post(self):
    self.write('Not Finish!')
