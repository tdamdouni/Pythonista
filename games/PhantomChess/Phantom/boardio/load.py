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

"""Get a FEN string for a given board save-name."""

#from Phantom.core.exceptions import ChessError, LogicError
from Phantom.constants import save_fen, phantom_dir
import os
#import inspect

def valid_lines_from_file(file_path):
    with open(file_path) as in_file:
        return [line.strip() for line in in_file.readlines()
                if line.strip() and line.strip()[0] != '#']

def load_game(name):
    file_path = os.path.join(phantom_dir, 'boardio', save_fen)
    for line in valid_lines_from_file(file_path):
        bname, _, fen = line.partition(':')
        if bname.strip() == name:
            return fen.strip()

def list_games():
    file_path = os.path.join(phantom_dir, 'boardio', save_fen)
    return [line.partition(':')[0].strip() for line in valid_lines_from_file(file_path)]
