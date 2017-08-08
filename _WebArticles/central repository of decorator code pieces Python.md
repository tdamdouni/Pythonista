https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize

**This page is meant to be a central repository of decorator code pieces**, whether useful or not <wink>. It is NOT a page to discuss decorator syntax! 

Contents

  1. Creating Well-Behaved Decorators / "Decorator decorator"
  2. Property Definition
  3. Memoize
  4. Alternate memoize as nested functions
  5. Alternate memoize as dict subclass
  6. Cached Properties
  7. Retry
  8. Pseudo-currying
  9. Creating decorator with optional arguments
  10. Controllable DIY debug
  11. Easy adding methods to a class instance
  12. Counting function calls
  13. Alternate Counting function calls
  14. Generating Deprecation Warnings
  15. Smart deprecation warnings (with valid filenames, line numbers, etc.)
  16. Ignoring Deprecation Warnings
  17. Enable/Disable Decorators
  18. Easy Dump of Function Arguments
  19. Pre-/Post-Conditions
  20. Profiling/Coverage Analysis
  21. Line Tracing Individual Functions
  22. Synchronization
  23. Type Enforcement (accepts/returns)
  24. CGI method wrapper
  25. State Machine Implementaion
  26. C++/Java-keyword-like function decorators
  27. Different Decorator Forms
  28. Unimplemented function replacement
  29. Redirects stdout printing to python standard logging.
  30. Access control
  31. Events rising and handling
  32. Singleton
  33. The Sublime Singleton
  34. Asynchronous Call
  35. Class method decorator using instance
  36. Another Retrying Decorator
  37. Logging decorator with specified logger (or default)
  38. Lazy Thunkify
  39. Aggregative decorators for generator functions
  40. Function Timeout

## Creating Well-Behaved Decorators / "Decorator decorator"

