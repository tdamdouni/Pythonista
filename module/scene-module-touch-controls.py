# coding: utf-8

# https://forum.omz-software.com/topic/3485/scene-module-touch-controls/3

import scene, ui

class ButtonNode (scene.SpriteNode):
	def __init__(self, title, *args, **kwargs):
		scene.SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		font_color = 'black'
		self.title_label = scene.LabelNode(title,
		font=button_font,
		color=font_color,
		position=(0, 0),
		parent=self)
		self.title = title
		#self.color = 'lime' #background color
		
	def touch_began(self, touch):
		if self.title == '←':
			x, y = self.parent.sprite.position
			self.parent.sprite.position = ((x-20) if (x-20) > 0 else x, y)
		elif self.title == '→':
			x, y = self.parent.sprite.position
			self.parent.sprite.position = ((x+20) if (x+20) < self.parent.size[0] else x, y)
		elif self.title == '↓':
			x, y = self.parent.sprite.position
			self.parent.sprite.position = (x, (y-20) if (y-20) > 0 else y)
		elif self.title == '↑':
			x, y = self.parent.sprite.position
			self.parent.sprite.position = (x, (y+20) if (y+20) < self.parent.size[1] else y)
			
class MyScene(scene.Scene):
	def setup(self):
		self.sprite = scene.SpriteNode('Dog_Face', position=self.size/2, parent=self)
		self.left_button = ButtonNode('←',
		position=(self.size[0]/2.0 - 300, self.size[1]/2-300), parent=self)
		self.right_button = ButtonNode('→',
		position=(self.size[0]/2.0-100, self.size[1]/2-300), parent=self)
		self.down_button = ButtonNode('↓',
		position=(self.size[0]/2.0 +100, self.size[1]/2-300), parent=self)
		self.up_button = ButtonNode('↑',
		position=(self.size[0]/2.0+300, self.size[1]/2-300), parent=self)
		
	def touch_began(self, touch):
		for node in self.children:
			if hasattr(node, 'touch_began'):
				if touch.location in node.frame:
					node.touch_began(touch)
					
scene.run(MyScene())

