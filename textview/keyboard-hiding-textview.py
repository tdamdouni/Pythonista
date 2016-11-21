# coding: utf-8

# https://forum.omz-software.com/topic/2701/keyboard-hiding-textview 

from scene import *
import sound
import random
import math
from ui import Path
A = Action

class MyScene (Scene):
	def setup(self):
		h = 200
		w = 300
		p = Path()
		p.line_to(w/2, h)
		p.line_to(-(w/2), h)
		p.close()
		self.s = ShapeNode(p)
		self.s.anchor_point = (0.5, 0)
		self.s.position = (self.size.x/2, self.size.y/2)
		self.add_child(self.s)
		
		ph = Path()
		ph.line_to(self.size.x, 0)
		ph.line_to(self.size.x, 1)
		ph.line_to(0, 1)
		ph.close()
		self.lh = ShapeNode(ph)
		self.lh.fill_color = 'red'
		self.lh.position = (self.size.x/2, self.size.y/2)
		self.add_child(self.lh)
		
		pv = Path()
		pv.line_to(0, self.size.y)
		pv.line_to(1, self.size.y)
		pv.line_to(1, 0)
		pv.close()
		self.lv = ShapeNode(pv)
		self.lv.fill_color = 'red'
		self.lv.position = (self.size.x/2, self.size.y/2)
		self.add_child(self.lv)
		
	def did_change_size(self):
		pass
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
	
		node_x, node_y = self.s.point_from_scene(touch.location)
		node_y = self.s.frame.h - node_y
		self.lh.position = (self.lh.position.x, touch.location.y)
		self.lv.position = (touch.location.x, self.lv.position.y)
		if self.s.path.hit_test(node_x, node_y):
			self.s.fill_color = 'green'
		else:
			self.s.fill_color = 'white'
			
	def touch_ended(self, touch):
		pass
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)

