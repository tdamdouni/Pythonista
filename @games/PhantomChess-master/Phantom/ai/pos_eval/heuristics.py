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

"""A lot of rules that analyze a board.

All functions in this file take one argument, a board, and analyze it
for a specific characteristic.
They all return a number which should be added to the board variation's score.

The file defines an all_rules list that contains all the functions.  It can be iterated through
with a loop similar to the following to obtain a score for a board:

```
from Phantom.ai.pos_eval.heuristics import all_rules
from Phantom.ai.pos_eval.basic import pos_eval_basic
from Phantom.core.board import Board

test = Board()
score = pos_eval_basic(test)  # should be 0
print("Basic evaluation:", score)

for rule in all_rules:
    score += rule(test)
    print("Applied {} rule, score:".format(rule.__name__), score)

print("Final score:", score)
```

I'm not going to document the reasoning for each of these rules -- they should be easily
locatable on the internet.
"""

import string
from Phantom.ai.phases import Phase
#from Phantom.core.coord.point import Coord
import Phantom.constants as C
from Phantom.utils.debug import call_trace, log_msg

#board_north_edge = [Coord(x, 7) for x in xrange(grid_width)]
#board_south_edge = [Coord(x, 0) for x in xrange(grid_width)]
#board_east_edge  = [Coord(7, y) for y in xrange(grid_height)]
#board_west_edge  = [Coord(0, y) for y in xrange(grid_height)]


#board_rim = board_north_edge + board_south_edge + board_east_edge + board_west_edge
def in_board_rim(fen_loc):
    x, y = fen_loc
    return x in 'ah' or y in '18'

'''
files = dict(
a = [Coord(0, y) for y in xrange(grid_height)],
b = [Coord(1, y) for y in xrange(grid_height)],
c = [Coord(2, y) for y in xrange(grid_height)],
d = [Coord(3, y) for y in xrange(grid_height)],
e = [Coord(4, y) for y in xrange(grid_height)],
f = [Coord(5, y) for y in xrange(grid_height)],
g = [Coord(6, y) for y in xrange(grid_height)],
h = [Coord(7, y) for y in xrange(grid_height)],
)
#the following dict comprehension is equivalent and faster but not as easy to understand
#filez = {string.lowercase[i]:[Coord(i, y) for y in xrange(grid_height)]
#         for i in xrange(grid_width)}
#assert files == filez, '{}\n{}'.format(files, filez)
'''

all_rules = []

@call_trace(3)
def knight_on_edge(board):
    from Phantom.ai.settings import knight_on_edge_score
    #east_west_edges = board_east_edge + board_west_edge
    return sum(knight_on_edge_score * (1 if p.color == 'white' else -1)
               for p in board.get_piece_list(ptype='knight') if p.col in 'ah')
# this is left out for the more advanced & precise assess_knights()
#all_rules.append(knight_on_edge)

@call_trace(3)
def developed_pieces(board):
    from Phantom.ai.settings import developed_scores
    return sum(developed_scores[p.ptype] * (1 if p.color == 'white' else -1)
               for p in board.pieces if not p.first_move)
all_rules.append(developed_pieces)

@call_trace(3)
def advanced_pawns(board):
    from Phantom.ai.settings import advanced_pawn_mul, promotable_bonus
    #from Phantom.constants import grid_width
    score = 0
    for piece in board.get_piece_list(ptype='pawn'):
        if piece.color == 'white':
            if piece.y >= 4:
                score += piece.y * advanced_pawn_mul
            if piece.is_promotable:
                score += promotable_bonus
        elif piece.color == 'black':
            if piece.y <= 3:
                score -= (8 - piece.y) * advanced_pawn_mul
            if piece.is_promotable:
                score -= promotable_bonus
    return score
all_rules.append(advanced_pawns)

@call_trace(3)
def rate_kings(board):
    from Phantom.ai.settings import king_endgame
    from Phantom.ai.phases import Phase
    if Phase.analyze(board) != Phase.endgame:
        return 0
    return sum(king_endgame * (1 if p.color == 'white' else -1)
               for p in board.get_piece_list(ptype='king'))
all_rules.append(rate_kings)

@call_trace(3)
def bishop_pair(board):
    from Phantom.ai.settings import bishop_pair_bonus
    white_bishops = board.get_piece_list(ptype='bishop', color='white')
    black_bishops = board.get_piece_list(ptype='bishop', color='black')
    return (bishop_pair_bonus if len(white_bishops) >= 2 else 0
          - bishop_pair_bonus if len(black_bishops) >= 2 else 0)
all_rules.append(bishop_pair)

