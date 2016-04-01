#!/usr/bin/env python
# Written by: DGC

import abc

#==============================================================================
class Shape(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    def area(self):
        """ 
        Returns the area of the shape calculated using the shape specific 
        implementation. 
        """
        assert self.calculator != None, "self.calculator not defined."
        return self.calculator(self)

#==============================================================================
class Rectangle(Shape):
    
    def __init__(self, x, y):
        self.calculator = rectangular_area_calculator
        self.x = x
        self.y = y

#==============================================================================
def rectangular_area_calculator(rectangle):
    return rectangle.x * rectangle.y
 
#==============================================================================
class Triangle(Shape):

    def __init__(self, base, height):
        self.calculator = triangular_area_calculator
        self.base = base
        self.height = height

#==============================================================================
def triangular_area_calculator(triangle):
    return 0.5 * triangle.base * triangle.height
       
#==============================================================================
if (__name__ == "__main__"):
    x = 4
    y = 5
    rect = Rectangle(x, y)
    print(str(x) + " x " + str(y) + " Rectangle area: " + str(rect.area()))
  
    base = 4
    height = 5
    tri = Triangle(base, height);
    print(
        "Base " +
        str(base) +
        ", Height " +
        str(height) + 
        " Triangle area: " +
        str(tri.area())
        )
