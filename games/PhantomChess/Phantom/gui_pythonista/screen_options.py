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

"""Options screen."""

import scene, sys

from Phantom.boardio.boardcfg import Cfg
from Phantom.core.chessobj import PhantomObj
#from Phantom.constants import scale_factor, screen_size
#from Phantom.core.coord.point import Coord
from Phantom.core.game_class import ChessGame

class ChessOptionsScreen (scene.Scene, PhantomObj):

    def __init__(self, game_view):
        self.game_view = game_view
        self.tmp_t = 0
        self.data = Cfg()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        if self.parent:
            self.parent.set_options_scene(self)

    def setup(self):
        self.game.data['has_gui'] = True
        self.data['game'] = self.game
        self.data.update(self.game.board.cfg)

                        # ( name,           title,           value,   position,           action)
                        # toggles have action == None
        self.buttons = [('disp_coords',    'Show coords',    True,    Coord(0, 672),      None),
                        ('',               'Save & exit',    'NA',    Coord(930, 576),    self.return_to_game),
                        ('force_moves',    'Force moves',    True,    Coord(0, 576),      None),
                        ('disp_turn',      'Show turn_color',      True,    Coord(0, 480),      None),
                        ('highlight',      'Show valid',     True,    Coord(0, 384),      None),
                        ('disp_pieces',    'Show pieces',    True,    Coord(0, 288),      None),
                        ('disp_sqrs',      'Show grid',      True,    Coord(0, 192),      None),
                        ('',               'Copy FEN',       'NA',    Coord(0, 96),       self.copy_fen),
                        ('disp_timers',    'Show timers',    True,    Coord(0, 0),        None) ]
                        # commented out until I can figure out how to make self.rst_game() work properly
                        #('',              'Reset game',     'NA',    Coord(96, 672),     self.rst_game),]
        self.button_size = Coord(scale_factor, scale_factor)
        self.size = screen_size

    # ------------------- Button actions ---------------------
    def toggle(self, key):
        self.data[key] = not self.data[key]

    def return_to_game(self):
        if self.parent:
            self.parent.switch_scene(self.game.data['screen_main'])
        else:  # when running this file standalone
            sys.exit('return_to_game() with no parent!')

    def copy_fen(self):
        import clipboard
        fen = self.game.board.fen_str()
        clipboard.set(fen)

    def rst_game(self):
        sc_data = self.data
        new_game = ChessGame()
        new_game.board.cfg = sc_data
        self.game = new_game
        # The reason this doesnt work is that after setting
        # self.game, the (new) game does NOT have the attributes
        # necessary to have a GUI (missing g.data['main_scene'] etc)
        # This makes the options class' `self.return_to_game()` raise AttributeError
    # ------------------ End button actions ------------------

    def sync_data(self):
        # update game data first to push any changes
        self.game.board.cfg.copy_data_from(self.data)

        # update our data as well in case any new variables have
        # been set
        self.data.update(self.game.board.cfg)

    @staticmethod
    def draw_toggle(name, curval, pos):
        name = str(name)
        val = str(curval)
        x, y = pos.x, pos.y
        w = h = scale_factor
        mid = Coord(x + (w / 2), y + (h / 2))
        label = Coord(mid.x, mid.y + 10)
        state = Coord(mid.x, mid.y - 10)
        scene.text(name, x=label.x, y=label.y)
        scene.text(val, x=state.x, y=state.y)

    @staticmethod
    def draw_button(name, pos):
        name = str(name)
        x, y = pos.x, pos.y
        w = h = scale_factor
        mid = Coord(x + (w / 2), y + (h / 2))
        scene.text(name, x=mid.x, y=mid.y)

    def touch_began(self, touch):
        w, h = self.button_size.x, self.button_size.y
        for button in self.buttons:
            name, title, value, position, action = button
            hit_test = scene.Rect(position.x, position.y, w, h)
            if touch.location in hit_test:
                if action:  # toggles have action == None
                    action()
                else:
                    self.toggle(name)
                self.sync_data()
                break

    def draw(self):
        scene.background(0, 0, 0)

        for button in self.buttons:
            name, title, value, position, action = button
            if action:  # toggles have action == None
                self.draw_button(title, position)
            else:
                self.draw_toggle(title, self.data[name], position)


if __name__ == '__main__':
    from Phantom.gui_pythonista.game_view import GameView
    GameView(game)
