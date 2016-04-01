from scene import *
import math

class MyScene (Scene):
    def __init__(self):
        self.distance_old = 0.0
        self.distance_new = 0.0
        self.reset = True
        self.zoom = 0
        
    def draw (self):
        background(0, 0, 0)
        locations = [[0,0],[0,0]]
        i = 0
        if len(self.touches) == 2:
            for touch in self.touches.values():
                locations[i] = touch.location
                i += 1
            if self.reset:
                self.reset = False
                self.distance_old = math.sqrt(math.pow((locations[1][0] - locations[0][0]),2) + pow((locations[1][1] - locations[0][1]),2))
            else:
                self.distance_new = math.sqrt(math.pow((locations[1][0] - locations[0][0]),2) + pow((locations[1][1] - locations[0][1]),2))
                self.zoom = self.distance_old - self.distance_new
        #print self.zoom

    def touch_ended(self,touch):
         self.reset = True
         
run(MyScene())
