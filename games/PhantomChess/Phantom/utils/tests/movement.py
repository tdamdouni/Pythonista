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

"""Test the Phantom.core.board.Board.move() method"""

#from Phantom.core.board import Board
from Phantom.core.game_class import ChessGame
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.core.board.Board.move() method', 0)
    #b = Board(None)  # white to move, opening layout
    b = ChessGame().board
    try:
        b.move('e2e4')
        b.move('g8f6')
        b.move('g2g3')
    except Exception as e:
        log_msg('Phantom.core.board.Board.move() method test failed:\n{}'.format(e), 0, err=True)
    finally:
        log_msg('Test complete', 0)

if __name__ == '__main__':
    main()
