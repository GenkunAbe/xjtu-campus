# -*- coding: utf-8 -*-

import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
from url import url

app = tornado.web.Application(url)

def init():
    if not os.path.exists("./data"):
        os.mkdir("./data")

if __name__ == '__main__':
    init()
    server = tornado.httpserver.HTTPServer(
        app, 
        ssl_options = {
            "certfile" : "server.crt",
            "keyfile" : "server.key",
        }
    )
    server.listen(12000)
    tornado.ioloop.IOLoop.instance().start()