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

"""Math functions that are useful for chess."""

import math
'''
def dist(p1, p2):
    if p1.x == p2.x:
        return abs(p2.y - p1.y)
    else:
        dx = abs(p2.x - p1.x)
        dy = abs(p2.y - p1.y)
        return math.sqrt(dx**2 + dy**2)
'''
def round_down(x, place=1):
    val = math.trunc(x*place) / float(place)
    return int(val) if int(val) == val else val

#def round_up(x):
#    return round_down(x) + 1

if __name__ == '__main__':
    print('=' * 35)
    fmt = 'round_down({}, {:>2}) --> {}'
    for i in xrange(20):
        print(fmt.format(math.pi, i+1, round_down(math.pi, i+1)))
