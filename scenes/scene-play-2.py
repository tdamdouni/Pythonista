# https://forum.omz-software.com/topic/3684/basic-touch-question/2

import scene, ui

class MyScene(scene.Scene):
	def setup(self):
		self.background_color = 'midnightblue'
		self.ship = scene.SpriteNode('spc:PlayerShip1Orange',
		position=self.size/2,
		parent=self)
		self.button = scene.ShapeNode(ui.Path.oval(0,0, 100, 100),
		position=(200, 100),
		fill_color='green',
		parent=self)
		
	def touch_began(self, touch):
		if touch.location in self.button.frame:
			self.ship.run_action(
			scene.Action.move_to(self.size[0], self.size[1], 2,
			scene.TIMING_SINODIAL),
			'move_action_key')
			
	def touch_ended(self, touch):
		if touch.location in self.button.frame:
			self.ship.remove_action('move_action_key')
			
scene.run(MyScene(), show_fps=True)

