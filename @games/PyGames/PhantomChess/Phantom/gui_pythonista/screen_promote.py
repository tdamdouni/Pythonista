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

"""The screen that allows users to select a piece to promote a pawn to."""

import scene
import os

from Phantom.core.game_class import ChessGame
from Phantom.core.pieces import Rook, Bishop, Knight, Queen
from Phantom.core.coord.point import Coord
from Phantom.core.chessobj import PhantomObj
from Phantom.constants import phantom_dir, scale_factor, screen_width, screen_height

class ChessPromoteScreen (scene.Scene, PhantomObj):
    
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        if self.parent is not None:
            self.parent.set_promote_scene(self)
    
    def setup(self):
        # Determine which pawn is being promoted and set up the options
        self.turn = self.game.board.turn
        for p in self.game.board.pieces:
            if p.is_promotable:
                self.promoter = p
                self.color = p.color
        if not hasattr(self, 'promoter'):
            self.parent.switch_scene(self.game.data['screen_main'])
        self.owner = self.promoter.owner
        y = 7 if p.color == 'white' else 0
        self.spawncoord = Coord(self.promoter.coord.x, y)
        qpos, rpos, bpos, kpos = [Coord(x, 4) for x in [2, 3, 4, 5]]
        self.queen = Queen(qpos, self.color, self.promoter.owner)
        self.rook = Rook(rpos, self.color, self.promoter.owner)
        self.bishop = Bishop(bpos, self.color, self.promoter.owner)
        self.knight = Knight(kpos, self.color, self.promoter.owner)
        self.pieces = [self.queen, self.rook, self.bishop, self.knight]
        self.selected = None
        
        self.qrect = scene.Rect(self.queen.coord.as_screen().x,
                                self.queen.coord.as_screen().y,
                                scale_factor, scale_factor)
        self.rrect = scene.Rect(self.rook.coord.as_screen().x,
                                self.rook.coord.as_screen().y,
                                scale_factor, scale_factor)
        self.brect = scene.Rect(self.bishop.coord.as_screen().x,
                                self.bishop.coord.as_screen().y,
                                scale_factor, scale_factor)
        self.krect = scene.Rect(self.knight.coord.as_screen().x,
                                self.knight.coord.as_screen().y,
                                scale_factor, scale_factor)
        
        files = [p.pythonista_gui_imgname for p in self.pieces]
        readfiles = [os.path.join(phantom_dir, 'gui_pythonista', 'imgs', f) for f in files]

        img_names = {}
        for file in readfiles:
            name = os.path.split(file)[1]
            img = scene.load_image_file(file)
            img_names.update({name: img})
        self.img_names = img_names
    
    def set_parent(self, s):
        self.parent = s
        self.parent.set_promote_scene(self)
    
    def touch_began(self, touch):
        if touch.location in self.qrect:
            self.selected = self.queen
        elif touch.location in self.rrect:
            self.selected = self.rook
        elif touch.location in self.brect:
            self.selected = self.bishop
        elif touch.location in self.krect:
            self.selected = self.knight
        
        if self.selected:
            self.promote()
            self.parent.switch_scene(self.game.data['screen_main'])
        
    def promote(self):
        self.game.board.promote(self.promoter.coord, self.selected.fen_char.upper())

    def draw(self):
        scene.background(0, 0, 0)
        for i, piece in enumerate(self.pieces):
            img = self.img_names[piece.pythonista_gui_imgname]
            pos = piece.coord.as_screen()
            scene.image(img, pos.x, pos.y, scale_factor, scale_factor)
        tpos = Coord(screen_width/2, screen_height/2 + 2*scale_factor)
        scene.text('Select a piece to promote to', x=tpos.x, y=tpos.y)

if __name__ == '__main__':
    import Phantom as P
    g = ChessGame('Long Endgame 1')
    # add a piece to test the promotion mechanism
    g.board.pieces.add(P.Pawn(P.Coord(0, 1), 'black', g.board.player2))
    g.gui()

