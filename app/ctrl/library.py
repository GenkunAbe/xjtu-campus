# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.lib import Library

class BookSearchCtrl(tornado.web.RequestHandler):

  def get(self):
    arg = self.get_argument('arg')
    lib = Library()
    books = lib.get_book_list(arg)
    self.write(json.dumps(books))


  def post(self):
    self.write('Not Finish!')

class BookDetailCrtl(tornado.web.RequestHandler):

  def get(self):
    link = self.get_argument('link')
    ff = self.get_argument('FF')
    lib = Library()
    detail = lib.get_book_detail(link, ff)
    self.write(json.dumps(detail))

  def post(self):
    self.write('Not Finish!')
