#!/usr/bin/env python
# Written by: DGC

import abc

class Observer(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def update(self):
        raise

class ConcreteObserver(Observer):
    pass

if (__name__ == "__main__"):
    print("thing")
    conc = ConcreteObserver()
    
    
        


