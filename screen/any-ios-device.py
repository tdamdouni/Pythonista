# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/1618/any-ios-device_

from __future__ import print_function
import ui

mainview = ui.View()
mainview.present()
subview = ui.View(frame=mainview.bounds)
mainview.add_subview(subview)
subview.border_width = 5
subview.border_color = 'pink'
subview.background_color = 'green'
subview.flex = 'WH'

###==============================

import ui

w, h = ui.get_screen_size()
mainview = ui.View(frame=(0, 0, w, h))
subview = ui.View(frame=mainview.bounds)
mainview.add_subview(subview)
subview.border_width = 5
subview.border_color = 'pink'
subview.background_color = 'green'
subview.flex = 'WH'
mainview.present()

###==============================

import ui, time
presentmodes=[('full_screen',True),('full_screen',False),('panel',True),('panel',False)]
for m in presentmodes:
	v=ui.View()
	w=ui.WebView()
	v.add_subview(w)
	v.present(m[0],hide_title_bar=m[1])
	orientation=w.eval_js('window.orientation')
	
	print(m, orientation, v.frame)
	time.sleep(1.0)
	v.close()
	time.sleep(1.0)
	
time.sleep(1.0)
print('complete')

###==============================

