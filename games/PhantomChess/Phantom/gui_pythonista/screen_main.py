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

"""The main screen."""

import os
import sys
import scene

#from Phantom.core.coord.point import Coord, bounds
Coord = scene.Point
import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.utils.debug import log_msg, call_trace
#from Phantom.constants import *
#from Phantom.ai.pos_eval.advanced import pos_eval_advanced
from Phantom.core.exceptions import InvalidMove
from Phantom.gui_pythonista.screen_options import ChessOptionsScreen
from Phantom.gui_pythonista.screen_promote import ChessPromoteScreen


class ChessMainScreen (scene.Scene): #, PhantomObj):

    def __init__(self, game_view):
        self.game_view = game_view
        #print(self.bounds, self.size)
        self.tmp_t = 0  # ccc: what?, why?

    def setup(self):
        #print(self.bounds, self.size)
        #print(type(self.bounds))
        #sys.exit(type(self.bounds))
        self.square_size = min(*self.size) / 8  # normally 96.0 on an iPad

        if self.size.w > self.size.h:
            self.offset = scene.Point((self.size.w - self.size.h) / 2, 0)
        else:  # normally Point(x=128.0, y=0) on an iPad in landscape mode
            self.offset = scene.Point(0, (self.size.h - self.size.w) / 2)
        
        #self.offset = 
        #print(self.square_size)
        cfg = self.game_view.game.board.cfg
        self.coord_disp_mode = {'onoff': cfg.disp_coords,
                                'mode': cfg.coord_mode}
        self.render_mode = {'sqrs': cfg.disp_sqrs,
                            'pieces': cfg.disp_pieces,
                            'valid': cfg.highlight,
                            'coords': cfg.disp_coords,
                            'turn_color': cfg.disp_turn,
                            'timers': cfg.disp_timers}
        self.is_selected = False
        self.selected = ''  # Coord(None, None)  self.selected --> a fen_pos
        self.target = self.selected
        self.err = None
        self.err_pos = ''  # Coord(None, None)
        self.valid_cache = []
        self.img_names = self.game_view.load_images()
        #print(self.img_names)
        self.turn_indicator_img = 'White_Square'
        self.pos_score = None
        self.disp_score = False
        #min = Coord(0, 0).as_screen
        #max = Coord(8, 8).as_screen
        #self.bounds = scene.Rect(min.x, min.y, max.x-min.x, max.y-min.y)
        #print(screen_size)
        #self.size = screen_size
        #print(self.bounds) # --> Rect(x=128, y=0, w=768, h=768)
        self.won = self.game_view.game.is_won()

    def as_screen(self, piece):
        return scene.Point(piece.x * self.square_size + self.offset.x,
                           piece.y * self.square_size + self.offset.y)
        
    def from_screen(self, touch_loc):
        return (int((touch_loc.x - self.offset.x) / self.square_size),
                int((touch_loc.y - self.offset.y) / self.square_size))

    def did_err(self, e):
        self.err = sys.exc_info()
        self.selected = ''  # Coord(None, None)
        self.is_selected = False
        #self.game_view.game.board.freeze()

    def touch_began(self, touch):
        scale_factor = self.square_size
        game = self.game_view.game
        self.valid_cache = []
        tpos = Coord(touch.location.x, touch.location.y)
        #cpos = Coord.from_screen(tpos)
        cpos = self.from_screen(tpos)
        fen_loc = C.fen_loc_from_xy(*cpos)
        print('tpos, cpos, fen_loc...', tpos, cpos, fen_loc, self.offset)
        #if touch.location in self.bounds:
        if touch.location.x >= self.offset.x and touch.location.y >= self.offset.y:
            if not self.is_selected:
                piece = game.board[fen_loc]
                if isinstance(piece, list):
                    try:
                        raise ChessError('More than one piece at position',
                              'Phantom.gui_pythonista.screen_main.ChessMainScreen.touch_began()')
                    except ChessError as e:
                        self.did_err(e)
                        return
                if piece:
                    self.selected = fen_loc  # cpos
                    self.valid_cache = piece.all_valid_moves  # piece.valid()
                    self.is_selected = True
                else:
                    self.selected = ''  # Coord(None, None)
            else:
                self.target = fen_loc
                try:
                    if game.board[self.selected].ptype == 'king':
                        piece = game.board[self.selected]
                        castling_rights = game.board.castling_rights
                        if piece.color == 'white':
                            if self.target == 'g8':  # Coord(6, 0):
                                if 'K' in castling_rights:
                                    game.castle('K')
                            elif self.target == 'c8':  # Coord(2, 0):
                                if 'Q' in castling_rights:
                                    game.castle('Q')
                        elif piece.color == 'black':
                            if self.target == 'g1':  # Coord(6, 7):
                                if 'k' in castling_rights:
                                    game.castle('k')
                            elif self.target == 'c1':  # Coord(2, 7):
                                if 'q' in castling_rights:
                                    game.castle('q')
                    mr = game.move(self.selected, self.target)
                    self.disp_score = False
                    self.won = game.is_won()
                except InvalidMove as e:
                    self.err_pos = self.target
                    self.did_err(e)
                except Exception as e:
                    self.did_err(e)
                self.selected = ''  # Coord(None, None)
                self.target = ''  # Coord(None, None)
                self.is_selected = False
                if isinstance(mr, str):
                    self.err_pos = self.target
                if any([p.is_promotable for p in game.board.pieces]):
                    self.game_view.switch_scene(ChessPromoteScreen)
        elif 0 < touch.location.x <= scale_factor:
            if 6*scale_factor < touch.location.y <= 7*scale_factor:
                self.game_view.switch_scene(ChessOptionsScreen)
            elif 5*scale_factor < touch.location.y:
                game.ai_easy()
            elif 4*scale_factor < touch.location.y:
                game.ai_hard()
            elif 3*scale_factor < touch.location.y:
                self.pos_score = game.ai_rateing
                self.disp_score = True
            elif 2*scale_factor < touch.location.y:
                game.rollback()
            elif scale_factor < touch.location.y:
                self.is_selected = False
                self.selected = ''  # Coord(None, None)
                self.target = ''  # Coord(None, None)

    def draw(self):
        scale_factor = self.square_size
        scene.background(0, 0, 0)
        scene.fill(1, 1, 1, 1)
        board = self.game_view.game.board
        if self.render_mode['pieces']:
            for piece in board.pieces:
                scene.tint(1, 1, 1, 0.5)
                pos = self.as_screen(piece)  # piece.coord.as_screen
                #print(self.img_names)
                img = self.img_names[piece.name]
                scene.image(img, pos.x, pos.y, scale_factor, scale_factor)
                scene.tint(1, 1, 1, 1)
                if piece.fen_loc == self.selected:
                    scene.fill(0.23347,0.3564,0.59917, 0.6)
                    scene.rect(pos.x, pos.y, scale_factor, scale_factor)
                    scene.fill(1, 1, 1, 1)
            if self.render_mode['timers']:
                white = str(board.player1.timer.get_run())
                black = str(board.player2.timer.get_run())
                bpos = Coord(992, 672)
                wpos = Coord(992, 96)
                scene.tint(1, 1, 1, 1)
                scene.text(black, x=bpos.x, y=bpos.y)
                scene.text(white, x=wpos.x, y=wpos.y)
                scene.tint(1, 1, 1, 1)
        if self.render_mode['sqrs']:
            for tile in board.tiles:
                x = int(tile.color == 'white')  # zero or one Thi is code
                color = (x, x, x, 0.57)  # alpha value
                scene.fill(*color)
                pos = self.as_screen(tile)  # tile.as_screen
                scene.rect(pos.x, pos.y, scale_factor, scale_factor)
                scene.fill(1, 1, 1, 1)
                if self.render_mode['coords']:
                    center = Coord(pos.x + (scale_factor / 2), pos.y + (scale_factor / 2))
                    chess_pos = center + Coord(0, 10)
                    coord_pos = center - Coord(0, 10)
                    chess = tile.coord.as_chess
                    coord = str(tile.coord.as_tup)
                    scene.text(chess, x=chess_pos.x, y=chess_pos.y)
                    scene.text(coord, x=coord_pos.x, y=coord_pos.y)
            #if self.err_pos:  # FIXME this needs to be reenabled!
            #    sc = self.err_pos.as_screen
            #    scene.fill(1, 0, 0, 0.3)
            #    scene.rect(sc.x, sc.y, scale_factor, scale_factor)
            #    scene.fill(1, 1, 1, 1)
            #    scene.tint(0, 0, 1, 1)
            #    scene.text('Move\nInvalid', x=(sc.x + scale_factor/2), y=(sc.y + scale_factor/2))
            #    scene.tint(1, 1, 1, 1)
        if self.render_mode['valid']:
            for tile in board.tiles:
                #if self.valid_cache:
                #    print([x for x in self.valid_cache])
                #if tile.coord in self.valid_cache:  # FIXME
                if tile.fen_loc in self.valid_cache:
                    pos = self.as_screen(tile)  # tile.coord.as_screen
                    scene.fill(0.47934,0.81198,0.41839, 0.3)
                    scene.rect(pos.x, pos.y, scale_factor, scale_factor)
                    scene.fill(1, 1, 1, 1)
        if self.render_mode['turn_color']:
            if board.turn == 'white':
                turn_y = 1 * scale_factor
            elif board.turn == 'black':
                turn_y = 7 * scale_factor
            pos = Coord(896, turn_y)
            size = Coord(scale_factor / 2, scale_factor / 2)
            scene.tint(1, 1, 1, 1)
            scene.image(self.turn_indicator_img, pos.x, pos.y, size.x, size.y)
            scene.tint(1, 1, 1, 1)
        if self.won:
            pos = Coord(self.size.w/2, self.size.h/2)
            scene.tint(0.32645,0.28306,0.93492)
            # commented out until the bug in ChessGame.is_won() is fixed to be
            # less annoying
            scene.text('{} wins'.format(self.won), x=pos.x, y=pos.y, font_size=40.0)
            scene.tint(1, 1, 1, 1)

        # Buttons
        x=scale_factor/2
        scene.text('AI Easy', x=x, y=scale_factor*6 - x)
        scene.text('AI Hard', x=x, y=scale_factor*5 - x)
        scene.text('Get score', x=x, y=scale_factor*4 - x)
        if self.disp_score:
            scene.text(str(self.pos_score), x=x, y=scale_factor*4 - scale_factor/1.5)
        scene.text('Undo', x=x, y=scale_factor*3 - x)
        scene.text('Deselect', x=x, y=scale_factor*2 - x)
        scene.text('Options', x=x, y=scale_factor*7 - x)

if __name__ == '__main__':
    from Phantom.core.game_class import load_game
    from Phantom.gui_pythonista.game_view import GameView
    #game = load_game('Long Endgame 1')
    #game.board.cfg.disp_sqrs = True
    GameView()  # game)
