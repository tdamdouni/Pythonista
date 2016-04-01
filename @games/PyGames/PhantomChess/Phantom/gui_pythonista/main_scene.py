#!/usr/bin/env python
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

"""The main scene object for the GUI.  Allowes use of multiple scene classes with one GUI."""

import scene

from Phantom.core.chessobj import PhantomObj
from Phantom.boardio.boardcfg import Namespace

class MultiScene (scene.Scene, PhantomObj):
    
    def __init__(self, start_scene):
        self.active_scene = start_scene
        self.tmp_t = 0
        self.invocations = 0
        self.data = Namespace()
        
    def switch_scene(self, new_scene):
        new_scene.setup()
        self.active_scene = new_scene
        
    def setup(self):
        self.active_scene = self.load_scene
        self.tmp_t = self.t
        self.active_scene.setup()
        
    def draw(self):
        self.invocations += 1
        scene.background(0, 0, 0)
        scene.fill(1, 0, 0)
        self.active_scene.touches = self.touches
        self.active_scene.t = self.t - self.tmp_t
        self.active_scene.draw()
        
    def touch_began(self, touch):
        self.active_scene.touch_began(touch)
        
    def touch_moved(self, touch):
        self.active_scene.touch_moved(touch)
        
    def touch_ended(self, touch):
        self.active_scene.touch_ended(touch)
    
    def set_main_scene(self, s):
        self.main_scene = s
    
    def set_load_scene(self, s):
        self.load_scene = s
    
    def set_dbg_scene(self, s):
        self.dbg_scene = s
    
    def set_options_scene(self, s):
        self.options_scene = s
    
    def set_promote_scene(self, s):
        self.promote_scene = s
    
    def did_begin(self):
        self.switch_scene(self.main_scene)

if __name__ == '__main__':
    from Phantom.core.game_class import ChessGame
    game = ChessGame()
    game.gui()

