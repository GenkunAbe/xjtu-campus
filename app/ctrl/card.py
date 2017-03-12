# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
import time
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

class CardPayTestCtrl(tornado.web.RequestHandler):

  def get(self):
    self.write('{"success":true,"msg":"交易成功\n\n欢迎下次使用","obj":null}')

  def post(self):
    self.write('Not Finish!')

class CardPayCtrl(tornado.web.RequestHandler):

  def get(self):
    usr = self.get_argument('usr')
    psw = self.get_argument('psw')
    pay_psw = self.get_argument('paypsw')
    amt = self.get_argument('amt')
    card = Card(usr, psw)
    result = card.auto_pay(amt, pay_psw)

    try:
      print('%s\t%15s\tCard Pay\t%4.2f\t%s' % (
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        usr,
        float(amt),
        result
      ))
    except:
      print('%s\t%15s\tCard Pay\t%4.2f\t%s' % (
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        usr,
        float(amt),
        "Other False"
      ))

    self.write(result)

  def post(self):
    self.write('Not Finish!')
