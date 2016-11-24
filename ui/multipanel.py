#!/usr/bin/env python
########################################################################.......
from __future__ import division, print_function

import sys
import ui

PLACEHOLDER_TEXT = "No Views Presented"

class Multipanel(object):
    # Class of the object stored in ui.multipanel
    def __init__(self):
        # Init
        self.views = []
        self.curview = None
        
        self.root = ui.View(name="Multipanel")
        
        self.close = ui.Button()
        self.close.name = "close"
        self.close.enabled = False
        self.close.image = ui.Image.named("ionicons-close-round-32")
        self.close.action = self.close_tapped
        self.root.add_subview(self.close)
        self.close.frame = self.root.width - 32, 0, 32, 32
        self.close.flex = "LB"
        
        self.tabs = ui.SegmentedControl()
        self.tabs.name = "tabs"
        self.tabs.enabled = False
        self.tabs.selected_index = -1
        self.tabs.segments = [PLACEHOLDER_TEXT]
        self.tabs.action = self.segment_changed
        self.root.add_subview(self.tabs)
        self.tabs.frame = 0, 0, self.root.width - self.close.width, self.tabs.height
        self.tabs.flex = "WB"
        
        self.placeholder = ui.View()
        self.placeholder.background_color = "lightgray"
        
        self.ph_label = ui.Label()
        self.ph_label.font = ("<system-bold>", 24)
        self.ph_label.text_color = "gray"
        self.ph_label.text = "No View Selected"
        self.placeholder.add_subview(self.ph_label)
        self.ph_label.size_to_fit()
        self.ph_label.center = self.placeholder.center
        self.ph_label.flex = "TBLR"
        
        self.update_view()
    
    def segment_changed(self, sender):
        # Action method for self.tabs
        self.update_view()
    
    def close_tapped(self, sender):
        # Action method for self.close
        self.pop_view()
    
    def update_view(self):
        # Update the currently visible view based on self.tabs.selected_index
        if self.curview is not None:
            self.root.remove_subview(self.curview)
        
        if self.tabs.selected_index >= 0:
            self.curview = self.views[self.tabs.selected_index]
        else:
            self.curview = self.placeholder
        
        self.root.add_subview(self.curview)
        self.curview.frame = (
            0,
            self.tabs.height,
            self.root.width,
            self.root.height - self.tabs.height,
        )
        self.curview.flex = "WH"
    
    def add_view(self, view):
        # Add a view to the multipanel
        self.views.append(view)
        
        if len(self.tabs.segments) == 1 and self.tabs.segments[0] == PLACEHOLDER_TEXT:
            self.tabs.segments = (view.name or "",)
        else:
            self.tabs.segments += (view.name or "",)
                
        if self.tabs.selected_index < 0:
            self.tabs.selected_index = len(self.tabs.segments) - 1
        
        self.tabs.enabled = self.close.enabled = True
        self.update_view()
    
    def pop_view(self, index=None):
        # Pop a view from the multipanel by index
        index = self.tabs.selected_index if index is None else index
        view = self.views.pop(index)
        
        if len(self.views) > 0 and self.tabs.selected_index > 0:
            self.tabs.selected_index -= 1
        
        if len(self.views) == 0:
            self.tabs.segments = [PLACEHOLDER_TEXT]
            self.tabs.enabled = self.close.enabled = False
        else:
            # I'd use pop if this wasn't a tuple...
            self.tabs.segments = self.tabs.segments[:index] + self.tabs.segments[index+1:]
        
        self.update_view()

def init():
    # Monkey-patch the ui module to use Multipanel
    try:
        ui.view_real_present
    except AttributeError:
        ui.view_real_present = ui.View.present
    
    def present(self, mode, **kwargs):
        if mode == "panel":
            ui.multipanel.add_view(self)
        else:
            ui.view_real_present(self, mode, **kwargs)
    
    instancemethod = type(Multipanel.add_view)
    # ui.View is too builtin for us mere mortals to change its methods.
    ##ui.View.present = instancemethod(present, None, ui.View)
    
    ui.multipanel = Multipanel()
    ui.view_real_present(ui.multipanel.root, "panel")

def main():
    # (Re-)Initialize Multipanel if not already present
    try:
        ui.view_real_present(ui.multipanel.root, "panel")
    except AttributeError:
        init()
    except ValueError:
        print("Multipanel appears to be already running.", file=sys.stderr)
        return

if __name__ == "__main__":
    # Testing
    try:
        del ui.multipanel
    except AttributeError:
        pass
    
    main()

