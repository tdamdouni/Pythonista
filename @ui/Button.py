# https://forum.omz-software.com/topic/2295/python-string-object-as-callable-method

# coding: utf-8

import ui, console

w, h = ui.get_screen_size()
buttons = 'Scan_View Show_View'.split()

class OCRApp(ui.View):
    def __init__(self):
        self.background_color = 'orange'
        self.present()
        for i, button in enumerate(buttons):
            self.add_subview(self.make_button(button.lower(), i))
        
    def scan_view_action(self, sender):
        console.hud_alert('scan')
        
    def show_view_action(self, sender):
        console.hud_alert('show')
    
    def make_button(self, name, i):
        button = ui.Button(title=name)
        button.action = getattr(self, name + '_action')
        button.center = w / 2, i * 60 + button.height * 2
        return button

OCRApp()