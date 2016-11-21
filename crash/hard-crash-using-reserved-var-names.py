# https://forum.omz-software.com/topic/3233/v2-0-vs-v2-1-hard-crash-using-reserved-var-names/2

#This guy produces an hard crash on v2.1

from scene import *
import sound
import random
import math
#import photos

class MyScene (Scene):
	def setup(self):
		self.background_color = '#ffffff'
		
		self.target = SpriteNode('iob:ionic_256')
		
		self.add_child(self.target)
		
		pass
		
	def did_change_size(self):
		pass
		
	def update(self):
	
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
if __name__ == '__main__':
	run(MyScene(), PORTRAIT, show_fps=True)
	
# --------------------

import scene

class MyScene(scene.Scene):
	def setup(self):
		self.target = scene.SpriteNode('iob:alert_circled_256', parent=self)
		
if __name__ == '__main__':
	scene.run(MyScene(), show_fps=False)
	
# --------------------

#This guy produces an hard crash on v2.1

from scene import *
import sound
import random
import math
#import photos

class MyScene (Scene):
	def setup(self):
		self.background_color = '#ffffff'
		
		self.target = SpriteNode('iob:ionic_256')
		
		self.add_child(self.target)
		
		pass
		
	def did_change_size(self):
		pass
		
	def update(self):
	
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
if __name__ == '__main__':
	run(MyScene(), PORTRAIT, show_fps=True)
# --------------------
import scene

class MyScene(scene.Scene):
	def setup(self):
		self.target = scene.SpriteNode('iob:alert_circled_256', parent=self)
		
if __name__ == '__main__':
	scene.run(MyScene(), show_fps=False)
# --------------------
# coding: utf-8

from scene import *
import sound
import random
import math
A = Action

class MyScene (Scene):
	def setup(self):
		#Does not crash
		SpriteNode('emj:Airplane', position=self.size/2, parent=self)
		# Will crash
		SpriteNode('iow:alert_256', position=self.size/2, parent=self)
		
if __name__ == '__main__':
	run(MyScene(), show_fps=False)
# --------------------

