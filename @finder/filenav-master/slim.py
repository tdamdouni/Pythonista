#!/usr/bin/env python
########################################################################.......
u"""filenav for Pythonista, version 2, by dgelessus.
This is the "slim" version of filenav 2. It consists of a single
navigable table and is thus ideal for use on an iPhone or iPod touch, or
even on an iPad in popover mode.

A separate version intended for larger screens can be found under
`full.py`. It is designed to be run in panel mode on an iPad, though it
may also be usable on large iPhones in landscape mode.
"""

from __future__ import division, print_function

import argparse # For runtime argument parsing
import sys      # For runtime arguments
import ui       # Guess why

from filenav import common
##assert reload(common) # Development/testing only

MODE = "panel"
##MODE = "popover" # For testing on iPad

class SlimFilenavApp(common.FilenavApp):
    def push_view(self, view):
        return self.root.push_view(view)
    
    def pop_view(self):
        return self.root.pop_view()

def main(args):
    global fnapp # Technically not necessary, but useful for testing
    
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(u"dir", type=unicode, nargs="?",
                    help=u"initial directory, defaults to favorites list")
    ns = ap.parse_args(args)
    
    fnapp = SlimFilenavApp()
    
    lst = fnapp.make_favs_list(common.full_path("./favorites.json"))
    lst.left_button_items = (
        ui.ButtonItem(
            image=ui.Image.named("ionicons-close-24"),
            action=(lambda sender: fnapp.close()),
        ),
    )
    
    fnapp.root = ui.NavigationView(lst)
    fnapp.root.navigation_bar_hidden = False
    fnapp.root.flex = "WH"
    if MODE == "popover":
        fnapp.root.height = 1000
    
    if ns.dir:
        fnapp.push_view(fnapp.make_file_list(common.FileItem(ns.dir)))
    
    fnapp.root.present(MODE, hide_title_bar=True)
    
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
