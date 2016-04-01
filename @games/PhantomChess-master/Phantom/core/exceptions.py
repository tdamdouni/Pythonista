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

"""Exceptions used in Phantom."""

from Phantom.core.chessobj import PhantomObj

__all__ = []

class ChessError (Exception, PhantomObj):

    # 671: should call Exception.__init__ here? It's been working fine so I
    #      don't see a need to, but it could prevent future issues
    def __init__(self, msg='No error message supplied', caller=None):
        self.msg = self.message = msg
        self.name = self.__class__.__name__
        self.caller = caller

    def __str__(self):
        if self.caller:
            return '{} sourced at {}'.format(repr(self.msg), repr(self.caller))
        else:
            return '{} with no source'.format(repr(self.msg))

    def __repr__(self):
        return self.__str__()
__all__.append('ChessError')

class InvalidMove (ChessError): pass
__all__.append('InvalidMove')

class InvalidDimension (ChessError):pass
__all__.append('InvalidDimension')

class LogicError (ChessError): pass
__all__.append('LogicError')
