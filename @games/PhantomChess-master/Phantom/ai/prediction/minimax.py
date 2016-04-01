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

"""A minimax algorithim

By chance, this happens to be a clean import.  Nothing is needed.
"""

# Pseudocode
# src- Wikipedia article on minimax algorithim
#––––––––––––––––––––––––––––––––––––––––––––––––––––
# function minimax(node, depth, maximizingPlayer)
#     if depth = 0 or node is a terminal node
#         return the heuristic value of node
#     if maximizingPlayer
#         bestValue := -∞
#         for each child of node
#             val := minimax(child, depth - 1, FALSE)
#             bestValue := max(bestValue, val)
#         return bestValue
#     else
#         bestValue := +∞
#         for each child of node
#             val := minimax(child, depth - 1, TRUE)
#             bestValue := min(bestValue, val)
#         return bestValue
#
# (* Initial call for maximizing player *)
# minimax(origin, depth, TRUE)

def minimax_value(node, depth, maximizing):
    if depth <= 0 or node.is_terminal:
        return node.score
    if maximizing:
        f = max
        bestvalue = float('-inf')
    else:
        f = min
        bestvalue = float('inf')
    for child in node.children:
        val = minimax_value(child, depth - 1, not maximizing)
        bestvalue = f(bestvalue, val)
    return bestvalue
