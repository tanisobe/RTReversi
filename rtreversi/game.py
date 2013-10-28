#!/usr/bin/env python
# -*- coding=utf-8 -*-

import threading
import json
from rtreversi.reversi import Player
from rtreversi.reversi import Board
from rtreversi.reversi import Disc


class Game():
    def __init__(self, max_player=4):
        self.__players = dict()
        self.__board = Board()
        self.__max_player = max_player
        self.__lock = threading.Lock()
        self.DISC_COLORS = ['Black', 'White', 'Red', 'Blue', 'Yellow']
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
            if len(self.__players) == self.__max_player:
                self.wait = False
            return p

    def refuse(self, handler):
        with self.__lock:
            try:
                self.__players.pop(handler)
                self.wait = True
            except KeyError:
                pass

    def start(self):
        with self.__lock:
            if not self.wait:
                for player in self.__players:
                    if not player.ready:
                        return

    def update(self):
        for handler in self.__players.keys():
            handler.updateGame()


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

    def introduce(self, handler):
        with self.__lock:
            for game in self.games:
                if game.wait:
                    return (game.accept(handler), game)
            return self.create(handler)

    def oust(self, handler):
        with self.__lock:
            for game in self.games:
                game.refuse(handler)
