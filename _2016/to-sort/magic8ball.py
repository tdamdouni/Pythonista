#coding: utf-8


import random, motion, scene
from scene import *

choices = [
"Go for it!",
"No way, Jose!",
"I'm not sure.\nAsk me again.",
"Fear of the\nunknown is\nwhat imprisons\nus.",
"It would be\nmadness to\ndo that!",
"Makes no\ndifference to\nme, do or don't\n- whatever.",
"Yes, I think on\nbalance, that is\nthe right choice.",
]
class Particle(object):
    def __init__(self, wh):
        self.w = wh.w
        self.h = wh.h
        self.x = random.randint(0, self.w)
        self.y = random.randint(0, self.h)
        self.vx = random.randint(-10, 20)
        self.vy = random.randint(-10, 20)
        self.colour = Color(random.random(), random.random(), random.random())

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
        rect(self.x, self.y, 8, 8)

class MyScene(Scene):
    def setup(self):
        self.particles = []
        for p in xrange(200):
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
                p.colour = Color(random.random(), random.random(), random.random())

        s = 45 if self.size.w > 100 else 7
        text('Welcome to\nMyMagic8Ball\n\n\n', 'Futura', s, *self.bounds.center().as_tuple())
        t = 100 if self.size.w > 100 else 7
        text('\nðŸŽ±', 'Futura', t, *self.bounds.center().as_tuple())
        s = 27 if self.size.w > 100 else 7
        text('\n\n\n\n\n\n\n\n\n\n\n\nBy: Adedayo Ogunnoiki', 'Futura', s, *self.bounds.center().as_tuple())

    def touch_ended(self, touch):
        run(Help())


use_motion = True

class Help(Scene):
    def setup(self):
        self.particles = []
        for p in xrange(200):
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
                p.colour = Color(random.random(), random.random(), random.random())

        s = 45 if self.size.w > 100 else 7
        text('Ask me for\nadvice, then\ntap the screen.\nOr click the â�Ž\nat the top\nright of the \nscreen to exit.', 'Futura', s, *self.bounds.center().as_tuple())

    def touch_ended(self, touch):
        global answer
        answer = random.choice(choices)
        run(Advice())

use_motion = True

class Advice(scene.Scene):
    def __init__(self):
        scene.run(self, frame_interval=0)

    def setup(self):
        self.center = self.bounds.center()
        if use_motion:
            motion.start_updates()
        self.particles = []
        for p in xrange(200):
            self.particles.append(Particle(self.size))

    def stop(self):
        if use_motion:
            motion.stop_updates()

    def draw(self):
        x,y,z = motion.get_attitude() if use_motion else scene.gravity()
        r,g,b = abs(x), abs(y), abs(z)
        scene.background(r, g, b)
        scene.tint(1-r, 1-g, 1-b)
        scene.text(answer.format(x, y, z), font_size=45, x=self.center.x, y=self.center.y)
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
                p.colour = Color(random.random(), random.random(), random.random())

    def touch_ended(self, touch):
        run(Help())

run(MyScene())
