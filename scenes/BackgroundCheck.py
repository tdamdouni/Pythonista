# coding: utf-8

# https://forum.omz-software.com/topic/992/check-if-pythonista-is-in-background

from __future__ import print_function
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