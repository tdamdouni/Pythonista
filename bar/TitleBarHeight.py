# coding: utf-8

# https://forum.omz-software.com/topic/1618/any-ios-device/2

from __future__ import print_function
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

