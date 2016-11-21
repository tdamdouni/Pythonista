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

"""Make the AI pick a good move from the scored nodes in a search tree."""

from Phantom.core.board import Board
from Phantom.ai.tree.generate import spawn_tree

def make_smart_move(board):
    tree = spawn_tree(board)
    turn = board.turn
    if turn == 'black':
        best = float('inf')
        func = min
        cmp = lambda a, b: a < b
    elif turn == 'white':
        best = float('-inf')
        func = max
        cmp = lambda a, b: a > b

    bestnode = None
    print("turn_color: {}, func: {}, best: {}".format(turn, func, best))
    for child in tree.children:
        print(child, child.score)
        if cmp(child.score, best):
            print("New best node: {}".format(child))
            bestnode = child

    if not bestnode:
        print('make_smart_move() can not find a bestnode')
        return False
    move = bestnode.board.lastmove
    board.move(move[0], move[1])
    return True

def main(clear=True):
    from Phantom.core.game_class import ChessGame
    board = ChessGame().board
    board.pprint()
    for i in xrange(105):
        print('make_smart_move {}: {}'.format(i + 1, make_smart_move(board)))
        board.pprint()
        winner = False # board.game.is_won()
        if winner:
            print('{} won this game in {} smart moves.'.format(winner, (i + 1) / 2))
            break
    return(board.game.ai_rateing)

if __name__ == '__main__':
    print('=' * 80)
    score = main()
    print(score)