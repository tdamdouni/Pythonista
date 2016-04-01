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

"""The code that makes the AI do stuff.  Although this AI doesn't do very smart stuff."""

from Phantom.core.board import Board
from Phantom.core.coord.point import Coord
from Phantom.core.exceptions import InvalidMove, InvalidDimension, ChessError, LogicError
import random

def make_random_move(board):
    board.freeze()
    piece = random.choice(board.pieces)
    board.unfreeze()
    if len(piece.valid()) <= 0:
        return make_random_move(board)
    else:
        move = random.choice(piece.valid())
        board.game.move(piece.coord, move)
    return True
