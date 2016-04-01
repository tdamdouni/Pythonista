#!/usr/bin/env python
# Written by: DGC

#==============================================================================
class Line(object):
    """ A non-directed line. """

    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def __eq__(self, line):
        """ Magic method to overide == operator. """
        # if the lines are equal then the two points must be the same, but not 
        # necessarily named the same i.e self.point_1 == line.point_2 and 
        # self.point_2 == line.point_1 means that the lines are equal.
        if (type(line) != Line):
            return False
        if (self.point_1 == line.point_1):
            # line numbering matches
            return self.point_2 == line.point_2
        elif (self.point_1 == line.point_2):
            # line numbering does not match
            return self.point_2 == line.point_1
        else:
            # self.point_1 is not the start or end of the other line, not equal
            return False

#==============================================================================
class Vector(object):
    """ A directional vector. """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, vector):
        """ Magic method to overide == operator. """
        if (type(vector) != Vector):
            return False
        return (self.x == vector.x) and (self.y == vector.y)

#------------------------------------------------------------------------------
# Factory functions
#------------------------------------------------------------------------------

class Factory(object):

    @classmethod
    def line_from_point_vector(self, point, vector):
        """ Returns the line from travelling vector from point. """
        new_point = (point[0] + vector.x, point[1] + vector.y)
        return Line(point, new_point)

    @classmethod
    def vector_from_line(self, line):
        """ 
        Returns the directional vector of the line. This is a vector v, such 
        that line.point_1 + v == line.point_2 
        """
        return Vector(
            line.point_2.x - line.point_1.x, 
            line.point_2.y - line.point_1.y
            )

#==============================================================================
if (__name__ == "__main__"):
    # make a line from (1, 1) to (1, 0), check that the line made from the 
    # point (1, 1) and the vector (0, -1) is the same line.
    constructor_line = Line((1, 1), (1, 0))
    vector = Vector(0, -1);
    factory_line = Factory.line_from_point_vector(
        (1, 1),
        vector
        )
    print(constructor_line == factory_line)
    
