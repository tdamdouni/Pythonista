# https://forum.omz-software.com/topic/3824/how-to-use-or-call-a-navigation-view

import ui

view = ui.load_view("main.pyui")
view_to_push = ui.load_view("view_to_push.pyui")
view["navview"].push_view(view_to_push)
