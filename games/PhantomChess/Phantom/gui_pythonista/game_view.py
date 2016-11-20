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

"""The main scene object for the GUI.  Allows use of multiple scene classes with one GUI."""

import os, scene, ui
import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.core.game_class import ChessGame
from Phantom.gui_pythonista.screen_main import ChessMainScreen
from Phantom.gui_pythonista.screen_loading import ChessLoadingScreen

class GameView(ui.View):
    def __init__(self, game=None, in_scene=None):
        self.game = game or ChessGame()
        in_scene = in_scene or ChessLoadingScreen
        self.present('full_screen', orientations=['landscape'], hide_title_bar=True)
        self.scene_view = scene.SceneView(frame=self.frame)
        self.scene_view.scene = in_scene()
        self.add_subview(self.scene_view)
        self.add_subview(self.close_button())
        self.switch_scene()  # switch from loading to main

    def close_action(self, sender):
        print('Closing...')
        self.close()

    def close_button(self):
        the_button = ui.Button(title='X')
        the_button.x = self.width - the_button.width
        the_button.y = the_button.height / 2
        the_button.action = self.close_action
        the_button.font=('<system-bold>', 20)
        return the_button

    def switch_scene(self, new_scene=None):
        new_scene = new_scene or ChessMainScreen
        self.scene_view.scene = new_scene(self)

    @classmethod
    def load_images(cls, piece_types=None):
        # returns a dict of {piece_name : piece_image} entries
        piece_types = piece_types or 'king queen bishop knight rook pawn'.split()
        fmt = C.image_path_fmt
        filenames = ['{} {}'.format(color, ptype) for ptype in piece_types
                                                  for color in C.colors]
        return {filename : scene.load_image_file(fmt.format(filename))
            for filename in filenames}

if __name__ == '__main__':
    GameView()