@call_trace(3)
def has_castled(board):
    from Phantom.ai.settings import castle_opening_bonus, castle_midgame_bonus, castle_endgame_bonus
    from Phantom.ai.phases import Phase
    def sides_castled():
        ret = ['white', 'black']
        castle = board.castling_rights
        if 'K' in castle or 'Q' in castle:
            ret.remove('white')
        if 'k' in castle or 'q' in castle:
            ret.remove('black')
        return ret
    score = 0
    castled = sides_castled()
    if 'white' in castled or 'black' in castled:
        phase = Phase.analyze(board)
        if phase == Phase.opening:
            bonus = castle_opening_bonus
        elif phase == Phase.midgame:
            bonus = castle_midgame_bonus
        elif phase == Phase.endgame:
            bonus = castle_endgame_bonus
        if 'white' in castled:
            score += bonus
        if 'black' in castled:
            score -= bonus
    return score
all_rules.append(has_castled)

@call_trace(3)
def pawn_structure(board):
    score = 0
    from Phantom.ai.settings import (doubled_pawn, tripled_pawn, isolated_pawn,
                                     pawn_ram, eight_pawns, passed_pawn)
    #from Phantom.core.coord.point import Coord
    pawns       = board.get_piece_list(ptype='pawn')
    white_pawns = [p for p in pawns if p.color == 'white']
    black_pawns = [p for p in pawns if p.color == 'black']

    log_msg('pawn_structure: counting pawns...', 5)
    if len(white_pawns) == 8:
        score += eight_pawns
    if len(black_pawns) == 8:
        score -= eight_pawns
    log_msg('pawn_structure: finished pawn count score={}'.format(score), 5)

    log_msg('pawn_structure: analyzing passed pawns...', 5)
    score += passed_pawn * len([pawn for pawn in white_pawns if pawn.y >= 5])
    score -= passed_pawn * len([pawn for pawn in black_pawns if pawn.y <= 2])
    log_msg('pawn_structure: finished passed pawns score={}'.format(score), 5)

    log_msg('pawn_structure: analyzing doubled pawns...', 5)
    for pawn in white_pawns:
        for p in list(pawn.north())[:1]:  # a list of zero or one items
            if board[p] in white_pawns:
                score += doubled_pawn
    for pawn in black_pawns:
        for p in list(pawn.south())[:1]:  # a list of zero or one items
            if board[p] in black_pawns:
                score += doubled_pawn  # CCC: should this be minus instead of plus?!?
    log_msg('pawn_structure: finished doubled pawns score={}'.format(score), 5)

    log_msg('pawn_structure: analyzing isolated pawns...', 5)
    iso_white = iso_black = 0
    #tests = [Coord(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
    #tests.remove(Coord(0, 0))
    for pawn in pawns:
        neighbors = (list(pawn.north())[:1] + list(pawn.south())[:1]
                    + list(pawn.east())[:1] + list(pawn.west())[:1]
                      + list(pawn.ne())[:1] + list(pawn.nw())[:1]
                      + list(pawn.sw())[:1] + list(pawn.sw())[:1])
        if not [x for x in neighbors if board[x]]:  # if no occupied neighbors
            if pawn.color == 'white':
                iso_white += 1
            else:
                iso_black += 1
    score += isolated_pawn * iso_white
    score -= isolated_pawn * iso_black
    log_msg('pawn_structure: finished isolated pawns score={}'.format(score), 5)

    return score
all_rules.append(pawn_structure)

@call_trace(3)
def mobility(board):
    from Phantom.ai.settings import mobility_mul, colors
    return sum(mobility_mul * len(p.valid()) * colors[p.color] for p in board.pieces)
# too slow, can take up to 5 minutes in some situations
#all_rules.append(mobility)

@call_trace(3)
def bad_bishops(board):
    from Phantom.ai.settings import bad_bishop_mul, colors
    score = 0
    white_pawns = board.get_piece_list(ptype='pawn',   color='white')
    for bishop in board.get_piece_list(ptype='bishop', color='white'):
        tc = board.tile_at(bishop.fen_loc).color
        same_color = [pawn for pawn in white_pawns if board.tile_at(pawn.fen_loc).color == tc]
        score += (bad_bishop_mul * len(same_color)) * colors['white']

    black_pawns = board.get_piece_list(ptype='pawn',   color='black')
    for bishop in board.get_piece_list(ptype='bishop', color='black'):
        tc = board.tile_at(bishop.fen_loc).color
        same_color = [pawn for pawn in black_pawns if board.tile_at(pawn.fen_loc).color == tc]
        score += (bad_bishop_mul * len(same_color)) * colors['black']
    return score
all_rules.append(bad_bishops)

