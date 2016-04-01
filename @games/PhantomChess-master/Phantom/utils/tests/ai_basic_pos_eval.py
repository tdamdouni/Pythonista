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

"""Test the AI's basic position evaluation and material assesment."""

from Phantom.core.game_class import ChessGame
from Phantom.ai.pos_eval.basic import pos_eval_basic, pos_material
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.ai.pos_eval.basic pos_eval_basic() & pos_material()', 0)
    game = ChessGame()
    score = material = None
    try:
        score = pos_eval_basic(game.board)
    except Exception as e:
        log_msg('AI basic position evaluation failed: \n{}'.format(e), 0, err=True)
    try:
        material = pos_material(game.board)
    except Exception as e:
        log_msg('AI material assesment failed: \n{}'.format(e), 0, err=True)
    log_msg('Test complete', 0)
    return score, material

if __name__ == '__main__':
    main()
