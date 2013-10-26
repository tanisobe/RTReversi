#!/usr/bin/env python
# -*- coding=utf-8 -*-

import threading
from rtreversi.reversi import Player
from rtreversi.reversi import Board
from rtreversi.reversi import Disc


class Game():
    def __init__(self, max_player=2):
        self.__players = dict()
        self.__board = Board()
        self.__max_player = max_player
        self.__lock = threading.Lock()
        self.wait = True

    @property
    def playerCount(self):
        with self.__lock:
            return len(self.__players)

    def accept(self, handler):
        with self.__lock:
            if self.wait:
                p = Player('test', 'Black', Disc(), self.__board)
                self.__players[handler] = p
                if len(self.__players) == self.__max_player:
                    self.wait = False
                return p
            return None

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


class GameManager():
    def __init__(self):
        self.games = []
        self.__lock = threading.RLock()

    def create(self, handler):
        game = Game()
        player = game.accept(handler)
        with self.__lock:
            self.games.append(game)
            return player

    def introduce(self, handler):
        with self.__lock:
            for game in self.games:
                if game.wait:
                    return game.accept(handler)
            return self.create(handler)

    def oust(self, handler):
        with self.__lock:
            for game in self.games:
                game.refuse(handler)
