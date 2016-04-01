import os, ui
import editor

class App(object):
    def __init__(self, bview, fn):
        self.bview = bview
        self.fn    = fn
        
        self.view = ui.View()
        self.view.name = os.path.split(fn)[-1]
        self.view.right_button_items = [
            ui.ButtonItem("Open in editor", None, self.openineditor)
        ]
        
        self.text = ui.TextView()
        self.text.flex = "WH"
        self.text.font = ("Courier", 18)
        self.text.text = open(self.fn).read()
        
        self.view.add_subview(self.text)
        self.view.present("fullscreen")
    
    def openineditor(self, sender):
        self.view.close()
        editor.open_file(self.fn)

