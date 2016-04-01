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

"""Helpers for working with directions."""

from Phantom.core.coord.vectored_lists import (north, south, east, west, ne, se, nw, sw)
from Phantom.utils.debug import call_trace

__all__ = []

@call_trace(6)
def dirfinder(piece, target):
    """Locate the direction in which the target lies and return a 2-tuple of:
        (the string of the direction,
         the function that gives it)"""
    for func in (north, south, east, west, ne, nw, se, sw):
        if target in func(piece):
            return (func.__name__, func)
    return ('unknown', lambda p: [0])
__all__.append('dirfinder')
