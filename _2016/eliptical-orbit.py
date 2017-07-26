# https://forum.omz-software.com/topic/3754/show-all-scene-child-nodes/3

import scene
from math import pi

'''
Trying to create a rotating earth in an eliptical orbit around the sun.
'''

class SolorSystemScene(scene.Scene):
	def setup(self):
		center = self.bounds.center()
		sun = scene.SpriteNode('plc:Star', position=center, parent=self)
		earth_anchor = scene.Node(position=center, parent=self)
		earth = scene.SpriteNode('plc:Tree_Ugly', position=(0, 150))
		earth_anchor.add_child(earth)
		self_rotate_action = scene.Action.repeat(scene.Action.sequence(scene.Action.rotate_to(20*pi, 5),
		scene.Action.rotate_to(0,0), 0),0)
		earth.run_action(self_rotate_action)
		rotate_action = scene.Action.repeat(scene.Action.sequence(scene.Action.rotate_to(20*pi, 20),
		scene.Action.rotate_to(0,0), 0),0)
		earth_anchor.run_action(rotate_action)
		
scene.run(SolorSystemScene())

