#!/usr/bin/env python
# Written by: DGC

#==============================================================================
class ReverseIterator(object):
    """ 
    Iterates the object given to it in reverse so it shows the difference. 
    """

    def __init__(self, iterable_object):
        self.list = iterable_object
        # start at the end of the iterable_object
        self.index = len(iterable_object)

    def __iter__(self):
        # return an iterator
        return self

    def next(self):
        """ Return the list backwards so it's noticeably different."""
        if (self.index == 0):
            # the list is over, raise a stop index exception
            raise StopIteration
        self.index = self.index - 1
        return self.list[self.index]

#==============================================================================
class Days(object):

    def __init__(self):
        self.days = [
        "Monday",
        "Tuesday", 
        "Wednesday", 
        "Thursday",
        "Friday", 
        "Saturday", 
        "Sunday"
        ]

    def reverse_iter(self):
        return ReverseIterator(self.days)

#==============================================================================
if (__name__ == "__main__"):
    days = Days()
    for day in days.reverse_iter():
        print(day)
