#!/usr/bin/env python
# Written by: DGC

import copy

#==============================================================================
class Memento(object):

    def __init__(self, data):
        # make a deep copy of every variable in the given class
        for attribute in vars(data):
            # mechanism for using properties without knowing their names
            setattr(self, attribute, copy.deepcopy(getattr(data, attribute)))

#==============================================================================
class Undo(object):

    def __init__(self):
        # each instance keeps the latest saved copy so that there is only one 
        # copy of each in memory
        self.__last = None

    def save(self):
        self.__last = Memento(self)

    def undo(self):
        for attribute in vars(self):
            # mechanism for using properties without knowing their names
            setattr(self, attribute, getattr(self.__last, attribute))

#==============================================================================
class Data(Undo):

    def __init__(self):
        super(Data, self).__init__()
        self.numbers = []

#==============================================================================
if (__name__ == "__main__"):
    d = Data()
    repeats = 10
    # add a number to the list in data repeat times
    print("Adding.")
    for i in range(repeats):
        print("0" + str(i) + " times: " + str(d.numbers))
        d.save()
        d.numbers.append(i)
    print("10 times: " + str(d.numbers))
    d.save()
    print("")
    
    # now undo repeat times
    print("Using Undo.")
    for i in range(repeats):
        print("0" + str(i) + " times: " + str(d.numbers))
        d.undo()
    print("10 times: " + str(d.numbers))
