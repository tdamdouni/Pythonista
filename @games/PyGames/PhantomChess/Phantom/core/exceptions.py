# -*- coding: utf-8 -*-

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

__all__ = []

class ChessError (Exception): 
    def __init__(self, msg='No error message supplied', caller=None):
        self.msg = self.message = msg
        self.name = self.__class__.__name__
        self.caller = caller

    def __str__(self):
        if self.caller is not None:
            return repr(self.msg) + " sourced at {}".format(repr(self.caller))
        else:
            return repr(self.msg) + " with no source"

    def __repr__(self):
        return self.__str__()
__all__.append('ChessError')

class InvalidMove (ChessError): pass
__all__.append('InvalidMove')

class InvalidDimension (ChessError):pass
__all__.append('InvalidDimension')

class LogicError (ChessError): pass
__all__.append('LogicError')

