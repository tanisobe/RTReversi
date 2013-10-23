#! /usr/bin/env python
# -*- coding=utf-8 -*-

import threading
from rtreversi.error import BoardError


class Board:
    def __init__(self, x_size=8, y_size=8):
        self.__surface = [[None for x in range(x_size)] for y in range(y_size)]
        self.__disc = {None: x_size * y_size}
        self.__lock = threading.Lock()

    def surface(self, x, y):
        with self.__lock:
            return self.__surface[x][y]

    def disc(self, color):
        try:
            return self.__disc[color]
        except KeyError:
            return 0

    def set(self, x, y, color):
        with self.__lock:
            if self.onBoard(x, y):
                if self.__surface[x][y] is None and color is not None:
                    self.__disc[None] -= 1
                    if color in self.__disc.keys():
                        self.__disc[color] += 1
                    else:
                        self.__disc[color] = 1
                    self.__surface[x][y] = color
                    self.__eval(x, y, color)
                else:
                    raise BoardError(x, y, color, self.__surface[x][y], 'put disc on no empty point or color is None')
            else:
                raise BoardError(x, y, color, 'Unknown', 'out of board')

    def remove(self, x, y):
        with self.__lock:
            if self.onBoard(x, y):
                if self.__surface[x][y] is not None:
                    self.__disc[self.__surface[x][y]] -= 1
                    self.__disc[None] += 1
                    self.__surface[x][y] = None
                else:
                    raise BoardError(x, y, 'Unknown', self.__surface[x][y], 'remove disc from empty point')
            else:
                raise BoardError(x, y, 'Unknown', 'Unknown', 'out of board')

    def onBoard(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            self.__surface[x][y]
            return True
        except IndexError:
            return False

    def __eval(self, x, y, color):
        vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        plus = lambda x, y, vec: (x + vec[0], y + vec[1])
        for vec in vectors:
            capture_pos = []
            (posX, posY) = plus(x, y, vec)
            while self.onBoard(posX, posY):
                if self.__surface[posX][posY] is None:
                    break
                elif self.__surface[posX][posY] == color:
                    for cp in capture_pos:
                        self.__disc[self.__surface[cp[0]][cp[1]]] -= 1
                        self.__disc[color] += 1
                        self.__surface[cp[0]][cp[1]] = color
                    break
                else:
                    capture_pos.append((posX, posY))
                (posX, posY) = plus(posX, posY, vec)


class Disc:
    def __init__(self, count=32):
        self.__count = count
        self.__lock = threading.Lock()

    @property
    def count(self):
        return self.__count

    def increase(self, x):
        with self.__lock:
            if self.__count > 0:
                self.__count += x
                return True
            else:
                return False

    def reduce(self, x):
        with self.__lock:
            if self.__count - x >= 0:
                self.__count -= x
                return True
            else:
                return False


class Player:
    def __init__(self, name, color, disc, board):
        self.__name = name
        self.__disc = disc
        self.__board = board
        self.color = color

    def initialize(self, disc, board):
        self.__disc = disc
        self.__board = board

    @property
    def name(self):
        return self.__name

    def putDisc(self, x, y):
        if self.__disc.reduce(1):
            try:
                self.__board.set(x, y, self.color)
            except BoardError:
                self.__disc.increase(1)

    def removeDisc(self, x, y):
        if self.__disc.reduce(5):
            try:
                self.__board.remove(x, y)
            except BoardError:
                self.__disc.increase(5)
