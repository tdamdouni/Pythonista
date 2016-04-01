# https://forum.omz-software.com/topic/2255/agar-io-clone-help

# coding: utf-8

from scene import *
class MyScene (Scene):
    def setup(self):
        self.layer = Layer(Rect(self.size.w * 0.5, self.size.h * 0.5, 16, 16))
        self.layer.background = Color(1, 0, 0)
        
    def draw(self):
        background(0, 0, 0)
        self.layer.update(self.dt)
        self.layer.draw()
        ellipse(self.size.w * 0.5 + 90, self.size.h * 0.5 - 160, 120, 120)
        
    def touch_moved(self, touch):
        new_frame = Rect(touch.location.x -160, touch.location.y + 90, 16, 16)
        self.layer.animate('frame', new_frame, duration=0.1)
        fill(1,0,0)
        
run(MyScene(), LANDSCAPE)

# And the code for the food:

from scene import *
from random import *
import time
import sys
class Particle(object):
    def __init__(self, wh):
        self.w = wh.w*4
        self.h = wh.h*4
        self.x = randint(0, self.w)
        self.y = randint(0, self.h)
        self.vx = randint(-10, 20)
        self.vy = randint(-10, 20)
        self.colour = Color(random(), random(), random())

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        if self.x > self.w:
            self.x = self.w
            self.vx *= -1
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        if self.y > self.h:
            self.y = self.h
            self.vy *= -1
        if self.y < 0:
            self.y = 0
            self.vy *= -1
            
    def draw(self):
        fill(*self.colour)
        ellipse(self.x, self.y, 8, 8)

class Intro(Scene):
    def setup(self):
        num=100
        self.particles = []
        for p in xrange(num):
            self.particles.append(Particle(self.size))
            
    def draw(self):
        background(0.00, 0.05, 0.20)
        for p in self.particles:
            p.update()
            p.draw()
        for t in self.touches.values():
            for p in self.particles:
                tx, ty = t.location.x, t.location.y
                d = (p.x - tx)*(p.x - tx)+(p.y - ty)*(p.y - ty)
                d = sqrt(d)
                p.vx = p.vx - 5/d*(p.x-tx)
                p.vy = p.vy - 5/d*(p.y-ty)
                p.colour = Color(random(), random(), random())
                
run(Intro(), LANDSCAPE)