#! /usr/bin/env python
# -*- coding=utf-8 -*-

import unittest
from rtreversi.reversi import Board
from rtreversi.reversi import Disc
from rtreversi.reversi import Player
from rtreversi.error import BoardError


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(x_size=8, y_size=8)

    def test_surface(self):
        self.assertEqual(self.board.surface(1, 4), None)

    def test_set(self):
        self.board.set(1, 4, 'Black')
        self.assertEqual(self.board.surface(1, 4), 'Black')
        with self.assertRaises(BoardError):
            self.board.set(100, 4, 'Black')
        with self.assertRaises(BoardError):
            self.board.set(1, 1, None)

    def test_cross(self):
        self.board.set(1, 4, 'Black')
        self.board.set(2, 4, 'White')
        self.board.set(3, 4, 'White')
        self.board.set(4, 4, 'Black')
        self.assertEqual(self.board.surface(2, 4), 'Black')
        self.assertEqual(self.board.surface(3, 4), 'Black')
        self.assertEqual(self.board.disc('Black'), 4)
        self.assertEqual(self.board.disc('White'), 0)
        self.assertEqual(self.board.disc(None), 60)

    def test_remove(self):
        self.board.set(1, 4, 'Black')
        self.assertEqual(self.board.disc('Black'), 1)
        self.assertEqual(self.board.disc(None), 63)
        self.assertEqual(self.board.surface(1, 4), 'Black')
        self.board.remove(1, 4)
        self.assertEqual(self.board.disc('Black'), 0)
        self.assertEqual(self.board.disc(None), 64)
        self.assertEqual(self.board.surface(1, 4), None)
        with self.assertRaises(BoardError):
            self.board.remove(100, 4)
        with self.assertRaises(BoardError):
            self.board.remove(1, 1)

    def test_disc(self):
        self.assertEqual(self.board.disc('Red'), 0)

    def test_onBoard(self):
        self.assertFalse(self.board.onBoard(10, 20))
        self.assertFalse(self.board.onBoard(-1, 0))
        self.assertTrue(self.board.onBoard(0, 3))


class TestDisc(unittest.TestCase):
    def setUp(self):
        self.disc5 = Disc(count=5)

    def test_increase(self):
        self.assertTrue(self.disc5.increase(1))
        self.assertEqual(self.disc5.count, 6)
        empty = Disc(count=0)
        self.assertEqual(empty.count, 0)
        self.assertTrue(empty.increase(1))

    def test_reduce(self):
        self.assertTrue(self.disc5.reduce(1))
        self.assertEqual(self.disc5.count, 4)
        self.assertFalse(self.disc5.reduce(32))
        self.assertEqual(self.disc5.count, 4)
        self.assertTrue(self.disc5.reduce(4))


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.disc10 = Disc(count=10)
        self.empty_disc = Disc(count=0)
        self.board = Board()
        self.player = Player('black', 'Black', self.disc10, self.board)
        self.empty_player = Player('white', 'White', self.empty_disc, self.board)

    def test_putDisc(self):
        self.player.putDisc(2, 3)
        self.assertEqual(self.disc10.count, 9)
        self.assertEqual(self.board.surface(2, 3), 'Black')
        self.player.putDisc(2, 3)
        self.assertEqual(self.disc10.count, 9)
        self.player.putDisc(10, 3)
        self.assertEqual(self.disc10.count, 9)
        self.empty_player.putDisc(2, 4)
        self.assertEqual(self.empty_disc.count, 0)
        self.assertEqual(self.board.surface(2, 4), None)

    def test_removeDisc(self):
        self.player.putDisc(2, 3)
        self.player.removeDisc(2, 3)
        self.assertEqual(self.disc10.count, 4)
        self.assertEqual(self.board.surface(2, 3), None)
        self.disc10.increase(6)
        self.player.removeDisc(2, 3)
        self.assertEqual(self.disc10.count, 10)


if __name__ == '__main__':
    unittest.main()
