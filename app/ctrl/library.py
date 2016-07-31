# -*- coding: utf-8 -*-

import tornado.web
import sys
import json
sys.path.append('..')
from model.lib import Library

class LibraryCtrl(tornado.web.RequestHandler):

  def get(self):
    arg = self.get_argument('arg')
    lib = Library()
    books = lib.get_book_list(arg)
    self.write(json.dumps(books))
    

  def post(self):
    self.write('Not Finish!')
