from __future__ import print_function
# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/15

# https://pypi.python.org/pypi/ProxyTypes/0.9

import ui
from proxy import ObjectWrapper

class ButtonWrapper(ObjectWrapper):
	def __init__(self, obj):
		ObjectWrapper.__init__(self, obj)
	def msg(self, leader):
		print(leader + ': ' + self.name)
		
button = ButtonWrapper(ui.Button(name = 'Wrapped ui.Button'))

button.msg('Calling extra method')

