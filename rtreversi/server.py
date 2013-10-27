#!/usr/bin/env python
# -*- config=utf-8 -*-

from rtreversi.game import GameManager
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json


class WTReversiApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/reversi", ReversiHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.manager = GameManager()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages='hello, world')


class ReversiHandler(tornado.websocket.WebSocketHandler):
    def initialize(self):
        print 'initialize'
        self.player = self.application.manager.introduce(self)

    def open(self):
        print 'open connection'
        j = {
            'command': 'init',
            'param': 'initialize'
        }
        self.write_message(json.dumps(j))

    def on_close(self):
        print 'close connection'
        self.application.manager.delete(self)

    def on_message(self, msg):
        print msg


def main():
    app = WTReversiApp()
    app.listen(5000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
