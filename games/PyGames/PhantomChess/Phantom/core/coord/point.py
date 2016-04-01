# -*- coding: utf-8 -*-

#########################################################################
# This file is part of PhantomChess.                                    #
#                                                                       #
# PhantomChess is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  # 
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# PhantomChess is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with PhantomChess.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

"""Coordinate handling."""

from Phantom.constants import (screen_height, screen_width, scale_factor, grid_height, grid_width)
from Phantom.functions import round_down
from Phantom.core.chessobj import PhantomObj
from Phantom.utils.decorators import integer_args

__all__ = []

class Coord (PhantomObj):
    
    tochesskeys = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h',}

    fromchesskeys = dict(zip(tochesskeys.values(), [k-1 for k in tochesskeys.keys()]))
    
    @integer_args
    def __init__(self, *args):
        if len(args) == 1:
            c = Coord.from_chess(args[0])
            self.x = c.x
            self.y = c.y
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
    
    def __repr__(self):
        return 'Coord({}, {})'.format(self.x, self.y)
    
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    
    def __tuple__(self):
        return (self.x, self.y)
    
    def __add__(self, other):
        if not isinstance(other, Coord):
            raise TypeError('type {} cannot be added to Coord'.format(type(other)))
        return Coord(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if not isinstance(other, Coord):
            raise TypeError('type {} cannot be subtracted from Coord'.format(type(other)))
        return Coord(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Coord(self.x * other, self.y * other)
        raise TypeError('type {} cannot be multiplied by Coord'.format(type(other)))
    
    def __div__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Coord(self.x / other, self.y / other)
        raise TypeError('Coord cannot be divided by type {}'.format(type(other)))
    
    def __pow__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x ** other.x, self.y ** other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Coord(self.x ** other, self.y ** other)
        raise TypeError('Coord cannot be exponentiated to type {}'.format(type(other)))
    
    def __contains__(self, elem):
        return (elem == self.x) or (elem == self.y)
    
    def __eq__(self, other):
        if isinstance(other, Coord):
            return (self.x == other.x) and (self.y == other.y)
        elif isinstance(other, tuple):
            return self.__eq__(Coord(other[0], other[1]))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __ge__(self, other):
        raise TypeError('type {} cannot be compared with type Coord'.format(type(other)))
    
    def __le__(self, other):
        raise TypeError('type {} cannot be compared with type Coord'.format(type(other)))
    
    def __gt__(self, other):
        raise TypeError('type {} cannot be compared with type Coord'.format(type(other)))
    
    def __lt__(self, other):
        raise TypeError('type {} cannot be compared with type Coord'.format(type(other)))
    
    def __len__(self):
        return 2  # coordinates are made of 2 values (x and y)
    
    def __hash__(self):
        return (self.x + 2) ** (self.y + 2)
    
    def as_tup(self):
        return self.__tuple__()
    
    def as_chess(self):
        if not ((0 <= self.x < grid_width) or (0 <= self.y < grid_height)):
            raise ValueError('{} is outside of grid and cannot be converted to chess notation'.format(repr(self)))
        x = self.tochesskeys[self.x+1]
        y = self.y + 1
        return x + str(y)
    
    def as_coord(self):
        # return a coordinate that starts counting at 1 instead
        # of the default 0
        return Coord(self.x + 1, self.y + 1)
    
    def as_screen(self):
        y = self.y * scale_factor
        excess_x = (screen_width) - (grid_width * scale_factor)
        offset_x = excess_x / 2
        x = offset_x + (self.x * scale_factor)
        return Coord(x, y)
    
    @classmethod
    def from_chess(klass, chess):
        if chess == '-':
            return Coord(None, None)
        x = klass.fromchesskeys[chess[0]]
        y = int(chess[1])
        return Coord(x, y - 1)
    
    @classmethod
    def from_screen(klass, scr):
        y = round_down(scr.y / float(scale_factor))
        x = round_down((scr.x - 128) / float(scale_factor))
        return Coord(x, y)
__all__.append('Coord')


class Grid (object):
    
    def __init__(self, c1, c2, c3, c4):
        
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.max_x = max(c1.x, c2.x, c3.x, c4.x)
        self.max_y = max(c1.y, c2.y, c3.y, c4.y)
        self.min_x = min(c1.x, c2.x, c3.x, c4.x)
        self.min_y = min(c1.y, c2.y, c3.y, c4.y)
    
    def __len__(self):
        return (self.max_x - self.min_x) * (self.max_y - min_y)
    
    def __contains__(self, point):
        x_t = self.min_x <= point.x <= self.max_x
        y_t = self.min_y <= point.y <= self.max_y
        return x_t and y_t
__all__.append('Grid')

bounds = Grid(Coord(0, 0), Coord(0, 7), Coord(7, 0), Coord(7, 7))
__all__.append('bounds')

