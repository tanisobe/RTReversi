#!/usr/bin/env python
# -*- config=utf-8 -*-

from rtreversi.game import GameManager
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
import logging
log = logging.getLogger(__name__)


class RTReversiApp(tornado.web.Application):
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
        log.debug('initialize')
        (self.player, self.game) = self.application.manager.introduce(self)

    def open(self):
        log.debug('open connection')
        self.sendCommand('updateGame', json.loads(self.game.toJson()))
        self.game.update()

    def on_close(self):
        log.debug('close connection')
        self.application.manager.deleteHandler(self)
        self.game.update()

    def on_message(self, msg):
        log.debug(msg)
        m = json.loads(msg)
        setting_commands = ['changeStatus']
        game_commands = ['putDisc', 'removeDisc']
        if not self.game.wait:
            if m['command'] in game_commands:
                method = getattr(self.player, m['command'])
                if method(**m['param']):
                    if self.game.isOver():
                        self.sendCommand('finish', json.loads(self.game.toJson()))
                    self.game.update()
        else:
            if m['command'] in setting_commands:
                method = getattr(self.player, m['command'])
                if method(**m['param']):
                    self.game.start()
                    self.game.update()

    def sendCommand(self, command, param):
        j = {
            'command': command,
            'param': param
        }
        self.write_message(json.dumps(j))


def main():
    app = RTReversiApp()
    app.listen(5000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
