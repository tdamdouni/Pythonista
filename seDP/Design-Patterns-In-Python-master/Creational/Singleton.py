#!/usr/bin/env python
# Written by: DGC

import abc

#==============================================================================
class Singleton(object):
    """ A generic base class to derive any singleton class from. """
    __metaclass__ = abc.ABCMeta
    __instance = None

    def __new__(new_singleton, *arguments, **keyword_arguments):
        """Override the __new__ method so that it is a singleton."""
        if new_singleton.__instance is None:
            new_singleton.__instance = object.__new__(new_singleton)
            new_singleton.__instance.init(*arguments, **keyword_arguments)
        return new_singleton.__instance

    @abc.abstractmethod
    def init(self, *arguments, **keyword_arguments):
        """ 
        as __init__ will be called on every new instance of a base class of 
        Singleton we need a function for initialisation. This will only be 
        called once regardless of how many instances of Singleton are made.
        """
        raise

#==============================================================================
class GlobalState(Singleton):

    def init(self):
        self.value = 0
        print("init() called once")
        print("")

    def __init__(self):
        print("__init__() always called")
        print("")

class DerivedGlobalState(GlobalState):
    
    def __init__(self):
        print("derived made")
        super(DerivedGlobalState, self).__init__()

    def thing(self):
        print(self.value)

#==============================================================================
if (__name__ == "__main__"):
    d = DerivedGlobalState()
    print(type(d))
    d.thing()
    d.value = -20
    e = DerivedGlobalState()
    e.thing()
    f = DerivedGlobalState()
    f.thing()
    
    a = GlobalState()
    # value is default, 0
    print("Expecting 0, value = %i" %(a.value))
    print("")

    # set the value to 5
    a.value = 5

    # make a new object, the value will still be 5
    b = GlobalState()
    print("Expecting 5, value = %i" %(b.value))
    print("")
    print("Is a == b? " + str(a == b))
