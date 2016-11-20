#!/usr/bin/env python
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

"""Run all the tests in the Phantom.tests"""

from Phantom.utils.debug import log_msg, clear_log
import os
import inspect

def main(*args):
    clear_log()
    log_msg('Phantom beginning self-test', 0, mark=True)
    testdir = inspect.getfile(main)
    testdir, dirname = os.path.split(testdir)

    for f in os.listdir(testdir):
        if f in (dirname, '__init__.py'):
            continue
        else:
            mn = f[:f.index('.')]
            m = __import__(mn)
            m.main(False)
    log_msg('Phantom self-test complete', 0, mark=True)

if __name__ == '__main__':
    main()
