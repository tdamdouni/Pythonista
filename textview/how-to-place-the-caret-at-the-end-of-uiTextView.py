# coding: utf-8

# https://forum.omz-software.com/topic/2730/bug-list-for-beta-release-201001/16

tv = ui.TextView()
tv.text = '123456789'
tv.present()
tv.begin_editing()
l = len(tv.text)
# l is 9
tv.selected_range = (l, l)
#==============================

from objc_util import *
# ...
on_main_thread(ObjCInstance(tv).setSelectedRange_)((l, l))

