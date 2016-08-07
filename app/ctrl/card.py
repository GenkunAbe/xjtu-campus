# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.card import Card

class CardInfoCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    card = Card(usr, psw)
    info = card.get_card_info()
    self.write(json.dumps(info))

  def post(self):
    self.write('Not Finish!')

class CardPreCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    card = Card(usr, psw)
    pic = card.preprocess()
    print 'Get pic success.'
    self.write(pic.read())

  def post(self):
    self.write('Not Finish!')

class CardPostCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    raw_psw = self.get_argument('rawpsw')
    code = self.get_argument('code')
    amt = self.get_argument('amt')
    card = Card(usr, psw)
    result = card.postprocess(raw_psw, code, amt)
    self.write(result)

  def post(self):
    self.write('Not Finish!')

class CardChangeCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    card = Card(usr, psw)
    pic = card.change_code_pic()
    print 'Change pic success.'
    self.write(pic.read())

  def post(self):
    self.write('Not Finish!')
