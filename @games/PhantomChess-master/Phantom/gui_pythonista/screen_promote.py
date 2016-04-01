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

"""The screen that allows users to select a piece to promote a pawn to."""

import scene
import os

from Phantom.core.game_class import ChessGame
from Phantom.core.pieces import Rook, Bishop, Knight, Queen
#from Phantom.core.coord.point import Coord
from Phantom.core.chessobj import PhantomObj
from Phantom.constants import phantom_dir  #, scale_factor, screen_width, screen_height

class ChessPromoteScreen (scene.Scene, PhantomObj):

    def __init__(self, game_view):
        self.game_view = game_view

    def setup(self):
        # Determine which pawn is being promoted and set up the options
        board = self.game_view.game.board
        self.turn = board.turn
        for p in board.pieces:
            if p.is_promotable:
                self.promoter = p
                self.color = p.color  # this syntax is a bit mind numbing
        if not hasattr(self, 'promoter'):
            del self  # ???
            #self.parent.switch_scene(self.game.data['screen_main'])
        self.owner = self.promoter.owner
        y = 7 if self.color == 'white' else 0
        self.spawncoord = Coord(self.promoter.coord.x, y)
        qpos, rpos, bpos, kpos = [Coord(x, 4) for x in (2, 3, 4, 5)]
        self.queen = Queen(qpos, self.color, self.promoter.owner)
        self.rook = Rook(rpos, self.color, self.promoter.owner)
        self.bishop = Bishop(bpos, self.color, self.promoter.owner)
        self.knight = Knight(kpos, self.color, self.promoter.owner)
        self.pieces = [self.queen, self.rook, self.bishop, self.knight]

        self.qrect = scene.Rect(self.queen.coord.as_screen.x,
                                self.queen.coord.as_screen.y,
                                scale_factor, scale_factor)
        self.rrect = scene.Rect(self.rook.coord.as_screen.x,
                                self.rook.coord.as_screen.y,
                                scale_factor, scale_factor)
        self.brect = scene.Rect(self.bishop.coord.as_screen.x,
                                self.bishop.coord.as_screen.y,
                                scale_factor, scale_factor)
        self.krect = scene.Rect(self.knight.coord.as_screen.x,
                                self.knight.coord.as_screen.y,
                                scale_factor, scale_factor)

        piece_types = [p.ptype for p in self.pieces]
        self.img_names = self.game_view.load_images(piece_types)

    def touch_began(self, touch):
        if touch.location in self.qrect:
            selected = self.queen
        elif touch.location in self.rrect:
            selected = self.rook
        elif touch.location in self.brect:
            selected = self.bishop
        elif touch.location in self.krect:
            selected = self.knight
        else:
            selected = None

        if selected:
            self.promote(selected.fen_char.upper())
            print('b del')
            del self # ???
            print('a del')
            #self.parent.switch_scene(self.game.data['screen_main'])

    def promote(self, fen_char):
        print('promoting', fen_char)
        self.game_view.game.board.promote(self.promoter.coord, fen_char)
        print('promoted ', fen_char)

    def draw(self):
        scene.background(0, 0, 0)
        for piece in self.pieces:
            img = self.img_names[piece.pythonista_gui_img_name]
            pos = piece.coord.as_screen
            scene.image(img, pos.x, pos.y, scale_factor, scale_factor)
        tpos = Coord(screen_width/2, screen_height/2 + 2*scale_factor)
        scene.text('Select a piece to promote to', x=tpos.x, y=tpos.y)

if __name__ == '__main__':
    import Phantom as P
    g = ChessGame('Long Endgame 1')
    # add a piece to test the promotion mechanism
    g.board.pieces.add(P.Pawn(P.Coord(0, 1), 'black', g.board.player2))
    g.gui()
