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

"""Test the AI's search tree generation."""

from Phantom.ai.tree.leaves import Node
from Phantom.ai.tree.generate import spawn_tree
from Phantom.core.game_class import ChessGame
from Phantom.utils.debug import log_msg, clear_log

def main(clear=True):
    if clear: clear_log()
    log_msg('Testing Phantom.ai.tree.generate.spawn_tree()', 0)
    tree = None
    try:
        g = ChessGame()
        tree = spawn_tree(g.board)
    except Exception as e:
        log_msg('Phantom.ai.tree.generate.spawn_tree() test failed:\n{}'.format(e), 0, err=True)
    finally:
        log_msg('Test complete', 0)
    return tree

if __name__ == '__main__':
    tree = main()
