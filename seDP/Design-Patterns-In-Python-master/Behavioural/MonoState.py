#!/usr/bin/env python
# Written by: DGC

# python imports

#==============================================================================
class MonoState(object):
    __data = 5
    
    @property
    def data(self):
        return self.__class__.__data

    @data.setter
    def data(self, value):
        self.__class__.__data = value

#==============================================================================
class MonoState2(object):
    pass

def add_monostate_property(cls, name, initial_value):
    """
    Adds a property "name" to the class "cls" (should pass in a class object 
    not a class instance) with the value "initial_value".
    
    This property is a monostate property so all instances of the class will 
    have the same value property. You can think of it being a singleton 
    property, the class instances will be different but the property will 
    always be the same.

    This will add a variable __"name" to the class which is the internal 
    storage for the property.

    Example usage:
    class MonoState(object):
        pass
        
    add_monostate_property(MonoState, "data", 5)
    m = MonoState()
    # returns 5
    m.data
    """
    internal_name = "__" + name

    def getter(self):
        return getattr(self.__class__, internal_name)
    def setter(self, value):
        setattr(self.__class__, internal_name, value)
    def deleter(self):
        delattr(self.__class__, internal_name)
    prop = property(getter, setter, deleter, "monostate variable: " + name)
    # set the internal attribute
    setattr(cls, internal_name, initial_value)
    # set the accesser property
    setattr(cls, name, prop)

#==============================================================================
if (__name__ == "__main__"):
    print("Using a class:")
    class_1 = MonoState()
    print("First data:  " + str(class_1.data))
    class_1.data = 4
    class_2 = MonoState()
    print("Second data: " + str(class_2.data))
    print("First instance:  " + str(class_1))
    print("Second instance: " + str(class_2))
    print("These are not singletons, so these are different instances")

    print("")
    print("")

    print("Dynamically adding the property:")
    add_monostate_property(MonoState2, "data", 5)
    dynamic_1 = MonoState2()
    print("First data:  " + str(dynamic_1.data))
    dynamic_1.data = 4
    dynamic_2 = MonoState2()
    print("Second data: " + str(dynamic_2.data))
    print("First instance:  " + str(dynamic_1))
    print("Second instance: " + str(dynamic_2))
    print("These are not singletons, so these are different instances")
