# coding: utf-8

# https://forum.omz-software.com/topic/2513/getting-the-parent-of-a-dynamically-method-as-a-function/21

import ui
#from proxy import ObjectWrapper

from peak.util.proxies import ObjectWrapper

class DefaultStyle(ObjectWrapper):
    def __init__(self, obj):
        ObjectWrapper.__init__(self, obj)
        self.background_color = '#fff7ee'
        self.tint_color = 'black'

class HighlightStyle(DefaultStyle):
    def __init__(self, obj):
        DefaultStyle.__init__(self, obj)
        self.tint_color = 'red'

button = HighlightStyle(ui.Button())
button.title = 'Styled button'
button.present()
