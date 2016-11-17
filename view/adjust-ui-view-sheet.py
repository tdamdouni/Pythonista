# coding: utf-8

# https://forum.omz-software.com/topic/2546/ui-view-present-sheet-will-probably-be-too-small-in-pythonista-v2

import ui
view.width = view.height = min(ui.get_screen_size())
view.present('sheet')

