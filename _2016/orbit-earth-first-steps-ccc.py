# https://forum.omz-software.com/topic/3754/show-all-scene-child-nodes

import scene

'''
Trying to create a rotating earth in an eliptical orbit around the sun.
'''

class SolorSystemScene(scene.Scene):
	def setup(self):
		center = self.bounds.center()
		sun = scene.SpriteNode('plc:Star', position=center, parent=self)
		earth = scene.SpriteNode('plc:Tree_Ugly', position=center + (150, 150),
		parent=self, speed=0.2)
		earth.run_action(scene.Action.rotate_by(10))
		earth.run_action(scene.Action.move_to(center.x - 150, center.y - 150))
		
scene.run(SolorSystemScene())

