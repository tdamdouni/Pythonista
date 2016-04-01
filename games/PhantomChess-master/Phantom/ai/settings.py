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

"""A separate constants.py file to save some space in the main one."""

from Phantom.functions import round_down

maxdepth = 2
window = 5

# Points-per-piece simple
scores = {'pawn'  : 100,
          'knight': 320,
          'bishop': 330,
          'rook'  : 500,
          'queen' : 900,
          'king'  : 20000}  # use 20000 to signal the capture of a king is better than all other options

king_material = 400  # use the endgame score for material worth totalling

max_material = (16*scores['pawn'] + 4*scores['knight'] + 4*scores['bishop']
               + 4*scores['rook'] + 2*scores['queen']  + 2*king_material)
min_material = 2*king_material

opening_range = [max_material,]
midgame_range = xrange(round_down(max_material / 4), int(max_material))
endgame_range = xrange(0, midgame_range[0])
opening_moves = 6

colors = {'white': 1, 'black': -1}

# Advanced heuristic scores

# avoid a knight on the edge; they are bad
knight_on_edge_score = -50

# use a different set of scores for farther developed pieces
developed_scores = {'pawn'  : 70,
                    'knight': 350,
                    'bishop': 400,
                    'rook'  : 600,
                    'queen' : 1000,
                    'king'  : 0}  # king development will be tested in a different heuristic

# pawns closer to promotion are much better
advanced_pawn_mul = 40

# pawns that are promotable are *very* good
promotable_bonus = 350

# the king gets a score in the endgame but not opening/midage
king_endgame = 400

# bonus for having both bishops
bishop_pair_bonus = 50

# castling is good in the opening, ok in the midgame, but pointless in the endgame
castle_opening_bonus = 70
castle_midgame_bonus = 30
castle_endgame_bonus = -400

# pawn structure analysis
doubled_pawn = -50
tripled_pawn = -75
pawn_ram = -75
isolated_pawn = -40
eight_pawns = -75
passed_pawn = 250

# although move moves are better, most possible moves in chess are pointless
mobility_mul = 10

# bishops where there are many pawns on the same color squares as the bishops
# are less useful
bad_bishop_mul = 30
