#!/usr/bin/env python
# Written by: DGC

# python imports
import math

#==============================================================================
class DataCache(object):

    def __init__(self):
        """ A class representing cachable data, starts invalid."""
        self.data = None

    def __call__(self):
        """ 
        When an instance is called it returns the stored data or None if no 
        data has been cached.
        e.g
        data = cached_data()
        """
        return self.data

    def __nonzero__(self):
        """ 
        Called on bool(instance) or if(instance) returns if there is data 
        cached.
        e.g
        if (not data):
            # set data
        """
        return self.data is not None
    
    def set(self, data):
        """ Sets the data. """
        self.data = data
        
    def reset(self):
        """ Returns the class to an invalid state. """
        self.data = None

#==============================================================================
class Line(object):
    
    def __init__(self, start, end):
        """ 
        This is a class representing a 2D line.
        Takes a start point and end point represented by two pairs.
        """
        self.start = start
        self.end = end
        self.length_data = DataCache()
        
    def length(self):
        if (not self.length_data):
            x_length = self.start[0] - self.end[0]
            y_length = self.start[1] - self.end[1]
            length = math.sqrt((x_length ** 2) + (y_length ** 2))
            self.length_data.set(length)
        else:
            print("Cached value used")
        return self.length_data()

#==============================================================================
if (__name__ == "__main__"):
    l = Line((0, 0), (1, 0))
    print(l.length())
    print(l.length())
    
