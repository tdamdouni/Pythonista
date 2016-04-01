#!/usr/bin/env python
########################################################################.......
u"""filenav for Pythonista, version 2, by dgelessus.
This is the "full" version of filenav 2. It is designed to be run in
panel mode on an iPad, though it may also be usable on large iPhones in
landscape mode.

A more compact version usable on an iPhone or iPod touch can be found
under `slim.py`.
"""

from __future__ import division, print_function

import argparse # For runtime argument parsing
import console  # To hide the output panel
import sys      # For runtime arguments
import ui       # Guess why

from filenav import common
##assert reload(common) # Development/testing only

MODE = "panel"

class FullFilenavApp(common.FilenavApp):
    def __init__(self):
        self.root = ui.View()
        self.root.name = "filenav"
        self.root.flex = "WH"
        
        self.scroll = ui.ScrollView()
        self.scroll.shows_vertical_scroll_indicator = False
        self.scroll.flex = "WH"
        self.root.add_subview(self.scroll)
        self.scroll.bounds = self.root.bounds
        self.scroll.content_size = 0, self.scroll.height
        
        self.view_stack = []
        self.nav_stack = []
    
    def close(self):
        self.root.close()
        console.hide_output()
    
    def push_view(self, view):
        view.left_button_items = ui.ButtonItem(
            image=ui.Image.named("ionicons-close-24"),
            action=(lambda sender: self.pop_view()),
        ), # Needs to be a tuple
        self.view_stack.append(view)
        
        nav = ui.NavigationView(view)
        nav.width = view.width
        nav.height = self.scroll.height
        if len(self.nav_stack) > 0:
            nav.x = self.nav_stack[-1].x + self.nav_stack[-1].width
        else:
            nav.x = 0
        
        self.scroll.content_size = nav.x + nav.width, self.scroll.height
        
        # Automatically scroll to the newly pushed view if appropriate
        if (
            self.scroll.content_size[0] > self.scroll.width
            and self.scroll.content_offset[0] >= nav.x - self.scroll.width - 1
        ):
            self.scroll.content_offset = nav.x + nav.width - self.scroll.width, 0
        
        self.scroll.add_subview(nav)
        self.nav_stack.append(nav)
    
    def pop_view(self):
        view = self.view_stack.pop()
        nav = self.nav_stack.pop()
        self.scroll.remove_subview(nav)
        self.scroll.content_size = nav.x, self.scroll.height
        if len(self.view_stack) <= 0:
            self.close()
        return view

def main(args):
    global fnapp # Technically not necessary, but useful for testing
    
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(u"dir", type=unicode, nargs="?",
                    help=u"initial directory, defaults to favorites list")
    ns = ap.parse_args(args)
    
    fnapp = FullFilenavApp()
    fnapp.root.present(MODE, hide_title_bar=True)
    
    fnapp.push_view(fnapp.make_favs_list(common.full_path("./favorites.json")))
    
    if ns.dir:
        fnapp.push_view(fnapp.make_file_list(common.FileItem(ns.dir)))
    
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
