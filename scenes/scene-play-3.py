# https://forum.omz-software.com/topic/3684/basic-touch-question/4

import scene,ui

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
			self.buttonTouchId = touch.touch_id
			self.ship.run_action(
			scene.Action.move_to(self.size[0], self.size[1], 2,
			scene.TIMING_SINODIAL),
			'move_action_key')
			
	def touch_ended(self, touch):
		if touch.touch_id == self.buttonTouchId:
			self.buttonTouchId = None
			self.ship.remove_action('move_action_key')
			
if __name__ == '__main__':
	scene.run(MyScene(), scene.LANDSCAPE, show_fps=True)

