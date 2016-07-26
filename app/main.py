# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
from url import url

app = tornado.web.Application(url)

if __name__ == '__main__':
    app.listen(12000)
    tornado.ioloop.IOLoop.instance().start()