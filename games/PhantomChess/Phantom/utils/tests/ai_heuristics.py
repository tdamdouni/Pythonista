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

"""Test the AI's position evaluation heuristics, one at a time and print the output."""

from Phantom.utils.debug import log_msg, clear_log
from Phantom.ai.pos_eval.heuristics import all_rules
from Phantom.core.game_class import load_game

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.ai.pos_eval.heuristics functions', 0)
    #g = ChessGame('Game 1')
    g = load_game('Game 1')
    log_msg('Testing AI heuristics on savegame "Game 1":', 0)
    score = 0
    for rule in all_rules:
        try:
            log_msg(rule.__name__ + " evaluating...", 0)
            r = rule(g.board)
            log_msg(rule.__name__ + ' returned {}'.format(r), 0)
            score += r
        except Exception as e:
            log_msg('{} failed:\n{}'.format(f.__name__, e), 0, err=True)
    log_msg('Test complete', 0)
    return score

if __name__ == '__main__':
    print('=' * 20)
    score = main()
    print('score: {}'.format(score))
