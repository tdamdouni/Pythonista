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

"""Game timer.
Similar in use to `timeit.timeit()`, but is much more flexible and (I find) easier to use."""

import time
from Phantom.core.chessobj import PhantomObj

class Timer (PhantomObj):

    def __init__(self, active=True):
        self.is_active = active
        self.init_time = time.time()
        self.start_time = self.init_time
        self.stopped_total = 0
        self.stop_time = self.init_time
        self.pause_time = self.init_time if not active else None
        self.resume_time = None

    def start(self):
        self.is_active = True
        self.start_time = time.time()

    def stop(self):
        self.is_active = False
        self.stop_time = time.time()

    def pause(self):
        self.pause_time = time.time()
        self.is_active = False

    def resume(self):
        self.resume_time = time.time()
        self.is_active = True
        self.stopped_total += self.resume_time - self.pause_time
        self.pause_time = self.resume_time = None

    def get_total(self):
        return (self.stop_time or time.time()) - self.start_time

    def get_run(self):
        totaltime = self.get_total()
        return totaltime - self.stopped_total
