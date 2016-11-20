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

"""Rigorously test the advanced position evaluator."""

from Phantom.core.game_class import ChessGame
from Phantom.ai.pos_eval.advanced import pos_eval_advanced
from Phantom.utils.debug import log_msg, clear_log
from Phantom.boardio.epd_read import load_test, list_tests

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.ai.pos_eval.advanced.pos_eval_advanced()', 0)
    for test in list_tests():
        log_msg('Beginning pos eval on test {}'.format(test), 0)
        board = load_test(test)
        score = None
        try:
            score = pos_eval_advanced(board)
        except Exception as e:
            log_msg('Advanced position evaluation failed: \n{}'.format(e), 0, err=True)
        finally:
            log_msg('Pos eval test on {} complete: score={}'.format(test, score), 0)
    log_msg('Test complete', 0)


if __name__ == '__main__':
    main()
