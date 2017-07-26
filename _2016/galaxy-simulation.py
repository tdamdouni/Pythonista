# https://forum.omz-software.com/topic/3754/show-all-scene-child-nodes/6

import scene
from math import pi

A = scene.Action

'''
Trying to create a rotating earth in an eliptical orbit around the sun.
'''

def make_action(steps, speed):
	return A.repeat(A.sequence(A.rotate_to(steps * pi, speed),
	A.rotate_to(0, 0), 0), 0)
	
	
class Planet(scene.Node):
	def __init__(self, parent, orbit=150, image_name=''):
		parent.add_child(self)
		self.position = parent.bounds.center()
		self.run_action(make_action(20, orbit / 5))
		image_name = image_name or 'emj:Moon_5'
		planet = scene.SpriteNode(image_name, parent=self, position=(0, orbit))
		planet.run_action(make_action(20, 5))
		
		
class SolorSystemScene(scene.Scene):
	def setup(self):
		center = self.bounds.center()
		sun = scene.SpriteNode('emj:Sun_1', position=center, parent=self)
		earth = Planet(self)
		venus = Planet(self, 75, 'emj:Blue_Circle')
		mars = Planet(self, 225, 'emj:Moon_2')
		saturn = Planet(self, 300, 'emj:Moon_4')
		jupiter = Planet(self, 375, 'emj:Moon_1')
		
scene.run(SolorSystemScene())

