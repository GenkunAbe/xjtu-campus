# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.card import Card

class CardCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    card = Card(usr, psw)
    info = card.get_card_info()
    self.write(json.dumps(info))

  def post(self):
    self.write('Not Finish!')
