# coding: utf-8

# https://forum.omz-software.com/topic/2837/ui-scrollview-changing-what-a-page-stop-is/2 

import ui
from objc_util import *
from random import random

class PagingScrollContainer (ui.View):
    def __init__(self, scroll_view, **kwargs):
        ui.View.__init__(self, **kwargs)
        self.scroll_view = scroll_view
        # Center the scroll view horizontally:
        scroll_view.frame = (self.bounds.w/2 - scroll_view.bounds.w/2, 0, scroll_view.bounds.w, self.bounds.h)
        scroll_view.flex = 'HLR'
        scroll_view.shows_horizontal_scroll_indicator = False
        self.add_subview(scroll_view)
        # Turn off clipping:
        _scroll_view = ObjCInstance(scroll_view)
        _scroll_view.clipsToBounds = False
        # Make sure paging is enabled (that's the point after all)
        _scroll_view.pagingEnabled = True
        # Add the scroll view's gesture recognizer to this view:
        _self = ObjCInstance(self)
        _self.addGestureRecognizer_(_scroll_view.panGestureRecognizer())

def main():
    # Create a ScrollView with some colored "pages" as a demo...
    page_w = 200
    scroll_view = ui.ScrollView(frame=(0, 0, page_w, 500))
    scroll_view.content_size = (50 * page_w, 0)
    for i in range(50):
        swatch_frame = (i*page_w, 0, page_w, 500)
        swatch = ui.View(bg_color=(random(), random(), random()), frame=swatch_frame)
        scroll_view.add_subview(swatch)
    # Wrap it in the custom container view, and present that:
    container = PagingScrollContainer(scroll_view, frame=(0, 0, 500, 500))
    container.present('sheet')

if __name__ == '__main__':
    main()
