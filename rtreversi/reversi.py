#! /usr/bin/env python
# -*- coding=utf-8 -*-

import threading
import random
import json
from rtreversi.error import BoardError
import logging
log = logging.getLogger(__name__)


class Board:
    def __init__(self, x_size=10, y_size=10):
        self.initialize(x_size, y_size)
        self.__lock = threading.Lock()

    def initialize(self, x_size=10, y_size=10):
        self.__surface = [[None for x in range(x_size)] for y in range(y_size)]
        for i in range(1, int(x_size * y_size * 0.05)):
            self.__surface[random.randint(0, x_size - 1)][random.randint(0, y_size - 1)] = 'Obstacle'
        self.__disc = {None: x_size * y_size}
        self.__size = x_size * y_size

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
                if self.__surface[x][y] not in [None, 'Obstacle']:
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

    def toJson(self):
        with self.__lock:
            j = {
                'surface': self.__surface,
                'disc': self.__disc
            }
            return json.dumps(j)

    def __eval(self, x, y, color):
        vectors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        plus = lambda x, y, vec: (x + vec[0], y + vec[1])
        for vec in vectors:
            capture_pos = []
            (posX, posY) = plus(x, y, vec)
            while self.onBoard(posX, posY):
                if self.__surface[posX][posY] in [None, 'Obstacle']:
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

    def isGameOver(self):
        for color, num in self.__disc.items():
            if color and 100.0 * num / self.__size > 50:
                log.debug('game is over')
                return True
        return False


class Disc:
    def __init__(self, count=5, max=10):
        self.initialize(count, max)
        self.__lock = threading.Lock()

    def initialize(self, count=5, max=10):
        self.__count = count
        self.__max = max

    @property
    def count(self):
        with self.__lock:
            return self.__count

    def increase(self, x):
        with self.__lock:
            if self.__max > self.__count:
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
    def __init__(self, id, color, disc, board):
        self.__id = id
        self.__disc = disc
        self.__board = board
        self.ready = False
        self.color = color

    def initialize(self, disc=5):
        self.__disc.initialize(5, 10)

    @property
    def id(self):
        return self.__id

    @property
    def disc(self):
        return self.__disc

    def toJson(self):
        j = {
            'id': self.__id,
            'disc': self.__disc.count,
            'ready': self.ready,
            'color': self.color
        }
        return json.dumps(j)

    def putDisc(self, x, y):
        if self.__disc.reduce(1):
            try:
                self.__board.set(x, y, self.color)
                return True
            except BoardError:
                self.__disc.increase(1)
                return False

    def removeDisc(self, x, y):
        if self.__disc.reduce(5):
            try:
                self.__board.remove(x, y)
                return True
            except BoardError:
                self.__disc.increase(5)
                return False

    def changeStatus(self, ready, color, disc, id, board_disc):
        if self.__id == id:
            log.debug(ready)
            self.ready = ready
            self.color = color
            return True
