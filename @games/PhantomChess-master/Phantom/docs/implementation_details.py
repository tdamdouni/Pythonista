# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

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
# R0 20150215T2214
def top(): pass
#                                           IMPLEMENTATION DETAILS


# some common abbreviations used in this file:
# in - the file, (function)|(class & method) the detail is located in
# q - the question/problem
# cs - the currently implemented solution

def detail_0(): return """
–––––––––––––––––––
 in: Chess.core.board.Board.__getitem__
 q: if there is more than one item that matches the specified parameter,
    should they all be returned in a list OR simply the first one found?
    Further, should there be a decision-making process on which one to
    return if there are more than one?
 cs: return a list of them all with no ordering
"""

def detail_1(): return """
–––––––––––––––––––
 in Chess.core.board.Board.__getitem__
 q: what should __getitem__ search?  The board's list of pieces for a coord or the board's list of tiles?
 cs: Board.pieces for a specified coord
"""

def detail_2(): return """
–––––––––––––––––––
 in: Chess.core.coord.vectored_lists
 q: should the list gens include the position of the piece itself?
 cs: no
"""

def detail_3(): return """
–––––––––––––––––––
 in: Chess.core.coord.vectored_lists
 q: should the lists returned include instances of the Coord class or the Tile class?
 cs: Coord
"""

def detail_4(): return """
–––––––––––––––––––
 in: Chess.boardio.save
 q: what should the format be to save a game to a file?
 cs: games are written to a single file containing the fields
     'name of the game': 'game FEN string'
"""

def detail_5(): return """
–––––––––––––––––––
 in: Phantom.core.pieces.ChessPiece.valid
 q: should the property list instances of Phantom.core.coord.point.Coord or Phantom.core.board.Tile?
 cs: Coord
"""

def bottom(): pass
