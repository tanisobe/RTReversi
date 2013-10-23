#! /usr/bin/env python
# -*- coding=utf-8 -*-


class BoardError(Exception):
    def __init__(self, x, y, color, surface, msg):
        self.x = x
        self.y = y
        self.color = color
        self.surface = surface
        self.msg = msg
