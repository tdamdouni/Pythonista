# https://forum.omz-software.com/topic/2261/help-with-agar-io-clone-still-not-solved

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
        global cells
        cells=Rect(self.x, self.y, 5, 5)

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
        fill(*self.colour)
        ellipse(*cells)
            
class Intro(Scene):
    def setup(self):
        self.psize=10
        global plocx
        plocx=240
        global plocy
        plocy=160
        global newplocx
        newplocx = 0
        global newplocy
        newplocy = 0
        self.player = Rect(plocx, plocy, 16, 16)
        self.colour = Color(random(), random(), random())
        self.particles = []
        for p in xrange(100):
            self.particles.append(Particle(self.size))
            
    def touch_began(self, touch):
        global x1
        x1=touch.location.x
        global y1
        y1=touch.location.y
        

    def touch_moved(self, touch):
        global plocx
        global plocy
        global newplocx
        global newplocy
        x=touch.location.x
        y=touch.location.y
        if x > x1:
            addx=x-x1
            newplocx=plocx+addx
        if x < x1:
            subx=x-x1
            newplocx=plocx+subx
        if y > y1:
            addy=y-y1
            newplocy=plocy+addy
        if y < y1:
            suby=y-y1
            newplocy=plocy+suby
            
        while newplocx != plocx and newplocy > plocx:
            plocx = plocx + 1
            self.player = Rect(plocx, plocx, 16, 16)
        if plocx == newplocx:
            self.player = Rect(plocx, plocy, 16, 16)
                
        while newplocx != plocx and newplocx < plocx:
            plocx = plocx - 1
            self.player = Rect(plocx, plocy, 16, 16)
        if plocx == newplocx:
            self.player = Rect(plocx, plocy, 16, 16)
                
        while newplocy != plocy and newplocy > plocy:
            plocy = plocy + 1
            self.player = Rect(plocx, plocy, 16, 16)
        if plocy == newplocy:
            self.player = Rect(plocx, plocy, 16, 16)
    
        while newplocy != plocy and newplocy < plocy:
            plocy = plocy - 1
            self.player = Rect(plocx, plocy, 16, 16)
        if plocy == newplocy:
            self.player = Rect(plocx, plocy, 16, 16)
            
    def draw(self):
        global cells
        background(1, 1, 1)
        self.player = Rect(plocx, plocy, self.psize, self.psize)
        if not self.player.intersects(cells):
            ellipse(*self.player)
        if self.player.intersects(cells):
            self.cells=Rect(-2, -2, 5, 5)
            self.newpsize=self.psize
            self.newpsize=self.newpsize+1
            self.psize=self.newpsize
            ellipse(*self.player)
        for p in self.particles:
            p.update()
            p.draw()
    
run(Intro(), LANDSCAPE)