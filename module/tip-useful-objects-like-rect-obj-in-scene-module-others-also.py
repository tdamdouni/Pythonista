# coding: utf-8

# https://forum.omz-software.com/topic/2518/tip-useful-objects-like-rect-obj-in-scene-module-others-also


from scene import Rect

#==============================

import scene, ui
assert dir(scene.Point())   == dir(ui.Point())
assert dir(scene.Rect())    == dir(ui.Rect())
assert dir(scene.Vector2()) == dir(ui.Vector2())
print('Success!')

#==============================

>>> ui.Rect(1,1,5,5) in ui.Rect(0,0,10,10)
True
>>> ui.Rect(1,1,15,15) in ui.Rect(0,0,10,10)
False
>>> ui.Point(1,1) in ui.Rect(0,0,10,10)
True
>>> ui.Point(-1,1) in ui.Rect(0,0,10,10)
False

#==============================

assert(ui.Rect is scene.Rect)

#==============================

>>> v=ui.View(0,0,100,100)
>>> b=ui.Button(frame=(v.width,0,-30,30))
>>> b.frame
Rect(70.00, 0.00, 30.00, 30.00)

#==============================

touch in sprite_node                 # throws a TypeError -- I like this syntax!
touch.location in sprite_node        # throws a TypeError
touch in sprite_node.frame           # always returns False
touch.location in sprite_node.frame  # a real hit test

...

import scene

class MyScene(scene.Scene):
	def setup(self):
		self.snake = scene.SpriteNode(parent=self, position=self.bounds.center(),
		texture=scene.Texture('emj:Snake'))
		
	def touch_ended(self, touch):
		# print(touch in self.snake)             # TypeError SpriteNode is not iterable
		# print(touch.location in self.snake)    # TypeError SpriteNode is not iterable
		print(touch in self.snake.frame,         # always False
		touch.location in self.snake.frame)  # a real hit test
		
if __name__ == '__main__':
	scene.run(MyScene())
	
#==============================

import inspect, scene, ui
common = set(dict(inspect.getmembers(scene, inspect.isclass)))
common &= set(dict(inspect.getmembers(ui, inspect.isclass)))
common = sorted(list(common))
for cls in common:
	print 'class', cls, 'in scene and ui are', 'identical' if getattr(scene, cls) is getattr(ui, cls) else 'different'
	
#==============================

class Button in scene and ui are different
class Point in scene and ui are identical
class Rect in scene and ui are identical
class Size in scene and ui are identical
class Touch in scene and ui are different
class Vector2 in scene and ui are identical

