# extend

# Introduction

This module defines Extender, a base class for classes that are intended to add data and functionality to an instance of some other class.

This is useful when you are working with third-party classes that you do not want to or cannot enhance through inheritance. As an example, the class was developed to be used with the iOS Pythonista ui classes, which are to a large extent wrappers around the underlying iOS UIKit Objective-C classes, and do not support inheritance.

Extender has been tested in Python 2.7 and 3.5. You can run the tests in your environment by running the `extend.py` on its own.

# Examples

Let's say we have third-party class, ui.Button, and want to expand its functionality, for example, to record the number of times it has been clicked. Extender allows us to do this in a way that is maximally 'like' subclassing.

    class CounterButton(Extender):
      
      def __init__(self):
        self.click_count = 0
        self.action = self.increase_count
        
      def increase_count(self, sender):
        self.click_count += 1
        self.title = 'Clicked: ' + str(self.click_count)

We can now create a counter button by wrapping the button constructor with the extender:

    button = CounterButton(Button(title = 'Click me'))
    
The thing to note here is that in the extender class definition, `self` refers to the wrapped `Button` instance. Thus you can use all the properties from that instance - in this example, setting the `action` method that is called when the button is clicked.

Another example presents a hierarchy of UI element formatting definitions, combined with the functionality to make the button remember the toggled state:

    class BaseFormatting(Extender):
      
      def __init__(self):
        self.background_color = 'teal'
        self.font = ('Arial Rounded MT Bold', 24)
      
    class ButtonFormatting(BaseFormatting):
      
      def __init__(self):
        BaseFormatting.__init__(self) # 1
        self.tint_color = 'white'
        self.border_width = 2
        self.border_color = 'darkgrey'
      
    class SelectedButtonFormatting(ButtonFormatting):
      
      def __init__(self):
        ButtonFormatting.__init__(self)
        self.background_color = 'maroon'
        
    class ToggleButton(Extender):
      
      def __init__(self):
        self.toggle = False
        self.action = self.toggle_button
        
      def toggle_button(self, sender):
        if self.toggle: ButtonFormatting(self) # 2
        else: SelectedButtonFormatting(self)
        self.toggle = self.toggle == False

The extenders are again wrapped around the `Button` instance:

    button = ToggleButton(ButtonFormatting(Button(title = 'Click me')))

Specific things to note:

1. When using inheritance, calling overloaded `__init__` or any other method requires an explicit call to the overloaded method - `super()` will not work.
2. We can apply an extender at any time, not just at target instance creation.

Full examples are available in the `pythonista-examples` directory.

If you like, you can also use multiple inheritance to create e.g. a single extender that combines all the button aspects you need:

    class FormattedToggleButton(ButtonFormatting, ToggleButton):
      pass
      
In case of conflicts in the attributes, regular multiple inheritance resolution order applies, i.e. the first parent class wins.

# Miscellaneous notes

I originally used proxies for this same purpose, but ditched them for the metaclass approach, because there is no runtime overhead and potential weirdness after the target instance has been extended.
