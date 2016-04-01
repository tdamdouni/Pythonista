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

try:
    import scene
    in_pythonista = True
    del scene
except ImportError:
    in_pythonista = False

from Phantom.__version__ import __version__ as version

###################################################################################################################
############################################### USER SETTINGS #####################################################
###################################################################################################################

# Debug level
# This can make the program slow
# Please select from range(0, 11)
debug = 0

# Use the unicode prettyprinter or an ASCII prettyprinter
use_unicode = False

# Adjusts the scale of the board in the GUI
screen_height = 768  # pixels

# Adjusts the scale of the board in the GUI
screen_width = 1024  # pixels

###################################################################################################################
############################################# END USER SETTINGS ###################################################
###################################################################################################################

dirs = {'north': (0, 1), 
        'south': (0, -1), 
        'east': (1, 0), 
        'west': (-1, 0), 
        'nw': (1, 1), 
        'se': (1, -1), 
        'nw': (-1, 1), 
        'sw': (-1, -1), 
        'unknown': (None, None), 
        }

        
# These dont affect gameplay, here for my own reference
pieces = ['king', 'rook', 'bishop', 'queen', 'knight', 'pawn']
pieces_per_player = {'rook': 2, 
                     'king': 1, 
                     'bishop': 2, 
                     'queen': 1, 
                     'knight': 2, 
                     'pawn': 8, 
                     }                     

# these do affect gameplay and will raise errors if edited
grid_width = 8
grid_height = 8
grid_colors = {'black': (0.27462, 0.26326, 0.27367), 
               'white': (0.86674, 0.86674, 0.88017), 
               }
scale_factor = screen_height//grid_height  # Get the height, in pixels, of each square
               
holder_point = (-10, -10)

moves = []
detailed = []
counter = 1
ncounter = 0

filename = 'move_record.py'
rawname  = 'raw_record'
save_fen = 'savegames_fen.txt'
save_epd = 'savegames_epd.txt'
test_suite = 'Phantom_test_suite.txt'  # don't add your own games to this!
dbgname  = 'debug.txt'

c_white_pawn = 'P'
c_black_pawn = 'p'
c_white_rook = 'R'
c_black_rook = 'r'
c_white_bishop = 'B'
c_black_bishop = 'b'
c_white_knight = 'N'
c_black_knight = 'n'
c_white_queen = 'Q'
c_black_queen = 'q'
c_white_king = 'K'
c_black_king = 'k'
c_white_space = ' '
c_black_space = '.'
c_turn_indicator = '<'

d_white_pawn = u'\u2659'
d_black_pawn = u'\u265f'
d_white_rook = u'\u2656'
d_black_rook = u'\u265c'
d_white_bishop = u'\u2657'
d_black_bishop = u'\u265d'
d_white_knight = u'\u2658'
d_black_knight = u'\u265e'
d_white_queen = u'\u2655'
d_black_queen = u'\u265b'
d_white_king = u'\u2654'
d_black_king = u'\u265a'
d_white_space = u'\u25e6'  # hollow bullet
d_black_space = u'\u2022'  # solid bullet
d_turn_indicator = u'\u25c0'

opening_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen_rank_split = '/'

default_halfmove = 0
default_fullmove = 1

import os as _os
phantom_dir = _os.path.dirname(_os.path.realpath(__file__))
del _os

if in_pythonista:
    import scene
    screen_size = scene.Rect(0, 0, screen_width, screen_height)
    del scene
else:
    screen_size = (0, 0, screen_width, screen_height)

