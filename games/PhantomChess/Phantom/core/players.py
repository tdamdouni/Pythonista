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

"""Player class."""

import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.core.pieces import ChessPiece
from Phantom.core.exceptions import LogicError
from Phantom.utils.debug import call_trace, log_msg
from Phantom.utils.timer import Timer
import contextlib
import uuid

__all__ = []

# 671: This shouldn't be needed anymore
'''
class Side (PhantomObj):

    def __init__(self, color):
        if isinstance(color, Side):
            self.color = color.color
            self.tilecolor = color.tilecolor
            return
        if 'w' in color.lower():
            self.color = 'white'
        elif 'b' in color.lower():
            self.color = 'black'
        else:
            raise LogicError("Couldn't identify color: {}".format(color),
                             'Phantom.core.players.Side.__init__()')
        self.tilecolor = C.grid_colors[self.color]

    def __eq__(self, other):
        if isinstance(other, Side):
            return self.color == other.color
        elif isinstance(other, (str, unicode)):
            return self.color == other
        else:
            raise TypeError("Side can't be compared with type {}".format(type(other)))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Side('{}')".format(self.color)

    def __hash__(self):
        return 1 if self.color == 'white' else 0

    def opposite(self):
        return 'black' if self.color == 'white' else 'white'
__all__.append('Side')
'''

class Player (PhantomObj):

    #isFrozen = False  # this would freeze ALL players at once
    #total_moves = 0   # this is the count of ALL moves and is better kept be the board

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.score = 0
        #self.remaining_pieces = 16
        #self.pawns = 8
        #self.knights = 2
        #self.rooks = 2
        #self.bishops = 2
        #self.kings = 1
        #self.queens = 1
        self.moves = 0
        #self.owned_pieces = set()
        self.timer = Timer(self.color == 'white')  # start the clock if player is white
        self._uuid = uuid.uuid4()

    def __repr__(self):
        return "Player('{}')".format(self.color)

    #@call_trace(5)
    @property
    def is_my_turn(self):
        return self.color == self.board.turn

    '''
    def _update(self):
        self.remaining_pieces = (self.pawns +
                                 self.knights +
                                 self.rooks +
                                 self.bishops +
                                 self.kings +
                                 self.queens)
    '''

    # Do players need to make / own their pieces?
    def make_piece(self, fen_loc, fen_char):
        cls = ChessPiece.type_from_chr(fen_char)
        piece = cls(self, fen_loc)
        #self.add_owned_piece(piece)
        return piece

    def z_add_owned_piece(self, p):
        #freeze:wasfrozen = False
        #freeze:if self.isFrozen:
        #freeze:    wasfrozen = True
        #freeze:    self.unfreeze()
        self.owned_pieces.add(p)
        self._update()
        #freeze:if wasfrozen:
        #freeze:    self.freeze()

    #freeze:def freeze(self):
    #freeze:    self.isFrozen = True
    #freeze:    self.owned_pieces = list(self.owned_pieces)

    #freeze:def unfreeze(self):
    #freeze:    self.isFrozen = False
    #freeze:    self.owned_pieces = set(self.owned_pieces)

    #freeze:@contextlib.contextmanager
    #freeze:def frozen(self):
    #freeze:    self.freeze()
    #freeze:    yield
    #freeze:    self.unfreeze()

    def z_premove(self):
        if not self.is_my_turn():
            return
        else:
            #freeze:self.freeze()
            self._update()

    def postmove(self):
        #freeze:self.unfreeze()
        #self._update()
        self.moves += 1
        self.total_moves += 1

    def set_board(self, board):
        self.board = board

    def lose_piece(self, piece):
        with self.frozen():
            if piece.ptype == 'pawn':
                self.pawns -= 1
            elif piece.ptype == 'knight':
                self.knights -= 1
            elif piece.ptype == 'rook':
                self.rooks -= 1
            elif piece.ptype == 'bishop':
                self.bishops -= 1
            elif piece.ptype == 'king':
                self.kings -= 1
            elif piece.ptype == 'queen':
                self.queens -= 1
            self._update()

    @call_trace(3)
    def validate_move(self, srce, dest):
        piece = self.board[srce]
        canmove = piece.is_move_valid(dest)
        if self.board.cfg.do_checkmate:
            check = not self.board.will_checkmate(srce, dest)
        else:
            check = True
        log_msg('validatemove: piece={}, check={}, canmove={}'.format(
                               piece,    check,    canmove), 3)
        return check and canmove

    #@call_trace(2)
    #def make_move(self, p1, p2):
    #    with self.board.frozen():
    #        piece = self.board[p1]
    #        piece.move(p2)
    #        del self.board.pieces_dict[p1]
            
            
__all__.append('Player')

if __name__ == '__main__':
    print('=' * 20)
    p = Player(None, 'white')
    print(p)
