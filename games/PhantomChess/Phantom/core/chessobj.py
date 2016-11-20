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

"""A short & simple class for all Phantom objects to inherit from.

This file is 1 level import clean."""

from Phantom.utils.debug import log_msg

class_record = {}

class PhantomObj (object):

    name = "object"

    def __new__(cls, *args, **kwargs):
        inst = object.__new__(cls)
        log_msg('created object of type {}'.format(cls.__name__), 10)

        # keep track of number of instances of each class
        class_record[cls] = class_record.get(cls, 0) + 1
        return inst

    def __repr__(self):
        return "<{}.{} object at {}>".format(__name__, self.__class__.__name__, hex(id(self)))

    def __del__(self):
        if log_msg:  # ccc: it is unclear to me why log_msg == None
            log_msg('object of type {} deleted'.format(self.__class__.__name__), 10)
        if class_record:  # ccc: it is unclear to me why class_record == None
            if self.__class__ in class_record:
                # 671: i don't know why self.__class__ wouldn't be in class_record
                class_record[self.__class__] -= 1

    def __eq__(self, other):
        idmatch = id(self) == id(other)
        if idmatch:
            return True

        typematch = isinstance(other, self.__class__)
        if not typematch:
            return False

        contentmatch = self.__dict__.items() == other.__dict__.items()
        return contentmatch
