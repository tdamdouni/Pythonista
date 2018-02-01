# https://forum.omz-software.com/topic/4284/how-do-i-make-a-full-screen-button-and-handle-button-down-and-button-up-events/7

import scene

class MyScene(scene.Scene):
	def setup(self):
		self.name = scene.LabelNode('', position=self.size/2,
		font=('courier', 60), parent=self)
		
	def touch_began(self, touch):
		self.tap_time = self.t
		
	def touch_ended(self, touch):
		self.name.text += '.' if (self.t - self.tap_time) < .2 else '-'
		
scene.run(MyScene())
import scene

class MyScene(scene.Scene):
	def setup(self):
		self.name = scene.SpriteNode(color=(1,1,1), position=self.size/2,
		size=self.size, parent=self)
		self.name.alpha = 0
		A = scene.Action
		self.dot_action = A.sequence(
		A.fade_to(1, .2),
		A.fade_to(0, .2))
		self.dash_action = A.sequence(
		A.fade_to(1, .5),
		A.fade_to(0, .5))
		
	def touch_began(self, touch):
		self.tap_time = self.t
		
	def touch_ended(self, touch):
		if (self.t - self.tap_time) < .2:
			self.name.run_action(self.dot_action)
		else:
			self.name.run_action(self.dash_action)
			
scene.run(MyScene())

