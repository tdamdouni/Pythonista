# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2738/ui-gaussian-blur/8

# Here's an extended version of BlurView that includes support for vibrancy effects. The main function shows a little demo

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
        UIVibrancyEffect = ObjCClass('UIVibrancyEffect')
        UIBlurEffect = ObjCClass('UIBlurEffect')
        UILabel = ObjCClass('UILabel')
        frame = (self.bounds[:2], self.bounds[2:])
        self.effect_view = UIVisualEffectView.alloc().initWithFrame_(frame).autorelease()
        effect = UIBlurEffect.effectWithStyle_(self._style)
        self.effect_view.effect = effect
        self.effect_view.setAutoresizingMask_(18)
        ObjCInstance(self).addSubview_(self.effect_view)
        vibrancy_effect = UIVibrancyEffect.effectForBlurEffect_(effect)
        self.vibrancy_view = UIVisualEffectView.alloc().initWithFrame_(frame).autorelease()
        self.vibrancy_view.effect = vibrancy_effect
        self.effect_view.contentView().addSubview_(self.vibrancy_view)
        
    @property
    def style(self):
        return self._style
    
    @style.setter
    def style(self, value):
        if value != self._style:
            self._style = value
            self.setup_effect_view()
    
    @on_main_thread
    def add_vibrant_label(self, label):
        self.vibrancy_view.contentView().addSubview_(ObjCInstance(label))

def main():
    image_view = ui.ImageView(frame=(0, 0, 320, 320))
    image_view.image = ui.Image.named('test:Mandrill')
    blur_view = BlurView(style=2, frame=image_view.bounds.inset(40, 40))
    image_view.add_subview(blur_view)
    label = ui.Label(frame=blur_view.bounds)
    label.text = 'Hello World'
    label.font = ('HelveticaNeue', 40)
    label.alignment = ui.ALIGN_CENTER
    blur_view.add_vibrant_label(label)
    image_view.present('sheet')

main()
