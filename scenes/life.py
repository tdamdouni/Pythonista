# https://bitbucket.org/cromulentarian/life-pythonista/overview
# -*- coding: utf-8 -*-
# Conway's game of life.
# Touch cells to give them life.
# Tap screen with two fingers to pause/un-pause.
# Tap screen with three fingers to give life to random cells.
#
# GUI bits via https://gist.github.com/SebastianJarsve/8832970

import scene
from PIL import Image, ImageDraw
import random
import time

class Cell (object):
    def __init__(self, x, y, frame):
        self.frame = frame
        self.alive = False

    def draw(self):
        background = scene.Color(1, 1, 1) if self.alive else scene.Color(0, 0, 0)
        scene.fill(*background)
        scene.rect(*self.frame)

class Grid (object):
    def __init__(self, screen, w, h):
        self.size = scene.Size(w, h)
        w, h = (screen.w/w, screen.h/h)
        self.cells = {
            (x, y) : Cell(x, y, scene.Rect(x*w, y*h, w, h))
          for x in xrange(self.size.w)
          for y in xrange(self.size.h)
        }
        grid_img = Image.new('RGBA', [int(i) for i in screen.as_tuple()])
        grid_draw = ImageDraw.Draw(grid_img)

        for x in xrange(self.size.w):
            grid_draw.line((x*w, 0, x*w, screen.h))
        x = self.size.w
        grid_draw.line((x*w-1, 0, x*w-1, screen.h))

        for y in xrange(self.size.h):
            grid_draw.line((0, y*h, screen.w, y*h))
        y = self.size.h
        grid_draw.line((0, y*h-1, screen.w, y*h-1))
        self.grid_img = scene.load_pil_image(grid_img)
        del grid_img, grid_draw

    def turn_on(self, pos):
        self.cells[pos].alive = True

    def get_grid_position(self, location):
        for pos, cell in self.cells.iteritems():
            if location in cell.frame:
                return pos

    def update(self, next_gen):
        for k in self.cells.values():
            k.alive = False
        for l in next_gen:
            self.cells[l].alive = True

    def draw(self):
        scene.background(0, 0, 0)
        for c in self.cells.values():
            if c.alive:
                c.draw()
        scene.stroke(1,1,1)
        scene.stroke_weight(1)
        scene.image(self.grid_img, 0, 0)

WIDTH=50
HEIGHT=35

class MyScene (scene.Scene):
    def setup(self):
        self.paused = True
        self.grid = Grid(self.size, WIDTH, HEIGHT)
        self.curr_gen = set()
    def draw(self):
        self.grid.draw()
        if not self.paused:
            if len(self.curr_gen) == 0:
                self.paused = True
            if len(self.curr_gen) > 0:
                self.curr_gen = {wrap(p) for p in get_next_gen(self.curr_gen)}
                self.grid.update(self.curr_gen)
                #time.sleep(0.1)
        for touch in self.touches.values():
            if len(self.touches) == 1:
                pos = self.grid.get_grid_position(touch.location)
                if pos:
                    self.grid.turn_on(pos)
                    self.curr_gen.add(pos)

    def touch_began(self, touch):
        if len(self.touches) > 1:
            self.paused = True if not self.paused else False
            if len(self.touches) == 3:
                pos_list = randomize(self.grid.size)
                for pos in pos_list:
                    self.grid.turn_on(pos)
                    self.curr_gen.add(pos)

def get_next_gen(curr_gen):
    '''Given current active position list, return next active position list'''
    neighbors = flatmap(get_neighbors, curr_gen)
    wrapped_neighbors = set(map(wrap, neighbors))
    active = curr_gen | wrapped_neighbors
    counts = [(cell, count_neighbors(cell, curr_gen)) for cell in active]
    return set([
        cell for (cell, count) 
        in counts 
        if count == 3 or (count == 2 and cell in curr_gen)
    ])

def get_neighbors(pos):
    '''Given a position, return neighboring positions'''
    cx, cy = pos
    return [
        (cx - 1, cy - 1),
        (cx, cy - 1),
        (cx + 1, cy - 1),
        (cx - 1, cy),
        (cx + 1, cy),
        (cx - 1, cy + 1),
        (cx, cy + 1),
        (cx + 1, cy + 1),
    ]

def flatmap(fn, sequence):
    '''Map a list producing function over a collection and flatten the result into a single list'''
    return [
        l for lists 
        in [fn(item) for item in sequence] 
        for l in lists
    ]

def count_neighbors(cell, curr_gen):
    '''Given a position and a list of active positions, return count of active neighbors'''
    return sum((neigh in curr_gen) for neigh in map(wrap, get_neighbors(cell)))

def wrap(position):
    '''Given any position, return a position that fits on the grid'''
    w, h = WIDTH, HEIGHT
    x, y = position
    return (x + w) % w, (y + h) % h

def randomize(size):
    '''Given dimensions of screen, return list of random active positions'''
    w, h = size
    return [
        (random.randint(0, w - 1), random.randint(0, h - 1)) 
        for i in xrange(int((w * h) ** 0.5) * 2)
    ]

if __name__ == '__main__':
    scene.run(MyScene())