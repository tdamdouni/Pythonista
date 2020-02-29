# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/15

# Here is how I add functionality to built-in ui classes these days, using ProxyTypes.

from __future__ import print_function
import ui
from proxy import ObjectWrapper

class ButtonWrapper(ObjectWrapper):
    def __init__(self, obj):
        ObjectWrapper.__init__(self, obj)
    def msg(self, leader):
        print(leader + ': ' + self.name)
        
button = ButtonWrapper(ui.Button(name = 'Wrapped ui.Button'))

button.msg('Calling extra method')
