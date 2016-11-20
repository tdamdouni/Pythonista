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

"""Generate a tree for a given board."""

from Phantom.ai.tree.leaves import Node
from Phantom.ai.settings import window, maxdepth
from Phantom.ai.prediction.alphabeta import alpha_beta_value
from Phantom.core.board import Board
from Phantom.utils.debug import call_trace, log_msg

__all__ = []

def _spawn_children(node, tree=None):
    log_msg('_spawn_children({}) starting'.format(node), 4)
    legal = node.board.all_legal()
    for piece in legal:
        try:
            for move in legal[piece]:
                new = node.variate(piece.coord, move)
                newnode = Node(node.depth + 1, (node.depth+1) > maxdepth, new, parent=node)
                newnode.set_parent(node)
                if tree:
                    newnode.set_tree(tree)
        except KeyError:
            continue
    log_msg('_spawn_children({}) ending'.format(node), 4)

def _recursive_spawn(node, tree=None):
    log_msg('_recursive_spawn({}) starting'.format(node), 4)
    depth = node.depth
    if depth > maxdepth:
        log_msg('_recursive_spawn({}) reached depth cutoff'.format(node), 4)
        return False
    for child in node.children:
        _spawn_children(child, tree)
        _recursive_spawn(child, tree)
    log_msg('_recursive_spawn({}) ending'.format(node), 4)

@call_trace(4)
def spawn_tree(board):
    root = Node(0, False, board)
    _spawn_children(root, root)
    _recursive_spawn(root, root)
    for child in root.children:
        child.alphabeta = alpha_beta_value(child)
    return root
__all__.append('spawn_tree')

def main(clear=True):
    print('=' * 50)
    from Phantom.core.game_class import ChessGame
    from Phantom.utils.debug import log_msg, clear_log
    
    if clear: clear_log()
    log_msg('Testing Phantom.ai.tree.generate.spawn_tree()', 0)
    tree = None
    try:
        g = ChessGame()
        tree = spawn_tree(g.board)
    except ImportError:  #Exception as e:
        log_msg('Phantom.ai.tree.generate.spawn_tree() test failed:\n{}'.format(e), 0, err=True)
    finally:
        log_msg('Test complete', 0)
    return tree

if __name__ == '__main__':
    tree = main()
