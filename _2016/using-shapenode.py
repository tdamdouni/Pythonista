# https://forum.omz-software.com/topic/3892/using-a-shapenode-instead-of-spritenode/2

import scene, ui

class Coin(scene.SpriteNode):
	def __init__(self, **kwargs):
		super().__init__('emj:Snowflake', **kwargs)
		
class Ball(scene.ShapeNode):
	def __init__(self, **kwargs):
		circle = ui.Path.oval (0, 0, 20, 20)
		super().__init__(circle, fill_color='red', stroke_color='clear', shadow=None, **kwargs)
		
class Polygon(scene.ShapeNode):
	def __init__(self, **kwargs):
		path = ui.Path()
		path.line_width = 5
		path.move_to(0, 0)
		path.line_to(200, 0)
		path.line_to(100, 100)
		path.close()
		super().__init__(path, **kwargs)
		
class MyScene(scene.Scene):
	def setup(self):
		self.ball = Ball(position=(200, 100), parent=self)
		self.coin = Coin(position=(200, 200), parent=self)
		self.triangle1 = Polygon(fill_color='skyblue', stroke_color='green',
		position=(200, 400), parent=self)
		self.triangle2 = Polygon(fill_color='red', stroke_color='green',
		position=(200, 300), parent=self)
		
scene.run(MyScene())

