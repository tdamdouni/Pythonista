# coding: utf-8

# https://gist.github.com/balachandrana/255a25f19fffe8ec4f384c1bcdad9792

# https://forum.omz-software.com/topic/3322/scene-vs-ui/2

import bz2
from base64 import b64decode
data = '''\
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
'''
# coding: utf-8
import scene
import ui

max_stroke_width = 20
max_corner_radius = 100

class ShapeParameters(object):
	def __init__(self,
	shape_type="rectangle",
	position=(0, 0),
	size=(100, 200),
	corner_radius=20,
	fill_color=(0,1,0, 1),
	stroke_color=(1,0,0, 1),
	stroke_width=0):
		self.shape_type = shape_type
		self.position = (.25*frame1.w, .25*frame1.h)
		self.orig_size = size
		self.size = (.5*frame1.w, .5*frame1.h)
		self.corner_radius = .25*max_corner_radius
		self.fill_color = fill_color
		self.stroke_color = stroke_color
		self.stroke_width = .25*max_stroke_width
		self.image = None
		self.update()
		
	def update(self):
		with ui.ImageContext(self.orig_size[0], self.orig_size[1]) as ctx:
			ui.set_color((.9,.9,.9,1.0))
			self.path = ui.Path.rect(0, 0, self.orig_size[0], self.orig_size[1])
			self.path.fill()
			if self.shape_type == "oval":
				self.path= ui.Path.oval(
				self.position[0], self.position[1],
				self.size[0], self.size[1])
			elif self.shape_type == "rectangle":
				self.path = ui.Path.rect(
				self.position[0], self.position[1],
				self.size[0], self.size[1])
			elif self.shape_type == "rounded_rectangle":
				self.path = ui.Path.rounded_rect(
				self.position[0], self.position[1],
				self.size[0], self.size[1], self.corner_radius)
			ui.set_color(self.fill_color)
			self.path.fill()
			ui.set_color(self.stroke_color)
			self.path.line_width = self.stroke_width
			self.path.stroke()
			self.image = ctx.get_image()
		v['button4'].background_image = self.image
		v['imageview1'].image = self.image
		v['view1'].subviews[0].set_needs_display()
		
def oval_button(sender):
	myscene_shape_parameters.shape_type = "oval"
	myscene_shape_parameters.update()
	
def rect_button(sender):
	myscene_shape_parameters.shape_type = "rectangle"
	myscene_shape_parameters.update()
	
def rounded_rect_button(sender):
	myscene_shape_parameters.shape_type = "rounded_rectangle"
	myscene_shape_parameters.update()
	
def stroke_color_r(sender):
	r, g, b, a = myscene_shape_parameters.stroke_color
	r = sender.superview['slider1'].value
	myscene_shape_parameters.stroke_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def stroke_color_g(sender):
	r, g, b, a = myscene_shape_parameters.stroke_color
	g = sender.superview['slider2'].value
	myscene_shape_parameters.stroke_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def stroke_color_b(sender):
	r, g, b, a = myscene_shape_parameters.stroke_color
	b = sender.superview['slider3'].value
	myscene_shape_parameters.stroke_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def fill_color_r(sender):
	r, g, b, a = myscene_shape_parameters.fill_color
	r = sender.superview['slider4'].value
	myscene_shape_parameters.fill_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def fill_color_g(sender):
	r, g, b, a = myscene_shape_parameters.fill_color
	g = sender.superview['slider5'].value
	myscene_shape_parameters.fill_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def fill_color_b(sender):
	r, g, b, a = myscene_shape_parameters.fill_color
	b = sender.superview['slider6'].value
	myscene_shape_parameters.fill_color = (r,g, b, a)
	myscene_shape_parameters.update()
	
def position_x(sender):
	myscene_shape_parameters.position = (sender.superview['slider7'].value*frame1.w,
	myscene_shape_parameters.position[1])
	myscene_shape_parameters.update()
	
