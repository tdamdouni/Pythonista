# https://forum.omz-software.com/topic/2259/help-with-unlocal-variable

# coding: utf-8

from scene import *
from random import *
class Particle(object):
    def __init__(self, wh):
        self.w = wh.w
        self.h = wh.h
        self.x = randint(0, self.w)
        self.y = randint(0, self.h)
        self.vx = randint(-10, 20)
        self.vy = randint(-10, 20)
        self.colour = Color(random(), random(), random())

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0
        self.vy *= 0
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
        self.cells=Rect(self.x, self.y, 5, 5)
        fill(*self.colour)
        ellipse(*self.cells)
        if self.cells.intersects(self.cells):
            pass

class Intro(Scene):
    def setup(self):
        self.player = Rect(240,160, 10, 10)
        self.colour = Color(random(), random(), random())
        num=100
        self.particles = []
        for p in xrange(num):
            self.particles.append(Particle(self.size))
        if self.player.intersects(self.cells):
            pass
            
    def draw(self):
        background(0.00, 0.05, 0.20)
        fill(*self.colour)
        ellipse(*self.player)
        for p in self.particles:
            p.update()
            p.draw()
    
run(Intro(), LANDSCAPE)