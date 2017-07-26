# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/27

# Wrappers also chain nicely, so you might have e.g. styles in a different inheritance hierarchy and extra functionality in other.

# The only thing that is not chained is subject, so it probably makes sense inherit from a common base class and include a method that does the chaining, as follows:
	
import ui
from proxy import ObjectWrapper

class ChainableWrapper(ObjectWrapper):
    def __init__(self, obj):
        ObjectWrapper.__init__(self, obj)
    # Follow the chain of __subject__'s, if needed
    def get_subject(self):
        subject = self.__subject__
        while isinstance(subject, ObjectWrapper):
            subject = subject.__subject__
        return subject

class DefaultStyle(ChainableWrapper):
    def __init__(self, obj):
        super(DefaultStyle, self).__init__(obj)
        self.background_color = '#fff7ee'
        self.tint_color = 'black'
    
class HighlightStyle(DefaultStyle):
    def __init__(self, obj):
        super(HighlightStyle, self).__init__(obj)
        self.tint_color = 'red'
        
class ToggleButton(ChainableWrapper):
    def __init__(self, obj):
        super(ToggleButton, self).__init__(obj)
    def extra_functionality(self):
        pass
        
button = ToggleButton(HighlightStyle(ui.Button()))
button.title = 'Styled button'
button.present()

# Get the wrapped ui.* instance
some_other_view.add_subview(button.get_subject())
