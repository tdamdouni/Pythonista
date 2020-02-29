# coding: utf-8

# https://forum.omz-software.com/topic/2531/animation-of-complex-objects

from __future__ import print_function
from scene import *
import ui

class MyScene(Scene):
            
        def draw(self):
            
            
            startx = 20
            starty = 20
            length = 100
            width = 200
            
            #simple shape
            # begin location
            fill(.5,.5,.5)
            rect(startx, starty, width, length )
            fill(0,1,0)
            rect(startx*2, starty, width/2, length/2)
            fill(1,0,0)
            ellipse(startx*2, starty*2, 10,10)
            ellipse(startx*8, starty*2, 10,10)
            
    
            
        def touch_began(self, touch):
            #end location
            print(touch.location.x, touch.location.y)
            push_matrix()
            scale(1.5, 1.5)
            translate(touch.location.x, touch.location.y)
            rotate(180)
            pop_matrix()
            
            
class SceneViewer(ui.View):
    def __init__(self, in_scene):
        
        self.present('fullscreen')
        self.scene_view = SceneView(frame=self.bounds)
        self.scene_view.scene = in_scene
        self.add_subview(self.scene_view)

SceneViewer(MyScene())




