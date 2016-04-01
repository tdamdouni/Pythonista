# https://github.com/Pythonistapro777/Python-Scripts/blob/master/Agar.io

from scene import *
from random import *

class Particle(object):
        def __init__(self, wh):
                self.w = wh.w
                self.h = wh.h
                self.x = randint(self.w*-1, self.w)
                self.y = randint(self.h*-1, self.h)
                self.colour = Color(random(), random(), random())
                self.cells=Rect(self.x, self.y, 5, 5)

        def update(self):
                self.cells=Rect(self.x, self.y, 5, 5)

        def draw(self):
                stroke(*self.colour)
                ellipse(*self.cells)
                global attackx
                attackx=self.x
                global attacky
                attacky=self.y

class Bots(object):
        def __init__(self, wh):
                self.w = wh.w
                self.h = wh.h
                self.x = randint(self.w*-1, self.w)
                self.y = randint(self.h*-1, self.h)
                self.colour = Color(random(), random(), random())
                self.bsize=8

                self.lw=self.w*-1
                self.rw=self.w
                self.bh=self.h*-1
                self.th=self.h

        def update(self):
                self.attackers=Rect(self.x, self.y, self.bsize, self.bsize)
                stroke(0,0,0)
                stroke_weight(4)
                line(self.lw, self.bh, self.lw, self.th)
                line(self.lw, self.th, self.rw, self.th)
                line(self.rw, self.bh, self.rw, self.th)
                line(self.lw, self.bh, self.rw, self.bh)

        def draw(self):
                fill(*self.colour)
                stroke(*self.colour)
                ellipse(*self.attackers)

class Intro(Scene):
        def setup(self):
                global count
                count=0
                global psize
                psize=8
                plocx=240
                plocy=160
                self.player = Rect(plocx, plocy, psize, psize)
                self.colour = Color(random(), random(), random())
                self.particles = []
                for p in range(50):
                        self.particles.append(Particle(self.size))
                self.bots = []
                for b in range(1):
                        self.bots.append(Bots(self.size))

        def touch_began(self, touch):
                global x1
                global y1
                x1=touch.location.x
                y1=touch.location.y


        def touch_moved(self, touch):
                global x
                global y
                x=touch.location.x
                y=touch.location.y
                global count
                count = 1

        def movecells(self):
                global x
                global x1
                global y
                global y1
                global plocx
                global plocy
                global psize
                for p in self.particles:
                        for b in self.bots:
                                if x1 > x and b.lw < plocx:
                                        p.x += 2
                                        b.lw += 0.04
                                        b.rw += 0.04
                                if x1 < x and b.rw > plocx+psize:
                                        p.x += -2
                                        b.lw += -0.04
                                        b.rw += -0.04
                                if y1 > y and b.bh < plocy:
                                        p.y += 2
                                        b.bh += 0.04
                                        b.th += 0.04
                                if y1 < y and b.th > plocy+psize:
                                        p.y += -2
                                        b.bh += -0.04
                                        b.th += -0.04

        def draw(self):
                global count
                if count == 1:
                        self.movecells()
                global psize
                background(0.00, 0.05, 0.20)
                for p in self.particles:
                        p.update()
                        p.draw()
                        global plocx
                        global plocy
                        plocx=p.w/2-psize/2
                        plocy=p.h/2-psize/2
                        if self.player.intersects(p.cells):
                                self.particles.remove(p)
                                psize+=0.2
                                for p.cells in range(1):
                                                self.particles.append(Particle(self.size))
                for b in self.bots:
                        b.update()
                        b.draw()
                        for p in self.particles:
                                global attackx
                                global attacky
                                if b.x < attackx:
                                        b.x += 0.05

                                if b.y < attacky:
                                        b.y += 0.05

                                if b.x > attackx:
                                        b.x -= 0.05

                                if b.y > attacky:
                                        b.y -= 0.05

                                if b.attackers.intersects(p.cells):
                                        self.particles.remove(p)
                                        b.bsize+=0.2
                                        for p in range(1):
                                                self.particles.append(Particle(self.size))

                self.player = Rect(plocx, plocy, psize, psize)
                stroke(*self.colour)
                fill(*self.colour)
                ellipse(*self.player)

run(Intro(), LANDSCAPE)