# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.news import News

class NewsCtrl(tornado.web.RequestHandler):

  def get(self):
    news = News()
    self.write(json.dumps(news.ez_get()))

  def post(self):
    self.write('Not Finish!')