# --------------------assess piece layout according to Phantom.ai.pos_eval.piece_tables---------------------------------
@call_trace(3)
def pawn_assess(board):
    from Phantom.ai.pos_eval.piece_tables import white_pawns, black_pawns
    #from Phantom.constants import grid_width
    score = 0
    for piece in board.get_piece_list(ptype='pawn'):
        #print('pawn_assess:', repr(piece))
        # x, y = piece.coord.x, (grid_width - piece.coord.y) - 1
        if piece.color == 'white':
            score += white_pawns[piece.y][piece.x]  # ccc: should order be y,x or x,y?  Repeats below
        elif piece.color == 'black':
            score += black_pawns[piece.y][piece.x]
    return score
all_rules.append(pawn_assess)

@call_trace(3)
def knight_assess(board):
    from Phantom.ai.pos_eval.piece_tables import white_knights, black_knights
    #from Phantom.constants import grid_width
    score = 0
    for piece in board.get_piece_list(ptype='knight'):
        # x, y = piece.coord.x, (grid_width - piece.coord.y) - 1
        if piece.color == 'white':
            score += white_knights[piece.y][piece.x]
        elif piece.color == 'black':
            score += black_knights[piece.y][piece.x]
    return score
all_rules.append(knight_assess)

@call_trace(3)
def bishop_assess(board):
    from Phantom.ai.pos_eval.piece_tables import white_bishops, black_bishops
    #from Phantom.constants import grid_height
    score = 0
    for piece in board.get_piece_list(ptype='bishop'):
        # x, y = piece.coord.x, (grid_height - piece.coord.y) - 1
        if piece.color == 'white':
            score += white_bishops[piece.y][piece.x]
        elif piece.color == 'black':
            score += black_bishops[piece.y][piece.x]
    return score
all_rules.append(bishop_assess)

@call_trace(3)
def rook_assess(board):
    from Phantom.ai.pos_eval.piece_tables import white_rooks, black_rooks
    #from Phantom.constants import grid_height
    score = 0
    for piece in board.get_piece_list(ptype='rook'):
        # x, y = piece.coord.x, (grid_height - piece.coord.y) - 1
        if piece.color == 'white':
            score += white_rooks[piece.y][piece.x]
        elif piece.color == 'black':
            score += black_rooks[piece.y][piece.x]
    return score
all_rules.append(rook_assess)

@call_trace(3)
def queen_assess(board):
    from Phantom.ai.pos_eval.piece_tables import white_queens, black_queens
    #from Phantom.constants import grid_height
    score = 0
    for piece in board.get_piece_list(ptype='queen'):
        # x, y = piece.coord.x, (grid_height - piece.coord.y) - 1
        if piece.color == 'white':
            score += white_queens[piece.y][piece.x]
        elif piece.color == 'black':
            score += black_queens[piece.y][piece.x]
    return score
all_rules.append(queen_assess)

@call_trace(3)
def king_assess(board):
    from Phantom.ai.pos_eval.piece_tables import (white_kings, black_kings,
                                                  white_kings_endgame,
                                                  black_kings_endgame)
    from Phantom.ai.phases import Phase
    #from Phantom.constants import grid_height
    score = 0
    phase = Phase.analyze(board)
    if phase in (Phase.opening, Phase.midgame):
        for piece in board.get_piece_list(ptype='king'):
            # x, y = piece.coord.x, (grid_height - piece.coord.y) - 1
            if piece.color == 'white':
                score += white_kings[piece.y][piece.x]
            elif piece.color == 'black':
                score += black_kings[piece.y][piece.x]
    elif phase == Phase.endgame:
        for piece in board.get_piece_list(ptype='king'):
            # x, y = piece.coord.x, (grid_height - piece.coord.y) - 1
            if piece.color == 'white':
                score += white_kings_endgame[piece.y][piece.x]
            elif piece.color == 'black':
                score += black_kings_endgame[piece.y][piece.x]
    return score
all_rules.append(king_assess)

# tests...

def main(clear=True):
    from Phantom.utils.debug import log_msg, clear_log
    from Phantom.core.game_class import load_game # ChessGame
    if clear:
        clear_log()
    log_msg('Testing Phantom.ai.pos_eval.heuristics functions', 0)
    g = load_game('Game 1')
    log_msg('Testing AI heuristics on savegame "Game 1":', 0)
    score = 0
    for rule in all_rules:
        #try:
            log_msg(rule.__name__ + " evaluating...", 0)
            r = rule(g.board)
            log_msg(rule.__name__ + ' returned {}'.format(r), 0)
            score += r
        #except Exception as e:
        #    log_msg('{} failed:\n{}'.format(f.__name__, e), 0, err=True)
    log_msg('Test complete', 0)
    return score

if __name__ == '__main__':
    score = main()
    print(score)
