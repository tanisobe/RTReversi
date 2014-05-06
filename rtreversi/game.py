#!/usr/bin/env python
# -*- coding=utf-8 -*-

import threading
import time
import json
from rtreversi.reversi import Player
from rtreversi.reversi import Board
from rtreversi.reversi import Disc
import logging
log = logging.getLogger(__name__)


class Game():
    def __init__(self, max_player=4):
        self.__players = dict()
        self.__board = Board()
        self.__max_player = max_player
        self.__lock = threading.Lock()
        self.DISC_COLORS = ['Black', 'White', 'Red', 'Blue', 'Yellow']
        self.__timer = None
        self.wait = True

    @property
    def playerCount(self):
        with self.__lock:
            return len(self.__players)

    def toJson(self):
        pjson = []
        for player in self.__players.values():
            pjson.append(json.loads(player.toJson()))
        bjson = self.__board.toJson()
        j = {
            'players': pjson,
            'board': json.loads(bjson)
        }
        return json.dumps(j)

    def accept(self, handler):
        with self.__lock:
            p = Player(len(self.__players), self.DISC_COLORS[len(self.__players)], Disc(), self.__board)
            self.__players[handler] = p
            return p

    def delete(self, handler):
        if not self.wait and self.__timer is not None:
            self.__timer.stop()

        with self.__lock:
            try:
                self.__players.pop(handler)
                self.wait = True
            except KeyError:
                pass

    def start(self):
        self.__timer = GameTimer(self)
        with self.__lock:
            for  player in self.__players.values():
                if not player.ready:
                    return
            self.wait = False
            self.__board.initialize()
            for player in self.__players.values():
                player.initialize()
            self.__timer.start()
            log.debug('start game')

    def update(self):
        for handler in self.__players.keys():
            handler.sendCommand('updateGame', json.loads(self.toJson()))

    def increaseDisc(self, x):
        for player in self.__players.values():
            player.disc.increase(x)
            self.update()

    def isOver(self):
        if self.__board.isGameOver():
            for  p in self.__players.values():
                p.ready = False
            self.wait = True
            return True
        return False

    def isFull(self):
        if len(self.__players) > self.__max_player:
            return True
        return False


class GameManager():
    def __init__(self):
        self.games = []
        self.__lock = threading.RLock()

    def create(self, handler):
        game = Game()
        player = game.accept(handler)
        with self.__lock:
            self.games.append(game)
            return (player, game)

    def deleteHandler(self, handler):
        with self.__lock:
            for game in self.games:
                game.delete(handler)

    def introduce(self, handler):
        with self.__lock:
            for game in self.games:
                if game.wait and not game.isFull():
                    return (game.accept(handler), game)
            return self.create(handler)


class GameTimer(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.__stop = threading.Event()
        self.__game = game

    def run(self):
        while not self.__stop.isSet():
            if self.__game.isOver():
                return True
            time.sleep(2.5)
            self.__game.increaseDisc(1)

    def stop(self):
        self.__stop.set()