Note: This is only one recipe. Others include inheritance from a standard decorator (link?), the [functools @wraps decorator](http://docs.python.org/dev/library/functools.html), and a factory function such as [Michele Simionato's decorator module](http://pypi.python.org/pypi/decorator) which even preserves signature information. 

    
    
       1 def simple_decorator(decorator):
       2     '''This decorator can be used to turn simple functions
       3     into well-behaved decorators, so long as the decorators
       4     are fairly simple. If a decorator expects a function and
       5     returns a function (no descriptors), and if it doesn't
       6     modify function attributes or docstring, then it is
       7     eligible to use this. Simply apply @simple_decorator to
       8     your decorator and it will automatically preserve the
       9     docstring and function attributes of functions to which
      10     it is applied.'''
      11     def new_decorator(f):
      12         g = decorator(f)
      13         g.__name__ = f.__name__
      14         g.__doc__ = f.__doc__
      15         g.__dict__.update(f.__dict__)
      16         return g
      17     # Now a few lines needed to make simple_decorator itself
      18     # be a well-behaved decorator.
      19     new_decorator.__name__ = decorator.__name__
      20     new_decorator.__doc__ = decorator.__doc__
      21     new_decorator.__dict__.update(decorator.__dict__)
      22     return new_decorator
      23 
      24 #
      25 # Sample Use:
      26 #
      27 @simple_decorator
      28 def my_simple_logging_decorator(func):
      29     def you_will_never_see_this_name(*args, **kwargs):
      30         print 'calling {}'.format(func.__name__)
      31         return func(*args, **kwargs)
      32     return you_will_never_see_this_name
      33 
      34 @my_simple_logging_decorator
      35 def double(x):
      36     'Doubles a number.'
      37     return 2 * x
      38 
      39 assert double.__name__ == 'double'
      40 assert double.__doc__ == 'Doubles a number.'
      41 print double(155)
    

## Property Definition

These decorators provide a readable way to define properties: 

    
    
       1 import sys
       2 
       3 def propget(func):
       4     locals = sys._getframe(1).f_locals
       5     name = func.__name__
       6     prop = locals.get(name)
       7     if not isinstance(prop, property):
       8         prop = property(func, doc=func.__doc__)
       9     else:
      10         doc = prop.__doc__ or func.__doc__
      11         prop = property(func, prop.fset, prop.fdel, doc)
      12     return prop
      13 
      14 def propset(func):
      15     locals = sys._getframe(1).f_locals
      16     name = func.__name__
      17     prop = locals.get(name)
      18     if not isinstance(prop, property):
      19         prop = property(None, func, doc=func.__doc__)
      20     else:
      21         doc = prop.__doc__ or func.__doc__
      22         prop = property(prop.fget, func, prop.fdel, doc)
      23     return prop
      24 
      25 def propdel(func):
      26     locals = sys._getframe(1).f_locals
      27     name = func.__name__
      28     prop = locals.get(name)
      29     if not isinstance(prop, property):
      30         prop = property(None, None, func, doc=func.__doc__)
      31     else:
      32         prop = property(prop.fget, prop.fset, func, prop.__doc__)
      33     return prop
      34 
      35 # These can be used like this:
      36 
      37 class Example(object):
      38 
      39     @propget
      40     def myattr(self):
      41         return self._half * 2
      42 
      43     @propset
      44     def myattr(self, value):
      45         self._half = value / 2
      46 
      47     @propdel
      48     def myattr(self):
      49         del self._half
    

Here's a way that doesn't require any new decorators: 

    
    
       1 class Example(object):
       2     @apply  # doesn't exist in Python 3
       3     def myattr():
       4         doc = '''This is the doc string.'''
       5 
       6         def fget(self):
       7             return self._half * 2
       8 
       9         def fset(self, value):
      10             self._half = value / 2
      11 
      12         def fdel(self):
      13             del self._half
      14 
      15         return property(**locals())
      16     #myattr = myattr()  # works in Python 2 and 3
    

Yet another property decorator: 

    
    
       1 try:
       2     # Python 2
       3     import __builtin__ as builtins
       4 except ImportError:
       5     # Python 3
       6     import builtins
       7 
       8 def property(function):
       9     keys = 'fget', 'fset', 'fdel'
      10     func_locals = {'doc':function.__doc__}
      11     def probe_func(frame, event, arg):
      12         if event == 'return':
      13             locals = frame.f_locals
      14             func_locals.update(dict((k, locals.get(k)) for k in keys))
      15             sys.settrace(None)
      16         return probe_func
      17     sys.settrace(probe_func)
      18     function()
      19     return builtins.property(**func_locals)
      20 
      21 #====== Example =======================================================
      22 
      23 from math import radians, degrees, pi
      24 
      25 class Angle(object):
      26     def __init__(self, rad):
      27         self._rad = rad
      28 
      29     @property
      30     def rad():
      31         '''The angle in radians'''
      32         def fget(self):
      33             return self._rad
      34         def fset(self, angle):
      35             if isinstance(angle, Angle):
      36                 angle = angle.rad
      37             self._rad = float(angle)
      38 
      39     @property
      40     def deg():
      41         '''The angle in degrees'''
      42         def fget(self):
      43             return degrees(self._rad)
      44         def fset(self, angle):
      45             if isinstance(angle, Angle):
      46                 angle = angle.deg
      47             self._rad = radians(angle)
    

## Memoize

Here's a memoizing class. 

    
    
       1 import collections
       2 import functools
       3 
       4 class memoized(object):
       5    '''Decorator. Caches a function's return value each time it is called.
       6    If called later with the same arguments, the cached value is returned
       7    (not reevaluated).
       8    '''
       9    def __init__(self, func):
      10       self.func = func
      11       self.cache = {}
      12    def __call__(self, *args):
      13       if not isinstance(args, collections.Hashable):
      14          # uncacheable. a list, for instance.
      15          # better to not cache than blow up.
      16          return self.func(*args)
      17       if args in self.cache:
      18          return self.cache[args]
      19       else:
      20          value = self.func(*args)
      21          self.cache[args] = value
      22          return value
      23    def __repr__(self):
      24       '''Return the function's docstring.'''
      25       return self.func.__doc__
      26    def __get__(self, obj, objtype):
      27       '''Support instance methods.'''
      28       return functools.partial(self.__call__, obj)
      29 
      30 @memoized
      31 def fibonacci(n):
      32    "Return the nth fibonacci number."
      33    if n in (0, 1):
      34       return n
      35    return fibonacci(n-1) + fibonacci(n-2)
      36 
      37 print fibonacci(12)
    

## Alternate memoize as nested functions

Here's a memoizing function that works on functions, methods, or classes, and exposes the cache publicly. 

    
    
       1 # note that this decorator ignores **kwargs
       2 def memoize(obj):
       3     cache = obj.cache = {}
       4 
       5     @functools.wraps(obj)
       6     def memoizer(*args, **kwargs):
       7         if args not in cache:
       8             cache[args] = obj(*args, **kwargs)
       9         return cache[args]
      10     return memoizer
    

Here's a modified version that also respects kwargs. 

    
    
       1 def memoize(obj):
       2     cache = obj.cache = {}
       3 
       4     @functools.wraps(obj)
       5     def memoizer(*args, **kwargs):
       6         key = str(args) + str(kwargs)
       7         if key not in cache:
       8             cache[key] = obj(*args, **kwargs)
       9         return cache[key]
      10     return memoizer
    

## Alternate memoize as dict subclass

This is an idea that interests me, but it only seems to work on functions: 

    
    
       1 class memoize(dict):
       2     def __init__(self, func):
       3         self.func = func
       4 
       5     def __call__(self, *args):
       6         return self[args]
       7 
       8     def __missing__(self, key):
       9         result = self[key] = self.func(*key)
      10         return result
      11 
      12 #
      13 # Sample use
      14 #
      15 
      16 >>> @memoize
      17 ... def foo(a, b):
      18 ...     return a * b
      19 >>> foo(2, 4)
      20 8
      21 >>> foo
      22 {(2, 4): 8}
      23 >>> foo('hi', 3)
      24 'hihihi'
      25 >>> foo
      26 {(2, 4): 8, ('hi', 3): 'hihihi'}
    

## Cached Properties

    
    
       1 #
       2 # © 2011 Christopher Arndt, MIT License
       3 #
       4 
       5 import time
       6 
       7 class cached_property(object):
       8     '''Decorator for read-only properties evaluated only once within TTL period.
       9 
      10     It can be used to create a cached property like this::
      11 
      12         import random
      13 
      14         # the class containing the property must be a new-style class
      15         class MyClass(object):
      16             # create property whose value is cached for ten minutes
      17             @cached_property(ttl=600)
      18             def randint(self):
      19                 # will only be evaluated every 10 min. at maximum.
      20                 return random.randint(0, 100)
      21 
      22     The value is cached  in the '_cache' attribute of the object instance that
      23     has the property getter method wrapped by this decorator. The '_cache'
      24     attribute value is a dictionary which has a key for every property of the
      25     object which is wrapped by this decorator. Each entry in the cache is
      26     created only when the property is accessed for the first time and is a
      27     two-element tuple with the last computed property value and the last time
      28     it was updated in seconds since the epoch.
      29 
      30     The default time-to-live (TTL) is 300 seconds (5 minutes). Set the TTL to
      31     zero for the cached value to never expire.
      32 
      33     To expire a cached property value manually just do::
      34 
      35         del instance._cache[<property name>]
      36 
      37     '''
      38     def __init__(self, ttl=300):
      39         self.ttl = ttl
      40 
      41     def __call__(self, fget, doc=None):
      42         self.fget = fget
      43         self.__doc__ = doc or fget.__doc__
      44         self.__name__ = fget.__name__
      45         self.__module__ = fget.__module__
      46         return self
      47 
      48     def __get__(self, inst, owner):
      49         now = time.time()
      50         try:
      51             value, last_update = inst._cache[self.__name__]
      52             if self.ttl > 0 and now - last_update > self.ttl:
      53                 raise AttributeError
      54         except (KeyError, AttributeError):
      55             value = self.fget(inst)
      56             try:
      57                 cache = inst._cache
      58             except AttributeError:
      59                 cache = inst._cache = {}
      60             cache[self.__name__] = (value, now)
      61         return value
    

## Retry

Call a function which returns True/False to indicate success or failure. On failure, wait, and try the function again. On repeated failures, wait longer between each successive attempt. If the decorator runs out of attempts, then it gives up and returns False, but you could just as easily raise some exception. 

    
    
       1 import time
       2 import math
       3 
       4 # Retry decorator with exponential backoff
       5 def retry(tries, delay=3, backoff=2):
       6   '''Retries a function or method until it returns True.
       7 
       8   delay sets the initial delay in seconds, and backoff sets the factor by which
       9   the delay should lengthen after each failure. backoff must be greater than 1,
      10   or else it isn't really a backoff. tries must be at least 0, and delay
      11   greater than 0.'''
      12 
      13   if backoff <= 1:
      14     raise ValueError("backoff must be greater than 1")
      15 
      16   tries = math.floor(tries)
      17   if tries < 0:
      18     raise ValueError("tries must be 0 or greater")
      19 
      20   if delay <= 0:
      21     raise ValueError("delay must be greater than 0")
      22 
      23   def deco_retry(f):
      24     def f_retry(*args, **kwargs):
      25       mtries, mdelay = tries, delay # make mutable
      26 
      27       rv = f(*args, **kwargs) # first attempt
      28       while mtries > 0:
      29         if rv is True: # Done on success
      30           return True
      31 
      32         mtries -= 1      # consume an attempt
      33         time.sleep(mdelay) # wait...
      34         mdelay *= backoff  # make future wait longer
      35 
      36         rv = f(*args, **kwargs) # Try again
      37 
      38       return False # Ran out of tries :-(
      39 
      40     return f_retry # true decorator -> decorated function
      41   return deco_retry  # @retry(arg[, ...]) -> true decorator
    

## Pseudo-currying

(FYI you can use functools.partial() to emulate currying (which works even for keyword arguments)) 

    
    
       1 class curried(object):
       2   '''
       3   Decorator that returns a function that keeps returning functions
       4   until all arguments are supplied; then the original function is
       5   evaluated.
       6   '''
       7 
       8   def __init__(self, func, *a):
       9     self.func = func
      10     self.args = a
      11 
      12   def __call__(self, *a):
      13     args = self.args + a
      14     if len(args) < self.func.func_code.co_argcount:
      15       return curried(self.func, *args)
      16     else:
      17       return self.func(*args)
      18 
      19 
      20 @curried
      21 def add(a, b):
      22     return a + b
      23 
      24 add1 = add(1)
      25 
      26 print add1(2)
    

## Creating decorator with optional arguments

    
    
       1 import functools, inspect
       2 
       3 def decorator(func):
       4     ''' Allow to use decorator either with arguments or not. '''
       5 
       6     def isFuncArg(*args, **kw):
       7         return len(args) == 1 and len(kw) == 0 and (
       8             inspect.isfunction(args[0]) or isinstance(args[0], type))
       9 
      10     if isinstance(func, type):
      11         def class_wrapper(*args, **kw):
      12             if isFuncArg(*args, **kw):
      13                 return func()(*args, **kw) # create class before usage
      14             return func(*args, **kw)
      15         class_wrapper.__name__ = func.__name__
      16         class_wrapper.__module__ = func.__module__
      17         return class_wrapper
      18 
      19     @functools.wraps(func)
      20     def func_wrapper(*args, **kw):
      21         if isFuncArg(*args, **kw):
      22             return func(*args, **kw)
      23 
      24         def functor(userFunc):
      25             return func(userFunc, *args, **kw)
      26 
      27         return functor
      28 
      29     return func_wrapper
    

Example: 

    
    
       1 @decorator
       2 def apply(func, *args, **kw):
       3     return func(*args, **kw)
       4 
       5 @decorator
       6 class apply:
       7     def __init__(self, *args, **kw):
       8         self.args = args
       9         self.kw   = kw
      10 
      11     def __call__(self, func):
      12         return func(*self.args, **self.kw)
      13 
      14 #
      15 # Usage in both cases:
      16 #
      17 @apply
      18 def test():
      19     return 'test'
      20 
      21 assert test == 'test'
      22 
      23 @apply(2, 3)
      24 def test(a, b):
      25     return a + b
      26 
      27 assert test is 5
    

Note: There is only one drawback: wrapper checks its arguments for single function or class. To avoid wrong behavior you can use keyword arguments instead of positional, e.g.: 

    
    
       1 @decorator
       2 def my_property(getter, *, setter=None, deleter=None, doc=None):
       3     return property(getter, setter, deleter, doc)
    

## Controllable DIY debug

(Other hooks could be similarly added. Docstrings and exceptions are left out for simplicity of demonstration.) 

    
    
       1 import sys
       2 
       3 WHAT_TO_DEBUG = set(['io', 'core'])  # change to what you need
       4 
       5 class debug:
       6     '''Decorator which helps to control what aspects of a program to debug
       7     on per-function basis. Aspects are provided as list of arguments.
       8     It DOESN'T slowdown functions which aren't supposed to be debugged.
       9     '''
      10     def __init__(self, aspects=None):
      11         self.aspects = set(aspects)
      12 
      13     def __call__(self, f):
      14         if self.aspects & WHAT_TO_DEBUG:
      15             def newf(*args, **kwds):
      16                 print >> sys.stderr, f.func_name, args, kwds
      17                 f_result = f(*args, **kwds)
      18                 print >> sys.stderr, f.func_name, "returned", f_result
      19                 return f_result
      20             newf.__doc__ = f.__doc__
      21             return newf
      22         else:
      23             return f
      24 
      25 @debug(['io'])
      26 def prn(x):
      27     print x
      28 
      29 @debug(['core'])
      30 def mult(x, y):
      31     return x * y
      32 
      33 prn(mult(2, 2))
    

## Easy adding methods to a class instance

Credits to John Roth. 

    
    
       1 class Foo:
       2     def __init__(self):
       3         self.x = 42
       4 
       5 foo = Foo()
       6 
       7 def addto(instance):
       8     def decorator(f):
       9         import types
      10         f = types.MethodType(f, instance, instance.__class__)
      11         setattr(instance, f.func_name, f)
      12         return f
      13     return decorator
      14 
      15 @addto(foo)
      16 def print_x(self):
      17     print self.x
      18 
      19 # foo.print_x() would print "42"
    

## Counting function calls

    
    
       1 class countcalls(object):
       2    "Decorator that keeps track of the number of times a function is called."
       3 
       4    __instances = {}
       5 
       6    def __init__(self, f):
       7       self.__f = f
       8       self.__numcalls = 0
       9       countcalls.__instances[f] = self
      10 
      11    def __call__(self, *args, **kwargs):
      12       self.__numcalls += 1
      13       return self.__f(*args, **kwargs)
      14 
      15    @staticmethod
      16    def count(f):
      17       "Return the number of times the function f was called."
      18       return countcalls.__instances[f].__numcalls
      19 
      20    @staticmethod
      21    def counts():
      22       "Return a dict of {function: # of calls} for all registered functions."
      23       return dict([(f, countcalls.count(f)) for f in countcalls.__instances])
    

## Alternate Counting function calls

    
    
       1 class countcalls(object):
       2    "Decorator that keeps track of the number of times a function is called."
       3 
       4    __instances = {}
       5 
       6    def __init__(self, f):
       7       self.__f = f
       8       self.__numcalls = 0
       9       countcalls.__instances[f] = self
      10 
      11    def __call__(self, *args, **kwargs):
      12       self.__numcalls += 1
      13       return self.__f(*args, **kwargs)
      14 
      15    def count(self):
      16       "Return the number of times the function f was called."
      17       return countcalls.__instances[self.__f].__numcalls
      18 
      19    @staticmethod
      20    def counts():
      21       "Return a dict of {function: # of calls} for all registered functions."
      22       return dict([(f.__name__, countcalls.__instances[f].__numcalls) for f in countcalls.__instances])
      23 
      24 #example
      25 
      26 @countcalls
      27 def f():
      28    print 'f called'
      29 
      30 @countcalls
      31 def g():
      32    print 'g called'
      33 
      34 f()
      35 f()
      36 f()
      37 print f.count() # prints 3
      38 print countcalls.counts() # same as f.counts() or g.counts()
      39 g()
      40 print g.count() # prints 1
    

## Generating Deprecation Warnings

    
    
       1 import warnings
       2 
       3 def deprecated(func):
       4     '''This is a decorator which can be used to mark functions
       5     as deprecated. It will result in a warning being emitted
       6     when the function is used.'''
       7     def new_func(*args, **kwargs):
       8         warnings.warn("Call to deprecated function {}.".format(func.__name__),
       9                       category=DeprecationWarning)
      10         return func(*args, **kwargs)
      11     new_func.__name__ = func.__name__
      12     new_func.__doc__ = func.__doc__
      13     new_func.__dict__.update(func.__dict__)
      14     return new_func
      15 
      16 # === Examples of use ===
      17 
      18 @deprecated
      19 def some_old_function(x,y):
      20     return x + y
      21 
      22 class SomeClass:
      23     @deprecated
      24     def some_old_method(self, x,y):
      25         return x + y
    

## Smart deprecation warnings (with valid filenames, line numbers, etc.)

    
    
       1 import warnings
       2 import functools
       3 
       4 
       5 def deprecated(func):
       6     '''This is a decorator which can be used to mark functions
       7     as deprecated. It will result in a warning being emitted
       8     when the function is used.'''
       9 
      10     @functools.wraps(func)
      11     def new_func(*args, **kwargs):
      12         warnings.warn_explicit(
      13             "Call to deprecated function {}.".format(func.__name__),
      14             category=DeprecationWarning,
      15             filename=func.func_code.co_filename,
      16             lineno=func.func_code.co_firstlineno + 1
      17         )
      18         return func(*args, **kwargs)
      19     return new_func
      20 
      21 
      22 ## Usage examples ##
      23 @deprecated
      24 def my_func():
      25     pass
      26 
      27 @other_decorators_must_be_upper
      28 @deprecated
      29 def my_func():
      30     pass
    

## Ignoring Deprecation Warnings

    
    
       1 import warnings
       2 
       3 def ignore_deprecation_warnings(func):
       4     '''This is a decorator which can be used to ignore deprecation warnings
       5     occurring in a function.'''
       6     def new_func(*args, **kwargs):
       7         with warnings.catch_warnings():
       8             warnings.filterwarnings("ignore", category=DeprecationWarning)
       9             return func(*args, **kwargs)
      10     new_func.__name__ = func.__name__
      11     new_func.__doc__ = func.__doc__
      12     new_func.__dict__.update(func.__dict__)
      13     return new_func
      14 
      15 # === Examples of use ===
      16 
      17 @ignore_deprecation_warnings
      18 def some_function_raising_deprecation_warning():
      19     warnings.warn("This is a deprecationg warning.",
      20                   category=DeprecationWarning)
      21 
      22 class SomeClass:
      23     @ignore_deprecation_warnings
      24     def some_method_raising_deprecation_warning():
      25         warnings.warn("This is a deprecationg warning.",
      26                       category=DeprecationWarning)
    

## Enable/Disable Decorators

    
    
       1 def unchanged(func):
       2     "This decorator doesn't add any behavior"
       3     return func
       4 
       5 def disabled(func):
       6     "This decorator disables the provided function, and does nothing"
       7     def empty_func(*args,**kargs):
       8         pass
       9     return empty_func
      10 
      11 # define this as equivalent to unchanged, for nice symmetry with disabled
      12 enabled = unchanged
      13 
      14 #
      15 # Sample use
      16 #
      17 
      18 GLOBAL_ENABLE_FLAG = True
      19 
      20 state = enabled if GLOBAL_ENABLE_FLAG else disabled
      21 @state
      22 def special_function_foo():
      23     print "function was enabled"
    

## Easy Dump of Function Arguments

    
    
       1 def dump_args(func):
       2     "This decorator dumps out the arguments passed to a function before calling it"
       3     argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
       4     fname = func.func_name
       5 
       6     def echo_func(*args,**kwargs):
       7         print fname, ":", ', '.join(
       8             '%s=%r' % entry
       9             for entry in zip(argnames,args) + kwargs.items())
      10         return func(*args, **kwargs)
      11 
      12     return echo_func
      13 
      14 @dump_args
      15 def f1(a,b,c):
      16     print a + b + c
      17 
      18 f1(1, 2, 3)
    

## Pre-/Post-Conditions

    
    
       1 '''
       2 Provide pre-/postconditions as function decorators.
       3 
       4 Example usage:
       5 
       6   >>> def in_ge20(inval):
       7   ...    assert inval >= 20, 'Input value < 20'
       8   ...
       9   >>> def out_lt30(retval, inval):
      10   ...    assert retval < 30, 'Return value >= 30'
      11   ...
      12   >>> @precondition(in_ge20)
      13   ... @postcondition(out_lt30)
      14   ... def inc(value):
      15   ...   return value + 1
      16   ...
      17   >>> inc(5)
      18   Traceback (most recent call last):
      19     ...
      20   AssertionError: Input value < 20
      21   >>> inc(29)
      22   Traceback (most recent call last):
      23     ...
      24   AssertionError: Return value >= 30
      25   >>> inc(20)
      26   21
      27 
      28 You can define as many pre-/postconditions for a function as you
      29 like. It is also possible to specify both types of conditions at once:
      30 
      31   >>> @conditions(in_ge20, out_lt30)
      32   ... def add1(value):
      33   ...   return value + 1
      34   ...
      35   >>> add1(5)
      36   Traceback (most recent call last):
      37     ...
      38   AssertionError: Input value < 20
      39 
      40 An interesting feature is the ability to prevent the creation of
      41 pre-/postconditions at function definition time. This makes it
      42 possible to use conditions for debugging and then switch them off for
      43 distribution.
      44 
      45   >>> debug = False
      46   >>> @precondition(in_ge20, debug)
      47   ... def dec(value):
      48   ...   return value - 1
      49   ...
      50   >>> dec(5)
      51   4
      52 '''
      53 
      54 __all__ = ['precondition', 'postcondition', 'conditions']
      55 
      56 DEFAULT_ON = True
      57 
      58 def precondition(precondition, use_conditions=DEFAULT_ON):
      59     return conditions(precondition, None, use_conditions)
      60 
      61 def postcondition(postcondition, use_conditions=DEFAULT_ON):
      62     return conditions(None, postcondition, use_conditions)
      63 
      64 class conditions(object):
      65     __slots__ = ('__precondition', '__postcondition')
      66 
      67     def __init__(self, pre, post, use_conditions=DEFAULT_ON):
      68         if not use_conditions:
      69             pre, post = None, None
      70 
      71         self.__precondition  = pre
      72         self.__postcondition = post
      73 
      74     def __call__(self, function):
      75         # combine recursive wrappers (@precondition + @postcondition == @conditions)
      76         pres  = set((self.__precondition,))
      77         posts = set((self.__postcondition,))
      78 
      79         # unwrap function, collect distinct pre-/post conditions
      80         while type(function) is FunctionWrapper:
      81             pres.add(function._pre)
      82             posts.add(function._post)
      83             function = function._func
      84 
      85         # filter out None conditions and build pairs of pre- and postconditions
      86         conditions = map(None, filter(None, pres), filter(None, posts))
      87 
      88         # add a wrapper for each pair (note that 'conditions' may be empty)
      89         for pre, post in conditions:
      90             function = FunctionWrapper(pre, post, function)
      91 
      92         return function
      93 
      94 class FunctionWrapper(object):
      95     def __init__(self, precondition, postcondition, function):
      96         self._pre  = precondition
      97         self._post = postcondition
      98         self._func = function
      99 
     100     def __call__(self, *args, **kwargs):
     101         precondition  = self._pre
     102         postcondition = self._post
     103 
     104         if precondition:
     105             precondition(*args, **kwargs)
     106         result = self._func(*args, **kwargs)
     107         if postcondition:
     108             postcondition(result, *args, **kwargs)
     109         return result
     110 
     111 def __test():
     112     import doctest
     113     doctest.testmod()
     114 
     115 if __name__ == "__main__":
     116     __test()
    

## Profiling/Coverage Analysis

The code and examples are a bit longish, so I'll include a link instead: <http://mg.pov.lt/blog/profiling.html>

## Line Tracing Individual Functions

I cobbled this together from the trace module. It allows you to decorate individual functions so their lines are traced. I think it works out to be a slightly smaller hammer than running the trace module and trying to pare back what it traces using exclusions. 

    
    
       1 import sys
       2 import os
       3 import linecache
       4 
       5 def trace(f):
       6     def globaltrace(frame, why, arg):
       7         if why == "call":
       8             return localtrace
       9         return None
      10 
      11     def localtrace(frame, why, arg):
      12         if why == "line":
      13             # record the file name and line number of every trace
      14             filename = frame.f_code.co_filename
      15             lineno = frame.f_lineno
      16 
      17             bname = os.path.basename(filename)
      18             print "{}({}): {}".format(  bname,
      19                                         lineno,
      20                                         linecache.getline(filename, lineno)),
      21         return localtrace
      22 
      23     def _f(*args, **kwds):
      24         sys.settrace(globaltrace)
      25         result = f(*args, **kwds)
      26         sys.settrace(None)
      27         return result
      28 
      29     return _f
    

## Synchronization

Synchronize two (or more) functions on a given lock. 

    
    
       1 def synchronized(lock):
       2     '''Synchronization decorator.'''
       3 
       4     def wrap(f):
       5         def new_function(*args, **kw):
       6             lock.acquire()
       7             try:
       8                 return f(*args, **kw)
       9             finally:
      10                 lock.release()
      11         return new_function
      12     return wrap
      13 
      14 # Example usage:
      15 
      16 from threading import Lock
      17 my_lock = Lock()
      18 
      19 @synchronized(my_lock)
      20 def critical1(*args):
      21     # Interesting stuff goes here.
      22     pass
      23 
      24 @synchronized(my_lock)
      25 def critical2(*args):
      26     # Other interesting stuff goes here.
      27     pass
    

## Type Enforcement (accepts/returns)

Provides various degrees of type enforcement for function parameters and return values. 

    
    
       1 '''
       2 One of three degrees of enforcement may be specified by passing
       3 the 'debug' keyword argument to the decorator:
       4     0 -- NONE:   No type-checking. Decorators disabled.
       5  #!python
       6 -- MEDIUM: Print warning message to stderr. (Default)
       7     2 -- STRONG: Raise TypeError with message.
       8 If 'debug' is not passed to the decorator, the default level is used.
       9 
      10 Example usage:
      11     >>> NONE, MEDIUM, STRONG = 0, 1, 2
      12     >>>
      13     >>> @accepts(int, int, int)
      14     ... @returns(float)
      15     ... def average(x, y, z):
      16     ...     return (x + y + z) / 2
      17     ...
      18     >>> average(5.5, 10, 15.0)
      19     TypeWarning:  'average' method accepts (int, int, int), but was given
      20     (float, int, float)
      21     15.25
      22     >>> average(5, 10, 15)
      23     TypeWarning:  'average' method returns (float), but result is (int)
      24     15
      25 
      26 Needed to cast params as floats in function def (or simply divide by 2.0).
      27 
      28     >>> TYPE_CHECK = STRONG
      29     >>> @accepts(int, debug=TYPE_CHECK)
      30     ... @returns(int, debug=TYPE_CHECK)
      31     ... def fib(n):
      32     ...     if n in (0, 1): return n
      33     ...     return fib(n-1) + fib(n-2)
      34     ...
      35     >>> fib(5.3)
      36     Traceback (most recent call last):
      37       ...
      38     TypeError: 'fib' method accepts (int), but was given (float)
      39 
      40 '''
      41 import sys
      42 
      43 def accepts(*types, **kw):
      44     '''Function decorator. Checks decorated function's arguments are
      45     of the expected types.
      46 
      47     Parameters:
      48     types -- The expected types of the inputs to the decorated function.
      49              Must specify type for each parameter.
      50     kw    -- Optional specification of 'debug' level (this is the only valid
      51              keyword argument, no other should be given).
      52              debug = ( 0 | 1 | 2 )
      53 
      54     '''
      55     if not kw:
      56         # default level: MEDIUM
      57         debug = 1
      58     else:
      59         debug = kw['debug']
      60     try:
      61         def decorator(f):
      62             def newf(*args):
      63                 if debug is 0:
      64                     return f(*args)
      65                 assert len(args) == len(types)
      66                 argtypes = tuple(map(type, args))
      67                 if argtypes != types:
      68                     msg = info(f.__name__, types, argtypes, 0)
      69                     if debug is 1:
      70                         print >> sys.stderr, 'TypeWarning: ', msg
      71                     elif debug is 2:
      72                         raise TypeError, msg
      73                 return f(*args)
      74             newf.__name__ = f.__name__
      75             return newf
      76         return decorator
      77     except KeyError, key:
      78         raise KeyError, key + "is not a valid keyword argument"
      79     except TypeError, msg:
      80         raise TypeError, msg
      81 
      82 
      83 def returns(ret_type, **kw):
      84     '''Function decorator. Checks decorated function's return value
      85     is of the expected type.
      86 
      87     Parameters:
      88     ret_type -- The expected type of the decorated function's return value.
      89                 Must specify type for each parameter.
      90     kw       -- Optional specification of 'debug' level (this is the only valid
      91                 keyword argument, no other should be given).
      92                 debug=(0 | 1 | 2)
      93     '''
      94     try:
      95         if not kw:
      96             # default level: MEDIUM
      97             debug = 1
      98         else:
      99             debug = kw['debug']
     100         def decorator(f):
     101             def newf(*args):
     102                 result = f(*args)
     103                 if debug is 0:
     104                     return result
     105                 res_type = type(result)
     106                 if res_type != ret_type:
     107                     msg = info(f.__name__, (ret_type,), (res_type,), 1)
     108                     if debug is 1:
     109                         print >> sys.stderr, 'TypeWarning: ', msg
     110                     elif debug is 2:
     111                         raise TypeError, msg
     112                 return result
     113             newf.__name__ = f.__name__
     114             return newf
     115         return decorator
     116     except KeyError, key:
     117         raise KeyError, key + "is not a valid keyword argument"
     118     except TypeError, msg:
     119         raise TypeError, msg
     120 
     121 def info(fname, expected, actual, flag):
     122     '''Convenience function returns nicely formatted error/warning msg.'''
     123     format = lambda types: ', '.join([str(t).split("'")[1] for t in types])
     124     expected, actual = format(expected), format(actual)
     125     msg = "'{}' method ".format( fname )\
     126           + ("accepts", "returns")[flag] + " ({}), but ".format(expected)\
     127           + ("was given", "result is")[flag] + " ({})".format(actual)
     128     return msg
    

## CGI method wrapper

Handles HTML boilerplate at top and bottom of pages returned from CGI methods. Works with the cgi module. Now your request handlers can just output the interesting HTML, and let the decorator deal with all the top and bottom clutter. 

(Note: the exception handler eats all exceptions, which in CGI is no big loss, since the program runs in its separate subprocess. At least here, the exception contents will be written to the output page.) 

    
    
       1 class CGImethod(object):
       2     def __init__(self, title):
       3         self.title = title
       4 
       5     def __call__(self, fn):
       6         def wrapped_fn(*args):
       7             print "Content-Type: text/html\n\n"
       8             print "<HTML>"
       9             print "<HEAD><TITLE>{}</TITLE></HEAD>".format(self.title)
      10             print "<BODY>"
      11             try:
      12                 fn(*args)
      13             except Exception, e:
      14                 print
      15                 print e
      16             print
      17             print "</BODY></HTML>"
      18 
      19         return wrapped_fn
      20 
      21 @CGImethod("Hello with Decorator")
      22 def say_hello():
      23     print '<h1>Hello from CGI-Land</h1>'
    

## State Machine Implementaion

A much improved version of decorators for implementing state machines, too long to show here, is at [State Machine via Decorators](/moin/State%20Machine%20via%20Decorators)

This example uses Decorators to facilitate the implementation of a state machine in Python. Decorators are used to specify which methods are the event handlers for the class. In this example, actions are associated with the transitions, but it is possible with a little consideration to associate actions with states instead. 

The example defines a class, [MyMachine](/moin/MyMachine) that is a state machine. Multiple instances of the class may be instantiated with each maintaining its own state. A class also may have multiple states. Here I've used gstate and tstate. 

The code in the imported statedefn file gets a bit hairy, but you may not need to delve into it for your application. 

    
    
       1 # State Machine example Program
       2 
       3 from statedefn import *
       4 
       5 class MyMachine(object):
       6 
       7     # Create Statedefn object for each state you need to keep track of.
       8     # the name passed to the constructor becomes a StateVar member of the current class.
       9     # i.e. if my_obj is a MyMachine object, my_obj.gstate maintains the current gstate
      10     gstate = StateTable("gstate")
      11     tstate = StateTable("turtle")
      12 
      13     def __init__(self, name):
      14         # must call init method of class's StateTable object. to initialize state variable
      15         self.gstate.initialize(self)
      16         self.tstate.initialize(self)
      17         self.mname = name
      18         self.a_count = 0
      19         self.b_count = 0
      20         self.c_count = 0
      21 
      22     # Decorate the Event Handler virtual functions -note gstate parameter
      23     @event_handler(gstate)
      24     def event_a(self): pass
      25 
      26     @event_handler(gstate)
      27     def event_b(self): pass
      28 
      29     @event_handler(gstate)
      30     def event_c(self, val): pass
      31 
      32     @event_handler(tstate)
      33     def toggle(self): pass
      34 
      35 
      36     # define methods to handle events.
      37     def _event_a_hdlr1(self):
      38         print "State 1, event A"
      39         self.a_count += 1
      40     def _event_b_hdlr1(self):
      41         print "State 1, event B"
      42         self.b_count += 1
      43     def _event_c_hdlr1(self, val):
      44         print "State 1, event C"
      45         self.c_count += 3*val
      46 
      47     def _event_a_hdlr2(self):
      48         print "State 2, event A"
      49         self.a_count += 10
      50         # here we brute force the tstate to on, leave & enter functions called if state changes.
      51         # turtle is object's state variable for tstate, comes from constructor argument
      52         self.turtle.set_state(self, self._t_on)
      53     def _event_b_hdlr2(self):
      54         print "State 2, event B"
      55         self.b_count += 10
      56     def _event_c_hdlr2(self, val):
      57         print "State 2, event C"
      58         self.c_count += 2*val
      59 
      60     def _event_a_hdlr3(self):
      61         self.a_count += 100
      62         print "State 3, event A"
      63     def _event_b_hdlr3(self):
      64         print "State 3, event B"
      65         self.b_count += 100
      66         # we decide here we want to go to state 2, overrrides spec in state table below.
      67         # transition to next_state is made after the method exits.
      68         self.gstate.next_state = self._state2
      69     def _event_c_hdlr3(self, val):
      70         print "State 3, event C"
      71         self.c_count += 5*val
      72 
      73     # Associate the handlers with a state. The first argument is a list of methods.
      74     # One method for each event_handler decorated function of gstate. Order of methods
      75     # in the list correspond to order in which the Event Handlers were declared.
      76     # Second arg is the name of the state.  Third argument is to be come a list of the
      77     # next states.
      78     # The first state created becomes the initial state.
      79     _state1 = gstate.state("One",  (_event_a_hdlr1, _event_b_hdlr1, _event_c_hdlr1),
      80                                       ("Two", "Three", None))
      81     _state2 = gstate.state("Two",  (_event_a_hdlr2, _event_b_hdlr2, _event_c_hdlr2),
      82                                      ("Three",        None,          "One"))
      83     _state3 = gstate.state("Three",(_event_a_hdlr3, _event_b_hdlr3, _event_c_hdlr3),
      84                                  (None,         "One",         "Two"))
      85 
      86 
      87     # Declare a function that will be called when entering a new gstate.
      88     # Can also declare a leave function using @on_leave_function(gstate)
      89     @on_enter_function(gstate)
      90     def _enter_gstate(self):
      91         print "entering state ", self.gstate.name() , "of ", self.mname
      92     @on_leave_function(tstate)
      93     def _leave_tstate(self):
      94         print "leaving state ", self.turtle.name() , "of ", self.mname
      95 
      96 
      97     def _toggle_on(self):
      98         print "Toggle On"
      99 
     100     def _toggle_off(self):
     101         print "Toggle Off"
     102 
     103     _t_off = tstate.state("Off", [_toggle_on],
     104                          ["On"])
     105     _t_on =  tstate.state("On", [_toggle_off],
     106                           ["Off"])
     107 
     108 
     109 def main():
     110     big_machine = MyMachine("big")
     111     lil_machine = MyMachine("lil")
     112 
     113     big_machine.event_a()
     114     lil_machine.event_a()
     115     big_machine.event_a()
     116     lil_machine.event_a()
     117     big_machine.event_b()
     118     lil_machine.event_b()
     119     big_machine.event_c(4)
     120     lil_machine.event_c(2)
     121     big_machine.event_c(1)
     122     lil_machine.event_c(3)
     123     big_machine.event_b()
     124     lil_machine.event_b()
     125     big_machine.event_a()
     126     lil_machine.event_a()
     127     big_machine.event_a()
     128 
     129     big_machine.toggle()
     130     big_machine.toggle()
     131     big_machine.toggle()
     132 
     133     lil_machine.event_a()
     134     big_machine.event_b()
     135     lil_machine.event_b()
     136     big_machine.event_c(3)
     137     big_machine.event_a()
     138     lil_machine.event_c(2)
     139     lil_machine.event_a()
     140     big_machine.event_b()
     141     lil_machine.event_b()
     142     big_machine.event_c(7)
     143     lil_machine.event_c(1)
     144 
     145     print "Event A count ", big_machine.a_count
     146     print "Event B count ", big_machine.b_count
     147     print "Event C count ", big_machine.c_count
     148     print "LilMachine C count ", lil_machine.c_count
     149 
     150 main()
    

And now the imported statedefn.py 

    
    
       1 #
       2 # Support for State Machines.  ref - Design Patterns by GoF
       3 #  Many of the methods in these classes get called behind the scenes.
       4 #
       5 #  Notable exceptions are methods of the StateVar class.
       6 #
       7 #  See example programs for how this module is intended to be used.
       8 #
       9 class StateMachineError(Exception):
      10     def __init__(self, args = None):
      11        self.args = args
      12 
      13 class StateVar(object):
      14     def __init__(self, initial_state):
      15         self._current_state = initial_state
      16         self.next_state = initial_state            # publicly settable in an event handling routine.
      17 
      18     def set_state(self, owner, new_state):
      19         '''
      20         Forces a state change to new_state
      21         '''
      22         self.next_state = new_state
      23         self.__to_next_state(owner)
      24 
      25     def __to_next_state(self, owner):
      26         '''
      27         The low-level state change function which calls leave state & enter state functions as
      28         needed.
      29 
      30         LeaveState and EnterState functions are called as needed when state transitions.
      31         '''
      32         if self.next_state is not self._current_state:
      33             if hasattr(self._current_state, "leave"):
      34                 self._current_state.leave(owner)
      35             elif hasattr(self, "leave"):
      36                 self.leave(owner)
      37             self._current_state =  self.next_state
      38             if hasattr(self._current_state, "enter"):
      39                 self._current_state.enter(owner)
      40             elif hasattr(self, "enter"):
      41                 self.enter(owner)
      42 
      43     def __fctn(self, func_name):
      44         '''
      45         Returns the owning class's method for handling an event for the current state.
      46         This method not for public consumption.
      47         '''
      48         vf = self._current_state.get_fe(func_name)
      49         return vf
      50 
      51     def name(self):
      52         '''
      53         Returns the current state name.
      54         '''
      55         return self._current_state.name
      56 
      57 class STState(object):
      58     def __init__(self, state_name):
      59         self.name = state_name
      60         self.fctn_dict = {}
      61 
      62     def set_events(self, event_list, event_hdlr_list, next_states):
      63         dictionary = self.fctn_dict
      64         if not next_states:
      65             def set_row(event, method):
      66                 dictionary[event] = [method, None]
      67             map(set_row, event_list, event_hdlr_list)
      68         else:
      69             def set_row2(event, method, next_state):
      70                 dictionary[event] = [method, next_state]
      71             map(set_row2, event_list, event_hdlr_list, next_states)
      72         self.fctn_dict = dictionary
      73 
      74     def get_fe(self, fctn_name):
      75         return self.fctn_dict[fctn_name]
      76 
      77     def map_next_states(self, state_dict):
      78         ''' Changes second dict value from name of state to actual state.'''
      79         for de in self.fctn_dict.values():
      80             next_state_name = de[1]
      81             if next_state_name:
      82                 if next_state_name in state_dict:
      83                     de[1] = state_dict[next_state_name]
      84                 else:
      85                     raise StateMachineError('Invalid Name for next state: {}'.format(next_state_name))
      86 
      87 
      88 class StateTable(object):
      89     '''
      90     Magical class to define a state machine, with the help of several decorator functions
      91     which follow.
      92     '''
      93     def __init__(self, declname):
      94         self.machine_var = declname
      95         self._initial_state = None
      96         self._state_list = {}
      97         self._event_list = []
      98         self.need_initialize = 1
      99 
     100     def initialize(self, parent):
     101         '''
     102         Initializes the parent class's state variable for this StateTable class.
     103         Must call this method in the parent' object's __init__ method.  You can have
     104         Multiple state machines within a parent class. Call this method for each
     105         '''
     106         statevar= StateVar(self._initial_state)
     107         setattr(parent, self.machine_var, statevar)
     108         if hasattr(self, "enter"):
     109             statevar.enter = self.enter
     110         if hasattr(self, "leave"):
     111             statevar.leave = self.leave
     112         #Magic happens here - in the 'next state' table, translate names into state objects.
     113         if  self.need_initialize:
     114             for xstate in list(self._state_list.values()):
     115                 xstate.map_next_states(self._state_list)
     116             self.need_initialize = 0
     117 
     118     def def_state(self, event_hdlr_list, name):
     119         '''
     120         This is used to define a state. the event handler list is a list of functions that
     121         are called for corresponding events. name is the name of the state.
     122         '''
     123         state_table_row = STState(name)
     124         if len(event_hdlr_list) != len(self._event_list):
     125             raise StateMachineError('Mismatch between number of event handlers and the methods specified for the state.')
     126 
     127         state_table_row.set_events(self._event_list, event_hdlr_list, None)
     128 
     129         if self._initial_state is None:
     130             self._initial_state = state_table_row
     131         self._state_list[name] = state_table_row
     132         return state_table_row
     133 
     134     def state(self, name, event_hdlr_list, next_states):
     135         state_table_row = STState(name)
     136         if len(event_hdlr_list) != len(self._event_list):
     137             raise StateMachineError('Mismatch between number of event handlers and the methods specified for the state.')
     138         if next_states is not None and len(next_states) != len(self._event_list):
     139             raise StateMachineError('Mismatch between number of event handlers and the next states specified for the state.')
     140 
     141         state_table_row.set_events(self._event_list, event_hdlr_list, next_states)
     142 
     143         if self._initial_state is None:
     144             self._initial_state = state_table_row
     145         self._state_list[name] = state_table_row
     146         return state_table_row
     147 
     148     def __add_ev_hdlr(self, func_name):
     149         '''
     150         Informs the class of an event handler to be added. We just need the name here. The
     151         function name will later be associated with one of the functions in a list when a state is defined.
     152         '''
     153         self._event_list.append(func_name)
     154 
     155 # Decorator functions ...
     156 def event_handler(state_class):
     157     '''
     158     Declare a method that handles a type of event.
     159     '''
     160     def wrapper(func):
     161         state_class._StateTable__add_ev_hdlr(func.__name__)
     162         def obj_call(self, *args, **keywords):
     163             state_var = getattr(self, state_class.machine_var)
     164             funky, next_state = state_var._StateVar__fctn(func.__name__)
     165             if next_state is not None:
     166                 state_var.next_state = next_state
     167             rv = funky(self, *args, **keywords)
     168             state_var._StateVar__to_next_state(self)
     169             return rv
     170         return obj_call
     171     return wrapper
     172 
     173 def on_enter_function(state_class):
     174     '''
     175     Declare that this method should be called whenever a new state is entered.
     176     '''
     177     def wrapper(func):
     178         state_class.enter = func
     179         return func
     180     return wrapper
     181 
     182 def on_leave_function(state_class):
     183     '''
     184     Declares that this method should be called whenever leaving a state.
     185     '''
     186     def wrapper(func):
     187         state_class.leave = func
     188         return func
     189     return wrapper
    

## C++/Java-keyword-like function decorators

@abstractMethod, @deprecatedMethod, @privateMethod, @protectedMethod, @raises, @parameterTypes, @returnType 

The annotations provide run-time type checking and an alternative way to document code. 

The code and documentation are long, so I offer a link: <http://fightingquaker.com/pyanno/>

## Different Decorator Forms

There are operational differences between: 

  * Decorator with no arguments 
  * Decorator with arguments 
  * Decorator with wrapped class instance awareness 

This example demonstrates the operational differences between the three using a skit taken from Episode 22: Bruces. 

    
    
       1 from sys import stdout,stderr
       2 from pdb import set_trace as bp
       3 
       4 class DecoTrace(object):
       5     '''
       6     Decorator class with no arguments
       7 
       8     This can only be used for functions or methods where the instance
       9     is not necessary
      10 
      11     '''
      12 
      13     def __init__(self, f):
      14         self.f = f
      15 
      16     def _showargs(self, *fargs, **kw):
      17         print >> stderr, 'T: enter {} with args={}, kw={}'.format(self.f.__name__, str(fargs), str(kw))
      18 
      19     def _aftercall(self, status):
      20         print >> stderr, 'T: exit {} with status={}'.format(self.f.__name__, str(status))
      21 
      22     def __call__(self, *fargs, **kw):
      23         '''Pass *just* function arguments to wrapped function.'''
      24         self._showargs(*fargs, **kw)
      25         ret=self.f(*fargs, **kw)
      26         self._aftercall(ret)
      27         return ret
      28 
      29     def __repr__(self):
      30         return self.f.func_name
      31 
      32 
      33 class DecoTraceWithArgs(object):
      34     '''decorator class with ARGUMENTS
      35 
      36        This can be used for unbounded functions and methods.  If this wraps a
      37        class instance, then extract it and pass to the wrapped method as the
      38        first arg.
      39     '''
      40 
      41     def __init__(self, *dec_args, **dec_kw):
      42         '''The decorator arguments are passed here.  Save them for runtime.'''
      43         self.dec_args = dec_args
      44         self.dec_kw = dec_kw
      45 
      46         self.label = dec_kw.get('label', 'T')
      47         self.fid = dec_kw.get('stream', stderr)
      48 
      49     def _showargs(self, *fargs, **kw):
      50 
      51         print >> self.fid, \
      52               '{}: enter {} with args={}, kw={}'.format(self.label, self.f.__name__, str(fargs), str(kw))
      53         print >> self.fid, \
      54               '{}:   passing decorator args={}, kw={}'.format(self.label, str(self.dec_args), str(self.dec_kw))
      55 
      56     def _aftercall(self, status):
      57         print >> self.fid, '{}: exit {} with status={}'.format(self.label, self.f.__name__, str(status))
      58     def _showinstance(self, instance):
      59         print >> self.fid, '{}: instance={}'.format(self.label, instance)
      60 
      61     def __call__(self, f):
      62         def wrapper(*fargs, **kw):
      63             '''
      64               Combine decorator arguments and function arguments and pass to wrapped
      65               class instance-aware function/method.
      66 
      67               Note: the first argument cannot be "self" because we get a parse error
      68               "takes at least 1 argument" unless the instance is actually included in
      69               the argument list, which is redundant.  If this wraps a class instance,
      70               the "self" will be the first argument.
      71             '''
      72 
      73             self._showargs(*fargs, **kw)
      74 
      75             # merge decorator keywords into the kw argument list
      76             kw.update(self.dec_kw)
      77 
      78             # Does this wrap a class instance?
      79             if fargs and getattr(fargs[0], '__class__', None):
      80 
      81                 # pull out the instance and combine function and
      82                 # decorator args
      83                 instance, fargs = fargs[0], fargs[1:]+self.dec_args
      84                 self._showinstance(instance)
      85 
      86                 # call the method
      87                 ret=f(instance, *fargs, **kw)
      88             else:
      89                 # just send in the give args and kw
      90                 ret=f(*(fargs + self.dec_args), **kw)
      91 
      92             self._aftercall(ret)
      93             return ret
      94 
      95         # Save wrapped function reference
      96         self.f = f
      97         wrapper.__name__ = f.__name__
      98         wrapper.__dict__.update(f.__dict__)
      99         wrapper.__doc__ = f.__doc__
     100         return wrapper
     101 
     102 
     103 @DecoTrace
     104 def FirstBruce(*fargs, **kwargs):
     105     'Simple function using simple decorator.'
     106     if fargs and fargs[0]:
     107         print fargs[0]
     108 
     109 @DecoTraceWithArgs(name="Second Bruce", standardline="G'day, Bruce!")
     110 def SecondBruce(*fargs, **kwargs):
     111     'Simple function using decorator with arguments.'
     112     print '{}:'.format(kwargs.get('name', 'Unknown Bruce'))
     113 
     114     if fargs and fargs[0]:
     115         print fargs[0]
     116     else:
     117         print kwargs.get('standardline', None)
     118 
     119 class Bruce(object):
     120     'Simple class.'
     121 
     122     def __init__(self, id):
     123         self.id = id
     124 
     125     def __str__(self):
     126         return self.id
     127 
     128     def __repr__(self):
     129         return 'Bruce'
     130 
     131     @DecoTraceWithArgs(label="Trace a class", standardline="How are yer Bruce?", stream=stdout)
     132     def talk(self, *fargs, **kwargs):
     133         'Simple function using decorator with arguments.'
     134 
     135         print '{}:'.format(self)
     136         if fargs and fargs[0]:
     137             print fargs[0]
     138         else:
     139             print kwargs.get('standardline', None)
     140 
     141 ThirdBruce = Bruce('Third Bruce')
     142 
     143 SecondBruce()
     144 FirstBruce("First Bruce: Oh, Hello Bruce!")
     145 ThirdBruce.talk()
     146 FirstBruce("First Bruce: Bit crook, Bruce.")
     147 SecondBruce("Where's Bruce?")
     148 FirstBruce("First Bruce: He's not here, Bruce")
     149 ThirdBruce.talk("Blimey, s'hot in here, Bruce.")
     150 FirstBruce("First Bruce: S'hot enough to boil a monkey's bum!")
     151 SecondBruce("That's a strange expression, Bruce.")
     152 FirstBruce("First Bruce: Well Bruce, I heard the Prime Minister use it. S'hot enough to boil a monkey's bum in 'ere, your Majesty,' he said and she smiled quietly to herself.")
     153 ThirdBruce.talk("She's a good Sheila, Bruce and not at all stuck up.")
    

## Unimplemented function replacement

Allows you to test unimplemented code in a development environment by specifying a default argument as an argument to the decorator (or you can leave it off to specify None to be returned. 

    
    
       1 # Annotation wrapper annotation method
       2 def unimplemented(defaultval):
       3     if(type(defaultval) == type(unimplemented)):
       4         return lambda: None
       5     else:
       6         # Actual annotation
       7         def unimp_wrapper(func):
       8             # What we replace the function with
       9             def wrapper(*arg):
      10                 return defaultval
      11             return wrapper
      12         return unimp_wrapper
    

## Redirects stdout printing to python standard logging.

    
    
       1 class LogPrinter:
       2     '''LogPrinter class which serves to emulates a file object and logs
       3        whatever it gets sent to a Logger object at the INFO level.'''
       4     def __init__(self):
       5         '''Grabs the specific logger to use for logprinting.'''
       6         self.ilogger = logging.getLogger('logprinter')
       7         il = self.ilogger
       8         logging.basicConfig()
       9         il.setLevel(logging.INFO)
      10 
      11     def write(self, text):
      12         '''Logs written output to a specific logger'''
      13         self.ilogger.info(text)
      14 
      15 def logprintinfo(func):
      16     '''Wraps a method so that any calls made to print get logged instead'''
      17     def pwrapper(*arg, **kwargs):
      18         stdobak = sys.stdout
      19         lpinstance = LogPrinter()
      20         sys.stdout = lpinstance
      21         try:
      22             return func(*arg, **kwargs)
      23         finally:
      24             sys.stdout = stdobak
      25     return pwrapper
    

## Access control

This example prevents users from getting access to places where they are not authorised to go 

    
    
       1 class LoginCheck:
       2     '''
       3     This class checks whether a user
       4     has logged in properly via
       5     the global "check_function". If so,
       6     the requested routine is called.
       7     Otherwise, an alternative page is
       8     displayed via the global "alt_function"
       9     '''
      10     def __init__(self, f):
      11         self._f = f
      12 
      13     def __call__(self, *args):
      14         Status = check_function()
      15         if Status is 1:
      16             return self._f(*args)
      17         else:
      18             return alt_function()
      19 
      20 def check_function():
      21     return test
      22 
      23 def alt_function():
      24     return 'Sorry - this is the forced behaviour'
      25 
      26 @LoginCheck
      27 def display_members_page():
      28     print 'This is the members page'
    

Example: 

    
    
       1 test = 0
       2 DisplayMembersPage()
       3 # Displays "Sorry - this is the forced behaviour"
       4 
       5 test = 1
       6 DisplayMembersPage()
       7 # Displays "This is the members page"
    

## Events rising and handling

Please see the code and examples here: <http://pypi.python.org/pypi/Decovent>

## Singleton

    
    
       1 import functools
       2 
       3 def singleton(cls):
       4     ''' Use class as singleton. '''
       5 
       6     cls.__new_original__ = cls.__new__
       7 
       8     @functools.wraps(cls.__new__)
       9     def singleton_new(cls, *args, **kw):
      10         it =  cls.__dict__.get('__it__')
      11         if it is not None:
      12             return it
      13 
      14         cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
      15         it.__init_original__(*args, **kw)
      16         return it
      17 
      18     cls.__new__ = singleton_new
      19     cls.__init_original__ = cls.__init__
      20     cls.__init__ = object.__init__
      21 
      22     return cls
      23 
      24 #
      25 # Sample use:
      26 #
      27 
      28 @singleton
      29 class Foo:
      30     def __new__(cls):
      31         cls.x = 10
      32         return object.__new__(cls)
      33 
      34     def __init__(self):
      35         assert self.x == 10
      36         self.x = 15
      37 
      38 assert Foo().x == 15
      39 Foo().x = 20
      40 assert Foo().x == 20
    

## The Sublime Singleton

    
    
       1 def singleton(cls):
       2     instance = cls()
       3     instance.__call__ = lambda: instance
       4     return instance
       5 
       6 #
       7 # Sample use
       8 #
       9 
      10 @singleton
      11 class Highlander:
      12     x = 100
      13     # Of course you can have any attributes or methods you like.
      14 
      15 Highlander() is Highlander() is Highlander #=> True
      16 id(Highlander()) == id(Highlander) #=> True
      17 Highlander().x == Highlander.x == 100 #=> True
      18 Highlander.x = 50
      19 Highlander().x == Highlander.x == 50 #=> True
    

## Asynchronous Call

    
    
       1 from Queue import Queue
       2 from threading import Thread
       3 
       4 class asynchronous(object):
       5     def __init__(self, func):
       6         self.func = func
       7 
       8         def threaded(*args, **kwargs):
       9             self.queue.put(self.func(*args, **kwargs))
      10 
      11         self.threaded = threaded
      12 
      13     def __call__(self, *args, **kwargs):
      14         return self.func(*args, **kwargs)
      15 
      16     def start(self, *args, **kwargs):
      17         self.queue = Queue()
      18         thread = Thread(target=self.threaded, args=args, kwargs=kwargs);
      19         thread.start();
      20         return asynchronous.Result(self.queue, thread)
      21 
      22     class NotYetDoneException(Exception):
      23         def __init__(self, message):
      24             self.message = message
      25 
      26     class Result(object):
      27         def __init__(self, queue, thread):
      28             self.queue = queue
      29             self.thread = thread
      30 
      31         def is_done(self):
      32             return not self.thread.is_alive()
      33 
      34         def get_result(self):
      35             if not self.is_done():
      36                 raise asynchronous.NotYetDoneException('the call has not yet completed its task')
      37 
      38             if not hasattr(self, 'result'):
      39                 self.result = self.queue.get()
      40 
      41             return self.result
      42 
      43 if __name__ == '__main__':
      44     # sample usage
      45     import time
      46 
      47     @asynchronous
      48     def long_process(num):
      49         time.sleep(10)
      50         return num * num
      51 
      52     result = long_process.start(12)
      53 
      54     for i in range(20):
      55         print i
      56         time.sleep(1)
      57 
      58         if result.is_done():
      59             print "result {0}".format(result.get_result())
      60 
      61 
      62     result2 = long_process.start(13)
      63 
      64     try:
      65         print "result2 {0}".format(result2.get_result())
      66 
      67     except asynchronous.NotYetDoneException as ex:
      68         print ex.message
    

## Class method decorator using instance

When decorating a class method, the decorator receives an function not yet bound to an instance. 

The decorator can't to do anything on the instance invocating it, unless it actually is a descriptor. 

    
    
       1 from functools import wraps
       2 
       3 def decorate(f):
       4     '''
       5     Class method decorator specific to the instance.
       6 
       7     It uses a descriptor to delay the definition of the
       8     method wrapper.
       9     '''
      10     class descript(object):
      11         def __init__(self, f):
      12             self.f = f
      13 
      14         def __get__(self, instance, klass):
      15             if instance is None:
      16                 # Class method was requested
      17                 return self.make_unbound(klass)
      18             return self.make_bound(instance)
      19 
      20         def make_unbound(self, klass):
      21             @wraps(self.f)
      22             def wrapper(*args, **kwargs):
      23                 '''This documentation will vanish :)'''
      24                 raise TypeError(
      25                     'unbound method {}() must be called with {} instance '
      26                     'as first argument (got nothing instead)'.format(
      27                         self.f.__name__,
      28                         klass.__name__)
      29                 )
      30             return wrapper
      31 
      32         def make_bound(self, instance):
      33             @wraps(self.f)
      34             def wrapper(*args, **kwargs):
      35                 '''This documentation will disapear :)'''
      36                 print "Called the decorated method {} of {}".format(self.f.__name__, instance)
      37                 return self.f(instance, *args, **kwargs)
      38             # This instance does not need the descriptor anymore,
      39             # let it find the wrapper directly next time:
      40             setattr(instance, self.f.__name__, wrapper)
      41             return wrapper
      42 
      43     return descript(f)
    

This implementation replaces the descriptor by the actual decorated function ASAP to avoid overhead, but you could keep it to do even more (counting calls, etc...) 

## Another Retrying Decorator

Here's another decorator for causing a function to be retried a certain number of times. This decorator is superior IMHO because it should work with any old function that raises an exception on failure. 

Features: 

  * Works with any function that signals failure by raising an exception (I.E. just about any function) 
  * Supports retry delay and backoff 
  * User can specify which exceptions are caught for retrying. E.g. networking code might be expected to raise [SocketError](/moin/SocketError) in the event of communications difficulties, while any other exception likely indicates a bug in the code. 
  * Hook for custom logging 

GIST: <https://gist.github.com/2570004>

    
    
       1 #
       2 # Copyright 2012 by Jeff Laughlin Consulting LLC
       3 #
       4 # Permission is hereby granted, free of charge, to any person obtaining a copy
       5 # of this software and associated documentation files (the "Software"), to deal
       6 # in the Software without restriction, including without limitation the rights
       7 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
       8 # copies of the Software, and to permit persons to whom the Software is
       9 # furnished to do so, subject to the following conditions:
      10 #
      11 # The above copyright notice and this permission notice shall be included in
      12 # all copies or substantial portions of the Software.
      13 #
      14 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
      15 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
      16 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
      17 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
      18 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
      19 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
      20 # SOFTWARE.
      21 
      22 
      23 import sys
      24 from time import sleep
      25 
      26 
      27 def example_exc_handler(tries_remaining, exception, delay):
      28     """Example exception handler; prints a warning to stderr.
      29 
      30     tries_remaining: The number of tries remaining.
      31     exception: The exception instance which was raised.
      32     """
      33     print >> sys.stderr, "Caught '%s', %d tries remaining, sleeping for %s seconds" % (exception, tries_remaining, delay)
      34 
      35 
      36 def retries(max_tries, delay=1, backoff=2, exceptions=(Exception,), hook=None):
      37     """Function decorator implementing retrying logic.
      38 
      39     delay: Sleep this many seconds * backoff * try number after failure
      40     backoff: Multiply delay by this factor after each failure
      41     exceptions: A tuple of exception classes; default (Exception,)
      42     hook: A function with the signature myhook(tries_remaining, exception);
      43           default None
      44 
      45     The decorator will call the function up to max_tries times if it raises
      46     an exception.
      47 
      48     By default it catches instances of the Exception class and subclasses.
      49     This will recover after all but the most fatal errors. You may specify a
      50     custom tuple of exception classes with the 'exceptions' argument; the
      51     function will only be retried if it raises one of the specified
      52     exceptions.
      53 
      54     Additionally you may specify a hook function which will be called prior
      55     to retrying with the number of remaining tries and the exception instance;
      56     see given example. This is primarily intended to give the opportunity to
      57     log the failure. Hook is not called after failure if no retries remain.
      58     """
      59     def dec(func):
      60         def f2(*args, **kwargs):
      61             mydelay = delay
      62             tries = range(max_tries)
      63             tries.reverse()
      64             for tries_remaining in tries:
      65                 try:
      66                    return func(*args, **kwargs)
      67                 except exceptions as e:
      68                     if tries_remaining > 0:
      69                         if hook is not None:
      70                             hook(tries_remaining, e, mydelay)
      71                         sleep(mydelay)
      72                         mydelay = mydelay * backoff
      73                     else:
      74                         raise
      75                 else:
      76                     break
      77         return f2
      78     return dec
    

## Logging decorator with specified logger (or default)

This decorator will log entry and exit points of your funtion using the specified logger or it defaults to your function's module name logger. 

In the current form it uses the logging.INFO level, but I can easily customized to use what ever level. Same for the entry and exit messages. 

    
    
       1 import functools, logging
       2 
       3 
       4 log = logging.getLogger(__name__)
       5 log.setLevel(logging.DEBUG)
       6 
       7 class log_with(object):
       8     '''Logging decorator that allows you to log with a
       9 specific logger.
      10 '''
      11     # Customize these messages
      12     ENTRY_MESSAGE = 'Entering {}'
      13     EXIT_MESSAGE = 'Exiting {}'
      14 
      15     def __init__(self, logger=None):
      16         self.logger = logger
      17 
      18     def __call__(self, func):
      19         '''Returns a wrapper that wraps func.
      20 The wrapper will log the entry and exit points of the function
      21 with logging.INFO level.
      22 '''
      23         # set logger if it was not set earlier
      24         if not self.logger:
      25             logging.basicConfig()
      26             self.logger = logging.getLogger(func.__module__)
      27 
      28         @functools.wraps(func)
      29         def wrapper(*args, **kwds):
      30             self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
      31             f_result = func(*args, **kwds)
      32             self.logger.info(self.EXIT_MESSAGE.format(func.__name__))   # logging level .info(). Set to .debug() if you want to
      33             return f_result
      34         return wrapper
    
    
    
       1 # Sample use and output:
       2 
       3 if __name__ == '__main__':
       4     logging.basicConfig()
       5     log = logging.getLogger('custom_log')
       6     log.setLevel(logging.DEBUG)
       7     log.info('ciao')
       8 
       9     @log_with(log)     # user specified logger
      10     def foo():
      11         print 'this is foo'
      12     foo()
      13 
      14     @log_with()        # using default logger
      15     def foo2():
      16         print 'this is foo2'
      17     foo2()
    
    
    
       1 # output
       2 >>> ================================ RESTART ================================
       3 >>>
       4 INFO:custom_log:ciao
       5 INFO:custom_log:Entering foo # uses the correct logger
       6 this is foo
       7 INFO:custom_log:Exiting foo
       8 INFO:__main__:Entering foo2  # uses the correct logger
       9 this is foo2
      10 INFO:__main__:Exiting foo2
    

## Lazy Thunkify

This decorator will cause any function to, instead of running its code, start a thread to run the code, returning a thunk (function with no args) that wait for the function's completion and returns the value (or raises the exception). 

Useful if you have Computation A that takes x seconds and then uses Computation B, which takes y seconds. Instead of x+y seconds you only need max(x,y) seconds. 

    
    
       1 import threading, sys, functools, traceback
       2 
       3 def lazy_thunkify(f):
       4     """Make a function immediately return a function of no args which, when called,
       5     waits for the result, which will start being processed in another thread."""
       6 
       7     @functools.wraps(f)
       8     def lazy_thunked(*args, **kwargs):
       9         wait_event = threading.Event()
      10 
      11         result = [None]
      12         exc = [False, None]
      13 
      14         def worker_func():
      15             try:
      16                 func_result = f(*args, **kwargs)
      17                 result[0] = func_result
      18             except Exception, e:
      19                 exc[0] = True
      20                 exc[1] = sys.exc_info()
      21                 print "Lazy thunk has thrown an exception (will be raised on thunk()):\n%s" % (
      22                     traceback.format_exc())
      23             finally:
      24                 wait_event.set()
      25 
      26         def thunk():
      27             wait_event.wait()
      28             if exc[0]:
      29                 raise exc[1][0], exc[1][1], exc[1][2]
      30 
      31             return result[0]
      32 
      33         threading.Thread(target=worker_func).start()
      34 
      35         return thunk
      36 
      37     return lazy_thunked
    

Example: 

    
    
       1 @lazy_thunkify
       2 def slow_double(i):
       3     print "Multiplying..."
       4     time.sleep(5)
       5     print "Done multiplying!"
       6     return i*2
       7 
       8 
       9 def maybe_multiply(x):
      10     double_thunk = slow_double(x)
      11     print "Thinking..."
      12     time.sleep(3)
      13     time.sleep(3)
      14     time.sleep(1)
      15     if x == 3:
      16         print "Using it!"
      17         res = double_thunk()
      18     else:
      19         print "Not using it."
      20         res = None
      21     return res
      22 
      23 #both take 7 seconds
      24 maybe_multiply(10)
      25 maybe_multiply(3)
    

## Aggregative decorators for generator functions

This could be a whole family of decorators. The aim is applying an aggregation function to the iterated outcome of a generator-functions. 

Two interesting aggregators could be sum and average: 

    
    
       1 import functools as ft import operator as op
       2 
       3 def summed(f):
       4   return lambda *xs : sum(f(*xs))
       5 
       6 def averaged(f):
       7   def aux(acc, x):
       8     return (acc[0] + x, acc[1] + 1)
       9 
      10   def out(*xs):
      11     s, n = ft.reduce(aux, f(*xs), (0, 0))
      12     return s / n if n > 0 else 0
      13 
      14   return out
    

Examples for the two proposed decorators: 

    
    
       1 @averaged
       2 def producer2():
       3     yield 10
       4     yield 5
       5     yield 2.5
       6     yield 7.5
       7 
       8 assert producer2() == (10 + 5 + 2.5 + 7.5) / 4
       9 
      10 @summed
      11 def producer1():
      12     yield 10
      13     yield 5
      14     yield 2.5
      15     yield 7.5
      16 
      17 assert producer1() == (10 + 5 + 2.5 + 7.5)
    

## Function Timeout

Ever had a function take forever in weird edge cases? In one case, a function was extracting URIs from a long string using regular expressions, and sometimes it was running into a bug in the Python regexp engine and would take minutes rather than milliseconds. The best solution was to install a timeout using an alarm signal and simply abort processing. This can conveniently be wrapped in a decorator: 

    
    
       1 import signal
       2 import functools
       3 
       4 class TimeoutError(Exception): pass
       5 
       6 def timeout(seconds, error_message = 'Function call timed out'):
       7     def decorated(func):
       8         def _handle_timeout(signum, frame):
       9             raise TimeoutError(error_message)
      10 
      11         def wrapper(*args, **kwargs):
      12             signal.signal(signal.SIGALRM, _handle_timeout)
      13             signal.alarm(seconds)
      14             try:
      15                 result = func(*args, **kwargs)
      16             finally:
      17                 signal.alarm(0)
      18             return result
      19 
      20         return functools.wraps(func)(wrapper)
      21 
      22     return decorated
    

Example: 

    
    
       1 import time
       2 
       3 @timeout(1, 'Function slow; aborted')
       4 def slow_function():
       5     time.sleep(5)
    

* * *

[CategoryDocumentation](/moin/CategoryDocumentation)

PythonDecoratorLibrary (last edited 2016-02-05 12:40:03 by [mohaned magdy](/moin/mohaned%20magdy))

  * [MoinMoin Powered](http://moinmo.in/)
  * [Python Powered](http://moinmo.in/Python)
  * [GPL licensed](http://moinmo.in/GPL)
  * [Valid HTML 4.01](http://validator.w3.org/check?uri=referer)

[Unable to edit the page? See the FrontPage for instructions.](/moin/FrontPage#use))
