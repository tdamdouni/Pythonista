# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to [http://unlicense.org]
from scene import *
from random import *

class Die(object):
	def __init__(self, sides, x_pos):
		self.sides = sides
		side_length = 100
		half_side_length = side_length/2
		y_pos = 400
		self.r = Rect(x_pos-half_side_length, y_pos, side_length, side_length)
		self.rolling = 0
		self.result = None

	@property
	def name(self):
		return 'D' + str(self.sides)
	
	def draw(self):
		rect(self.r.x, self.r.y, self.r.w, self.r.h)
		text(self.name, x=self.r.x+50, y=self.r.y+50, font_size=24)
		if self.rolling > 0:
			self.result = randint(1, self.sides)
			self.rolling += 1
		if self.rolling == 20:
			self.rolling = 0
		if self.result:
			text(str(self.result), x=self.r.x+50, y=self.r.y-50, font_size=40)

	def touch_began(self, touch):
		if touch.location in self.r:
			self.rolling = 1
		else:
			self.result = None


class Dice(Scene):
	def setup(self):
		dice_sides = [4, 6, 8, 10, 12, 20, 100]
		x_positions = []
		x_distance = self.size.w/(len(dice_sides)+1)
		self.dice = []
		current_die = 1
		for sides in dice_sides:
			self.dice.append(Die(sides, x_distance*current_die))
			current_die += 1

	def draw(self):
		background(85.0/255, 101.0/255, 56.0/255)
		fill(0.4, 0.2, 0.2)
		text('Dice Roller', x=self.size.w/2, y=625, font_size=68)
		for die in self.dice:
			die.draw()
	
	def touch_began(self, touch):
		for die in self.dice:
			die.touch_began(touch)


run(Dice())
