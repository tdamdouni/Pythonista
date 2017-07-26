# https://github.com/zacbir/pythonista

import random

from canvas import *

def shade_of(color):
	r, g, b = color
	return r, g, b, random.random() * 0.25 + 0.25

def gen_color(r, g, b):
    return (r/255.0, g/255.0, b/255.0)

def avg(color):
	return float(sum(color) / len(color))

class Theme:
	
	def __init__(self, name, colors):
		self.name = name
		self.colors = [gen_color(*color) for color in colors]
		self.lightest = self.determine_lightest()
		self.darkest = self.determine_darkest()
		
	def determine_lightest(self):
		avgs = [(avg(color), color) for color in self.colors]
		return max(avgs)[1]
		
	def determine_darkest(self):
		avgs = [(avg(color), color) for color in self.colors]
		return min(avgs)[1]

mucha_winter = Theme(
    name='Mucha Winter',
    colors=(
        (242.0, 212.0, 155.0),
        (242.0, 178.0, 102.0),
        (191.0, 111.0, 65.0),
        (89.0, 18.0, 2.0),
        (55.0, 69.0, 65.0),
    ))

mabelis = Theme(
    name='Mabelis',
    colors=(
        (88.0, 0.0, 34.0),
        (170.0, 44.0, 48.0),
        (255.0, 190.0, 141.0),
        (72.0, 123.0, 127.0),
        (1.0, 29.0, 36.0),
    ))

full_of_life = Theme(
    name='Full of Life',
    colors=(
        (2.0, 115.0, 115.0),
        (3.0, 140.0, 127.0),
        (217.0, 179.0, 67.0),
        (242.0, 140.0, 58.0),
        (191.0, 63.0, 52.0),
    ))

let_the_rays_fall_on_the_earth = Theme(
    name='Let the Rays Fall on the Earth',
    colors=(
        (64.0, 39.0, 104.0),
        (127.0, 83.0, 112.0),
        (191.0, 117.0, 96.0),
        (229.0, 141.0, 0.0),
        (255.0, 183.0, 0.0),
    ))

robots_are_cool = Theme(
    name='Robots Are Cool',
    colors=(
        (30.0, 58.0, 64.0),
        (104.0, 140.0, 140.0),
        (217.0, 209.0, 186.0),
        (242.0, 209.0, 148.0),
        (242.0, 160.0, 87.0),
    ))

def draw_block(x, y, theme):
    start_x, start_y = x, y
    for palette_color in theme.colors:
        set_fill_color(*palette_color)
        fill_rect(start_x, start_y, 25.0, 50.0)
        start_x += 25.0
    
    start_x += 10.0
    set_fill_color(*theme.darkest)
    fill_rect(start_x, start_y, 25.0, 50.0)

    start_x += 35.0
    set_fill_color(*theme.lightest)
    fill_rect(start_x, start_y, 25.0, 50.0)

themes = (mucha_winter, mabelis, full_of_life, let_the_rays_fall_on_the_earth, robots_are_cool)

if __name__ == 'main':
	set_size(1024.0, 1024.0)

	start_x = 10.0
	start_y = 10.0

	for theme in themes:
	    draw_block(start_x, start_y, theme)
	    start_y += 60.0
