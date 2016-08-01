# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.ssfw import Ssfw

class GradeCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    ssfw = Ssfw(usr, psw)
    grades = ssfw.get_grades()
    self.write(json.dumps(grades))
    # f = open('tmpgrade.json', 'r')
    # self.write(f.read())

  def post(self):
    self.write('Not Finish!')
