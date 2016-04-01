# coding: utf-8

import ui

class MyView(ui.View):
    def __init__(self):
        w,h = ui.get_screen_size()
        self.ty = ui.Label()
        self.ty.text = 'Hello'
        self.ty.text_color = 'black'
        self.ty.font = ('<system>', 60)
        self.ty.frame = (0, 0, w, h*0.25)
        self.ty.bg_color = 'yellow'
        self.sv = ui.ScrollView()
        self.sv.width = w
        self.sv.height = h*0.25
        self.sv.content_size = (2*w, h*0.25)
        self.sv.add_subview(self.ty)
        self.add_subview(self.sv)
view = MyView()
view.present('fullscreen')
