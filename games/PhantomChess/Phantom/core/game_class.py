#!/usr/bin/env python
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

"""The class that holds a complete game of Chess.

Generally, use this class rather than Phantom.core.board.Board, because this class
keeps track of history, which Board doesn't."""

"""
ChessGame
    Has one Board
        Has one players     [Player, Player]
        Has one tiles_dict  {fen_loc : Tile}
        Has one pieces_dict {fen_loc : ChessPiece}
        ### Has one graveyard   []

ChessGame.__init__(ChessGame, fen_str=None)
Board.__init__(fen_str=None)
Player.__init__(Board, color)
Tile.__init__(color, fen_loc)
ChessPiece.__init__(Player, fen_loc)
"""

import sys
import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.core.board import Board # , load as _load_board
from Phantom.boardio.load import load_game as load_board_fen
#from Phantom.core.players import Player
from Phantom.utils.debug import call_trace  # , log_msg

__all__ = []

def load_game(name):
    return ChessGame(load_board_fen(name))

class ChessGame (PhantomObj):
    def __init__(self, fen_str=None):
        self.board = Board(self, fen_str)
        self._uuid = self.board._uuid
        self.data = dict()
        self.history = []
        self.moves = []
        #try:  # autostart the gui?
        #    import sk
        #    self.sk_gui()
        #except ImportError:
        #    pass

    def __repr__(self):
        return self.board._pprnt()

    def __hash__(self):
        return int(self._uuid) % (self.board.__hash__() + 1)

    @property
    def ai_rateing(self):
        from Phantom.ai.pos_eval.advanced import pos_eval_advanced
        return pos_eval_advanced(self.board)

    def ai_easy(self):
        from Phantom.ai.movers.basic import make_random_move
        return make_random_move(self.board)

    def ai_hard(self):
        from Phantom.ai.movers.advanced import make_smart_move
        return make_smart_move(self.board)

    def move(self, *args):
        save_fen_str = self.board.as_fen_str()
        ret = self.board.move(*args)
        if ret:
            self.history.append(save_fen_str)
            self.moves.append(self.board.lastmove)
        return ret

    def castle(self, *args):
        self.history.append(self.board.as_fen_str())
        self.board.castle(*args)

    def promote(self, *args):
        self.history.append(self.board.as_fen_str())
        self.board.promote(*args)

    def clone(self):
        fen = self.board.as_fen_str()
        history = self.history
        cfg = self.board.cfg
        data = self.board.data
        sdata = self.data
        moves = self.moves
        #clone = ChessGame(self.player1, self.player2, Board(self.player1, self.player2, fen))
        clone = ChessGame(Board(self.board.players, fen))
        clone.history = history
        clone.board.cfg = cfg
        clone.board.data = data
        clone.data = sdata
        clone.moves = moves
        return clone

    def rollback(self):
        fen = self.history[-1]
        data = self.board.data
        cfg = self.board.cfg
        #self.player1 = self.board.player1
        #self.player2 = self.board.player2
        #self.board = Board(self.player1, self.player2, fen)
        self.board = Board(self.players, fen)
        self.board.data = data
        self.board.cfg = cfg

    def scene_gui(self):
        """Spawn a scene-based GUI for the game.
           **Only works in Pythonista, on other platforms prints an error message."""
        try:
            import scene
            from Phantom.gui_pythonista.game_view import GameView
            self.gui = GameView(self)
        except ImportError as e:
            print(e)
            #sys.exit('Pythonista scene module not found!')

    def sk_gui(self):
        """Spawn a sk-based GUI for the game.
           **Only works in Pythonista v1.6+, on other platforms prints an error message."""
        try:
            import sk  # only available in Pythonista
            from Phantom.sk_gui.SkChessView import SkChessView
            self.gui = SkChessView(self)
        except ImportError as e:
            print(e)
            #sys.exit('Pythonista sk module not found!')

    @call_trace(3)
    def is_won(self):
        """Tell if the game is won.  Returns one of [False, 'white', 'black']."""
        kings = self.board.get_piece_list(ptype='king')
        if len(kings) == 1:
            return kings[0].color  # the last king left standing wins

        for king in kings:
            if not king.all_valid_moves and king.threatened_by:
                return C.opposite_color(king.color)  # checkmate!

        return False

__all__.append('ChessGame')

if __name__ == '__main__':
    #g = ChessGame('Long Endgame 1')
    g = load_game('Long Endgame 1')
    print(g)
    g.board.cfg.disp_sqrs = False
    print(g)
