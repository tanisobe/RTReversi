#!/usr/bin/env python
# -*- coding=utf-8 -*-

import unittest
from mock import MagicMock
from rtreversi.game import Game
from rtreversi.game import GameManager


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.handler = MagicMock()

    def test_accept(self):
        self.game.accept(self.handler)
        self.assertEqual(self.game.playerCount, 1)

    def test_refuse(self):
        self.game.accept(self.handler)
        self.game.refuse(self.handler)
        self.assertEqual(self.game.playerCount, 0)


class TestCameManager(unittest.TestCase):
    def setUp(self):
        self.gm = GameManager()
        self.handler1 = MagicMock()
        self.handler2 = MagicMock()
        self.handler3 = MagicMock()

    def test_introduce(self):
        self.gm.introduce(self.handler1)
        self.assertEqual(len(self.gm.games), 1)
        self.gm.introduce(self.handler2)
        self.assertEqual(len(self.gm.games), 1)
        self.gm.introduce(self.handler3)
        self.assertEqual(len(self.gm.games), 2)

    def test_oust(self):
        self.gm.introduce(self.handler1)
        self.gm.introduce(self.handler2)
        self.gm.introduce(self.handler3)
        self.gm.oust(self.handler1)
        self.assertEqual(self.gm.games[0].playerCount, 1)
        self.gm.introduce(self.handler1)
        self.assertEqual(self.gm.games[0].playerCount, 2)

if __name__ == '__main__':
    unittest.main()