def position_y(sender):
	myscene_shape_parameters.position = (myscene_shape_parameters.position[0],
	sender.superview['slider8'].value*frame1.h)
	myscene_shape_parameters.update()
	
def size_w(sender):
	myscene_shape_parameters.size = (sender.superview['slider9'].value*frame1.w,
	myscene_shape_parameters.size[1])
	myscene_shape_parameters.update()
	
def size_h(sender):
	myscene_shape_parameters.size = ( myscene_shape_parameters.size[0],
	sender.superview['slider10'].value*frame1.h)
	myscene_shape_parameters.update()
	
def corner_radius(sender):
	myscene_shape_parameters.corner_radius = sender.superview['slider11'].value*max_corner_radius
	myscene_shape_parameters.update()
	
def stroke_width(sender):
	myscene_shape_parameters.stroke_width = sender.superview['slider12'].value*max_stroke_width
	myscene_shape_parameters.update()
	
class MyView (ui.View):
	def __init__(self):
		self.path = None
		#pass
		
	def did_load(self):
		pass
		
	def will_close(self):
		pass
		
	def draw(self):
		ui.set_color((.9,.9,.9,1.0))
		self.path = ui.Path.rect(0, 0, self.width, self.height)
		self.path.fill()
		if myscene_shape_parameters.shape_type == "oval":
			self.path= ui.Path.oval(
			myscene_shape_parameters.position[0], myscene_shape_parameters.position[1],
			myscene_shape_parameters.size[0], myscene_shape_parameters.size[1])
		elif myscene_shape_parameters.shape_type == "rectangle":
			self.path = ui.Path.rect(
			myscene_shape_parameters.position[0], myscene_shape_parameters.position[1],
			myscene_shape_parameters.size[0], myscene_shape_parameters.size[1])
		elif myscene_shape_parameters.shape_type == "rounded_rectangle":
			self.path = ui.Path.rounded_rect(
			myscene_shape_parameters.position[0], myscene_shape_parameters.position[1],
			myscene_shape_parameters.size[0], myscene_shape_parameters.size[1],
			myscene_shape_parameters.corner_radius)
		ui.set_color(myscene_shape_parameters.fill_color)
		self.path.fill()
		ui.set_color(myscene_shape_parameters.stroke_color)
		self.path.line_width = myscene_shape_parameters.stroke_width
		self.path.stroke()
		
	def layout(self):
		pass
		
	def touch_began(self, touch):
		self.set_needs_display()
		
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
		
	def keyboard_frame_will_change(self, frame):
		pass
		
	def keyboard_frame_did_change(self, frame):
		pass
		
class MyScene(scene.Scene):
	def setup(self):
		self.background_color = 'gray'
		self.sprite = scene.SpriteNode(scene.Texture(myscene_shape_parameters.image),
		position=(self.size[0]/2, self.size[1]/2),
		size=self.size,
		#anchor_point=(.5,.5),
		parent=self)
		self.anchor_point = (.5, .5)
		
	def update(self):
		self.sprite.texture = scene.Texture(myscene_shape_parameters.image)
		
USE_PYUI_ENCODED_STRING = True
if USE_PYUI_ENCODED_STRING:
	pyui = bz2.decompress(b64decode(data))
	v = ui.load_view_str(pyui.decode('utf-8'))
else:
	# use decoded .pyui file
	v = ui.load_view()
	
cv = MyView()
frame1 = v['view1'].frame
cv.width = frame1.w
cv.height = frame1.h
cv.flex='WH'
v['view1'].add_subview(cv)
frame2 = v['view2'].frame
myscene_shape_parameters = ShapeParameters(size=(frame1.w, frame1.h))
scene_view = scene.SceneView()
scene_view.flex= 'WH'
scene_view.width = frame2.w
scene_view.height = frame2.h
scene_view.scene = MyScene()
v['view2'].add_subview(scene_view)
v.present('sheet')

