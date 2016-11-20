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

"""Determine if your platform supports printing of unicode characters."""

# See: http://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
# Windows users could try running 'chcp 65001' before running Phantom

import sys

def can_print_unicode(msg='Welcome to PhantomChess...'):
    try:
        print(str(u'♜ ♞ ♝ {} ♗ ♘ ♖ '.format(msg)))
        return True
    except UnicodeEncodeError:
        print(msg)
        return False

if __name__ == '__main__':
    print(can_print_unicode())
