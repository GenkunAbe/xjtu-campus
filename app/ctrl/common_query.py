# -*- coding: utf-8 -*-

import tornado.web
import sys
from model.comm_qry import *

class CommonQuery(tornado.web.RequestHandler):

    def get(self):
        query_type = self.get_argument('type')
        if query_type == 'week':
            self.write(str(get_now_week()))

    def post(self):
        self.write('Not Finish!')

