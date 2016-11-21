# https://forum.omz-software.com/topic/3195/i-thought-about-spacing-my-questions-but-scene-present_modal_scene-issues

import scene
import ui

class Scene1(scene.Scene):

	def __init__(self):
		pass
		
	def touch_began(self, touch):
		self.menu = Scene2()
		self.present_modal_scene(self.menu)
		
		
class Scene2(scene.Scene):

	def __init__(self):
		pass
		
		
scene.run(Scene1())

# --------------------

import scene

class Scene1(scene.Scene):
	def setup(self):
		self.background_color = 'green'
		
	def touch_began(self, touch):
		next_scene = Scene2()
		self.view.scene = next_scene
		next_scene.setup()
		
class Scene2(scene.Scene):
	def setup(self):
		self.background_color = 'red'
		
		
scene.run(Scene1())

# --------------------

import scene
import ui

class Scene1(scene.Scene):

	def __init__(self):
		pass
		
	def touch_began(self, touch):
		self.menu = Scene2()
		self.present_modal_scene(self.menu)
		
		
class Scene2(scene.Scene):

	def __init__(self):
		pass
		
		
scene.run(Scene1())

# --------------------

import scene

class Scene1(scene.Scene):
	def setup(self):
		self.background_color = 'green'
		
	def touch_began(self, touch):
		next_scene = Scene2()
		self.view.scene = next_scene
		next_scene.setup()
		
class Scene2(scene.Scene):
	def setup(self):
		self.background_color = 'red'
		
		
scene.run(Scene1())

# --------------------

self.menu = Scene2()
self.present_modal_scene(self.menu)

# --------------------

self.present_modal_scene(Scene2())

# --------------------

