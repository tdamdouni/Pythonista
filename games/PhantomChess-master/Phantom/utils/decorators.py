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

"""Some useful decorators used in Phantom."""

from Phantom.utils.debug import log_msg
from Phantom.constants import debug, exc_catch_cutoff

class named (object):

    def __init__(self, name):
        self.fname = name

    def __call__(self, f):

        def named_wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        named_wrapped.__name__ = self.fname
        return named_wrapped

class exc_catch (object):
    """Catch exceptions.  Basically, if something goes wrong in a function and it's not one of the
    specified `passes` list, return the specified value.  If it is in the `passes` list, return
    the function (which will reraise the exception)"""
    def __init__(self, *passes, **kwargs):
        self.passes = [c.__class__.__name__ for c in passes]
        self.name = kwargs.get('name', None)
        self.ret = kwargs.get('ret', None)
        self.log = kwargs.get('log', 0)

    def __call__(self, f):
        retval = self.ret
        name = self.name or f.__name__

        # 671: I don't understand why this doesnt work
        if debug > exc_catch_cutoff:
            return f

        @named(name)
        def exc_catch_wrapped(*args, **kwargs):
            e = None
            try:
                f(*args, **kwargs)
            except Exception as e:
                #if exc_catch_cutoff and debug > exc_catch_cutoff:
                if True:
                    # if debugging, print full tracebacks
                    import traceback
                    traceback.print_exc()  # prints a full stack trace
                if e.__class__.__name__ in self.passes:
                    return f(*args, **kwargs)
            finally:
                if e:
                    if e.__class__ in self.passes:
                        raise e
                    else:
                        if self.log:
                            fmt = 'exc_catch: caught an unpassed exception - {}:\n    {}'
                            log_msg(fmt.format(e.__class__.__name__, e.message), self.log, err=True)
                        return retval

        return exc_catch_wrapped

class default_args (object):

    """As it is possible to supply a default (optional) argument, one whos value can be specified at
    call time by `foo = 'bar'`, but not possible to supply a default to `*args`, this decorator allows
    that to be done."""

    def __init__(self, *args, **kwargs):
        self.d_args = args
        self.d_kwargs = kwargs

    def __call__(self, f):

        @named(f.__name__)
        def default_args_wrapped(*args, **kwargs):
            fargs = args or self.d_args
            fkwargs = kwargs or self.d_kwargs
            return f(*fargs, **fkwargs)

        return default_args_wrapped

def integer_args(f):
    """Convert any float arguments given to a function to be integers.
    This decorator does NOT convert values such as 1.5.
    The test to see if an argument will be converted is

    `int(arg) == arg`

    If that is True, then the argument is converted to an integer."""

    @named(f.__name__)
    def int_args_wrapped(*args, **kwargs):
        fixed_args = ()
        for arg in args:
            try:
                if int(arg) == arg:
                    fixed_args += (int(arg),)
                else:
                    fixed_args += (arg,)
            except (ValueError, TypeError):
                fixed_args += (arg,)
        fixed_kwargs = {}
        for key in kwargs:
            try:
                if int(kwargs[key]) == kwargs[key]:
                    fixed_kwargs.update({key: int(kwargs[key])})
                else:
                    fixed_kwargs.update({key: kwargs[key]})
            except (ValueError, TypeError):
                fixed_kwargs.update({key: kwargs[key]})

        return f(*fixed_args, **fixed_kwargs)

    return int_args_wrapped
