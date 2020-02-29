from __future__ import print_function
# https://forum.omz-software.com/topic/2343/why-does-this-flicker

# coding: utf-8

import ui

class DragDrop(ui.View):
    def touch_moved(self, touch):
        cx, cy = touch.location
        ox, oy = touch.prev_location
        tx, ty = ox-cx, oy-cy
        print(tx, ty)
        self.x -= tx
        self.y -= ty
        
v=ui.View()
dnd = DragDrop(frame=(100,100,100,100))
dnd.background_color=(0,0,0)
v.add_subview(dnd)
v.present(hide_title_bar=1)

