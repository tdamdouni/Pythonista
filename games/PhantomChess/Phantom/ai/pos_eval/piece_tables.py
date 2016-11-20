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

"""Piece-square tables.  Ratings based on the postion of a piece and it's type.
This file is import clean.

The idea behind the lists in this file is to represent a chessboard.  Each list with in a list is 8 pieces long
and each 'master' list is 8 lists long.  This means there are 64 elements total in each list.  Those elements
are the ratings of the squares for the piece type (that the list is named for).  For example, a white pawn at
the coordinate (3, 3) will recieve a bonus of 20 points.
"""

white_pawns = [
[0,   0,   0,   0,   0,   0,   0,   0  ],
[50,  50,  50,  50,  50,  50,  50,  50 ],
[10,  10,  20,  30,  30,  20,  10,  10 ],
[5,   5,   10,  25,  25,  10,  5,   5  ],
[0,   0,   0,   20,  20,  0,   0,   0  ],
[5,   -5,  -10, 0,   0,   -10, -5,  -5 ],
[5,   10,  10,  -20, -20, 10,  10,  5  ],
[0,   0,   0,   0,   0,   0,   0,   0  ]]
black_pawns = [[-k for k in row] for row in white_pawns[::-1]]

white_knights = [
[-50, -40, -30, -30, -30, -30, -40, -50],
[-40, -20, 0,   0,   0,   0,   -20, -40],
[-30, 0,   10,  15,  15,  10,  0,   -30],
[-30, 5,   15,  20,  20,  15,  5,   -30],
[-30, 0,   15,  20,  20,  15,  0,   -30],
[-30, 5,   10,  15,  15,  10,  5,   -30],
[-40, -20, 0,   5,   5,   0,   -20, -40],
[-50, -40, -30, -30, -30, -30, -40, -50]]
black_knights = [[-k for k in row] for row in white_knights[::-1]]

white_bishops = [
[-20, -10, -10, -10, -10, -10, -10, -20],
[-10, 0,   0,   0,   0,   0,   0,   -10],
[-10, 0,   5,   10,  10,  5,   0,   -10],
[-10, 5,   5,   10,  10,  5,   5,   -10],
[-10, 0,   10,  10,  10,  10,  0,   -10],
[-10, 10,  10,  10,  10,  10,  10,  -10],
[-10, 12,  0,   0,   0,   0,   12,  -10],  # encourage fianchettos
[-20, -10, -10, -10, -10, -10, -10, -20]]
black_bishops = [[-k for k in row] for row in white_bishops[::-1]]

white_rooks = [
[0,   0,   0,   0,   0,   0,   0,   0  ],
[5,   10,  10,  10,  10,  10,  10,  5  ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ],
[-5,  0,   0,   0,   0,   0,   0,   -5 ]]
black_rooks = [[-k for k in row] for row in white_rooks[::-1]]

white_queens = [
[-20, -10, -10, -5,  -5,  -10, -10, -20],
[-10, 0,   0,   0,   0,   0,   0,   -10],
[-10, 0,   5,   5,   5,   5,   0,   -10],
[-5,  0,   5,   5,   5,   5,   0,   -5 ],
[0,   0,   5,   5,   5,   5,   0,   -5 ],
[-10, 5,   5,   5,   5,   5,   0,   -10],
[-10, 0,   5,   0,   0,   0,   0,   -10],
[-20, -10, -10, -5,  -5,  -10, -10, -20]]
black_queens = [[-k for k in row] for row in white_queens[::-1]]

white_kings = [
[-30, -40, -40, -50, -50, -40, -40, -30],
[-30, -40, -40, -50, -50, -40, -40, -30],
[-30, -40, -40, -50, -50, -40, -40, -30],
[-30, -40, -40, -50, -50, -40, -40, -30],
[-20, -30, -30, -40, -40, -30, -30, -20],
[-10, -20, -20, -30, -30, -20, -20, -10],
[20,  20,  0,   0,   0,   0,   20,  20 ],
[20,  30,  30,  10,  0,   10,  30,  20 ]]
black_kings = [[-k for k in row] for row in white_kings[::-1]]

white_kings_endgame = [
[-50, -40, -30, -20, -20, -30, -40, -50],
[-30, -20, -10, 0,   0,   -10, -20, -30],
[-30, -10, 20,  30,  30,  20,  -10, -30],
[-30, -10, 30,  40,  40,  30,  -10, -30],
[-30, -10, 30,  40,  40,  30,  -10, -30],
[-30, -10, 20,  30,  30,  20,  -10, -30],
[-30, -30, 0,   0,   0,   0,   -30, -30],
[-50, -30, -30, -30, -30, -30, -30, -50]]
black_kings_endgame = [[-k for k in row] for row in white_kings_endgame[::-1]]
