# coding: utf-8

# https://forum.omz-software.com/topic/992/check-if-pythonista-is-in-background

from __future__ import print_function
import webrowser
webrowser.open('safari-http://')
# I want the next line to execute only when returning back to Pythonista
print("Back here")


#==============================

import ui, scene

class scTest(scene.Scene):
	def pause(self):
		print('pause')
		
	def resume(self):
		print('resume')
		
if False:
	scene.run(scTest())
else:
	v = ui.View()
	sv = scene.SceneView()
	sv.scene = scTest()
	#sv.hidden = True
	v.add_subview(sv)
	v.present('panel')
	
#==============================


import ui, scene

def AmIBack():
	global gbGone
	if gbGone and not sv.paused:
		gbGone = False
		print("Back here")
	else:
		if sv.paused:
			gbGone = True
		ui.delay(AmIBack, 1)
		
gbGone = False
v = ui.View()
sv = scene.SceneView()
sv.hidden = True
v.add_subview(sv)
v.present('panel')
AmIBack()

