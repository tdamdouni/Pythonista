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

from __future__ import (absolute_import, division, print_function, unicode_literals)

import dialogs, photos, sk, sys, ui
#import Phantom.sk_gui.SkChessBoardScene ; reload(Phantom.sk_gui.SkChessBoardScene)  #Pythonista workaround
from Phantom.sk_gui.SkChessBoardScene import SkChessBoardScene
from Phantom.core.game_class import ChessGame

def quit_action(sender):
    msg = '{} is not yet implemented!!'.format(sender.title)
    dialogs.hud_alert(msg)
    print(msg)

# +-------------+  Given status_height and the screen size,
# | L |  C  | R |   screen_frames() calculates four frames:
# | e |  e  | i |
# | f |  n  | g |     left_frame: Rect(  0,   0,  128, 744)
# | t |  t  | h |   center_frame: Rect(128,   0,  704, 744)
# |   |  e  | t |    right_frame: Rect(832,   0,  128, 744)
# |   |  r  |   |
# +-------------+
# |   Status    |   status_frame: Rect(  0, 704, 1024,  24)
# +-------------+

def screen_frames(status_height=24):
    w, h = ui.get_screen_size()  # (1024, 768) on iPad in landscape mode
    assert w > h, 'This app only works in landscape mode!!'
    square_side = min(w, h) - status_height  # make room for a line of status text
    panel_width = (w - square_side) / 2
    center_frame = sk.Rect(panel_width, 0, square_side, square_side)
    left_frame   = sk.Rect(0, 0, panel_width, square_side)
    right_frame  = sk.Rect(panel_width + square_side, 0, panel_width, square_side)
    status_frame = sk.Rect(0, square_side, w, status_height)
    return center_frame, left_frame, right_frame, status_frame

#print(screen_frames())

class SkChessView(ui.View):
    views_alpha = 0.3  # allow the background photo to show thru the views

    def __init__(self, game=None):
        self.game = game or ChessGame()
        self.width, self.height = ui.get_screen_size()
        assert self.width > self.height, 'This app only works in landscape mode!!'
        if photos.is_authorized():  # add a photo as the background image
            self.add_subview(self.make_image_view())
        center_frame, left_frame, right_frame, status_frame = screen_frames()
        self.add_subview(self.make_left_side_view(left_frame))
        self.make_buttons(left_frame)
        self.add_subview(self.make_board_scene(center_frame))
        self.info_view = self.make_right_side_view(right_frame)
        self.add_subview(self.info_view)
        self.status_view = self.make_status_view(status_frame)
        self.add_subview(self.status_view)
        self.present(orientations=['landscape'], hide_title_bar=True)

    def make_image_view(self, image_name=''):  # fullscreen background photo
        image_view = ui.ImageView(frame=self.bounds)
        image_view.image = ui.Image.from_data(photos.get_image(raw_data=True))
        return image_view

    def make_board_scene(self, center_frame):
        board_scene = SkChessBoardScene(self.game, center_frame)
        scene_view = sk.View(board_scene)
        scene_view.frame = center_frame  # center_square()
        scene_view.shows_fps = True
        scene_view.shows_node_count = True
        scene_view.shows_physics = True
        return scene_view

    #@classmethod
    def make_button(self, title, i):
        button = ui.Button(name=title, title=title.replace('_', ' '))
        # interesting that getattr(self, ...) != self.getattr(...)
        button.action = getattr(self, 'action_' + title.lower(), quit_action)
        #print(title, button.action)
        button.x = 30
        button.y = 105 * (i + 1)
        return button

    def make_buttons(self, frame, menu_titles=None):
        menu_titles = menu_titles or 'Options AI_Easy AI_Hard Get_score Undo Deselect'.split()
        for i, title in enumerate(menu_titles):
            self.add_subview(self.make_button(title, i))

    def action_ai_easy(self, sender):
        self.game.ai_easy()

    def action_ai_hard(self, sender):
        self.game.ai_hard()

    def action_get_score(self, sender):
        dialogs.hud_alert('Score: {}'.format(self.game.ai_rateing))

    def action_undo(self, sender):
        self.game.rollback()

    @classmethod
    def make_right_side_view(cls, right_frame):
        text_view = ui.TextView(frame=right_frame)
        text_view.alpha = cls.views_alpha
        text_view.alignment = ui.ALIGN_CENTER
        text_view.editable = False
        text_view.text = '\n' + '1234567890 ' * 50
        return text_view

    @classmethod
    def make_left_side_view(cls, left_frame):
        view = ui.TextView(frame=left_frame)
        view.alpha = cls.views_alpha
        view.editable = False
        return view

    @classmethod
    def make_status_view(cls, status_frame):
        text_view = ui.TextView(frame=status_frame)
        text_view.alpha = cls.views_alpha
        text_view.alignment = ui.ALIGN_CENTER
        text_view.editable = False
        text_view.text = "Status: let the game begin...  It is white's turn to move"
        return text_view
    
    def update_view(self, piece=None):
        if piece:
            self.info_view.text = '\n' + piece.as_str
        self.status_view.text = self.game.board.as_fen_str()

def gui_sk(game=None):
    SkChessView(game or ChessGame())

if __name__ == '__main__':
    from Phantom.core.game_class import ChessGame
    print('=' * 30)
    gui_sk()
