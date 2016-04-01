# coding: utf-8

# https://forum.omz-software.com/topic/2738/ui-gaussian-blur/2

# @omz

# Below is a little BlurView class I've written to wrap UIVisualEffectView in an easy-to-use ui.View subclass. For the style argument, you can pass 1 (extra light) 2 (light) or 3 (dark). You can also use this class in the UI editor. Simply add a custom view and set its class to BlurView. To set the style from the UI editor, you can put something like {'style': 2} in the "custom attributes" field

import ui
from objc_util import *

class BlurView (ui.View):
    def __init__(self, style=1, *args, **kwargs):
        ui.View.__init__(self, **kwargs)
        self._style = style
        self.effect_view = None
        self.setup_effect_view()
    
    @on_main_thread
    def setup_effect_view(self):
        if self.effect_view is not None:
            self.effect_view.removeFromSuperview()
        UIVisualEffectView = ObjCClass('UIVisualEffectView')
        UIBlurEffect = ObjCClass('UIBlurEffect')
        frame = (self.bounds[:2], self.bounds[2:])
        self.effect_view = UIVisualEffectView.alloc().initWithFrame_(frame).autorelease()
        effect = UIBlurEffect.effectWithStyle_(self._style)
        self.effect_view.effect = effect
        self.effect_view.setAutoresizingMask_(18)
        ObjCInstance(self).addSubview_(self.effect_view)
    
    @property
    def style(self):
        return self._style
    
    @style.setter
    def style(self, value):
        if value != self._style:
            self._style = value
            self.setup_effect_view()