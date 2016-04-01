# -*- coding: utf-8 -*-
import os, sys, editor, shutil
from glob import glob
from scene import *
from time import time
from copy import deepcopy
from PIL import Image, ImageDraw, ImageFont

# https://gists.github.com/4034526


global EventQ

def p_click():
	print('Klick!')

def focus_true():
	return True 

class Event():
	def setup(self, msg_type,msg=None,obj=None):
		self.msg_type = msg_type
		self.msg = msg
		self.obj = obj
	
class Events():
	def __init__(self):
		self.listeners = []
	def add_listener(self, listener):
		self.listeners.append(listener)
	def remove_listener(self, listener):
		self.listeners.remove(listener)
	def pass_event(self, event):
		print event.msg_type
		for listener in self.listeners:
			listener(event)
		del event

class TextBuffer():
	def __init__(self, callback=None, got_focus=focus_true, font_size = 32.0):
		self.text = ''
		self.max_len = 50
		self.font_name = 'Helvetica'
		self.font_size = font_size
		self.text_img = None
		self.text_img_s = None
		self.type_callback = callback
		self.got_focus = got_focus
		self.color = Color(0,0,0)
	def input_char(self, char):
		if char=='backspace':
			self.text=self.text[:-1]
		elif char == 'return':
			pass
		elif len(self.text) < self.max_len:
			self.text += char
		if self.text_img:
			del self.text_img
			del self.text_img_s
		self.text_img, self.text_img_s = render_text(self.text, font_name=self.font_name, font_size=self.font_size)
		
		if self.type_callback:
			self.type_callback()
		
	def event_listener(self, e):
		if e.msg_type == 'KeyPress':
			self.input_char(e.msg)

class EmptyLayer(Layer):
	def __init__(self, frame):
		super(EmptyLayer, self).__init__(frame)
	def touch_began(self, touch):
		if self.superlayer:
			self.superlayer.touch_began(touch)
		
	def touch_ended(self, touch):
		if self.superlayer:
			self.superlayer.touch_ended(touch)
		
	def touch_moved(self, touch):
		if self.superlayer:
			self.superlayer.touch_moved(touch)

class ScrollLayer(Layer):
	def __init__(self, frame, sublayer, orientation_y = True):
		super(ScrollLayer, self).__init__(frame)
		self.orientation_y = orientation_y
		self.sub_layer = None
		self.stroke=Color(0,0,0)
		self.stroke_weight = 1
		self.set_layer(sublayer)
		self.cover1 = None 
		self.cover2 = None 
	def scrollTo(self, xy):
		if xy < 0:
			self.scrollTo(0)
		elif xy > self.scroll_range:
			self.scrollTo(self.scroll_range)
		else:
			self.scroll_pos = xy
			if self.orientation_y:
				self.sub_layer.frame.y = self.frame.h -self.sub_layer.frame.h + xy
			else:
				self.sub_layer.frame.x = self.frame.w -self.sub_layer.frame.w + xy
	def scrollBy(self, dy):
		self.scrollTo(self.scroll_pos + dy)
	def touch_moved(self, touch):
		if self.orientation_y:
			self.scrollBy((touch.location.y - touch.prev_location.y))
		else:
			self.scrollBy((touch.location.x - touch.prev_location.x))
	#	self.superlayer.touch_moved(touch)
	def set_layer(self, sublayer):
		if self.sub_layer:
			self.sub_layer.remove_layer()
		self.sub_layer = sublayer
		self.add_layer(self.sub_layer)
		# zero when upper left corners match
		if self.orientation_y:
			scroll_range = self.sub_layer.frame.h - self.frame.h
		else:
			scroll_range = self.sub_layer.frame.w - self.frame.w
		if scroll_range < 0: scroll_range = 0
		self.scroll_range = scroll_range
		self.scroll_pos = scroll_range
		
		if self.sub_layer.frame.h > self.frame.h or self.sub_layer.frame.w > self.frame.w:
			if self.orientation_y:
				self.cover1 = Layer(Rect(0, self.frame.h+1, self.frame.w, self.sub_layer.frame.h))
				self.cover2 = Layer(Rect(0, 0, self.frame.w, 0-self.sub_layer.frame.h))
			else:
				self.cover1 = Layer(Rect(0-1, 0, 0-self.sub_layer.frame.w, self.sub_layer.frame.h))
				self.cover2 = Layer(Rect(self.frame.w+1, 0, self.sub_layer.frame.w, self.sub_layer.frame.h))
			self.cover1.tint = Color(1,1,1)
			self.cover1.background = Color(0,0,0)
			self.add_layer(self.cover1)
			self.cover2.tint = Color(1,1,1)
			self.cover2.background = Color(0,0,0)
			self.add_layer(self.cover2)
			self.scrollTo(0)
	def touch_began(self, touch):
	#	self.superlayer.touch_began(touch)
		pass
	def touch_ended(self, touch):
	#	self.superlayer.touch_ended(touch)
		pass
	def event_listener(self, e):
		if e.msg_type == 'touch_moved':
			if self.frame.intersects(Rect(e.obj.location.x, e.obj.location.y, 1,1)):
				self.touch_moved(e.obj)
		elif e.msg_type == 'scroll_top':
			self.scrollTo(0)

class Textbox(ScrollLayer):
	def __init__(self, frame):
		super(Textbox, self).__init__(frame, Layer(Rect(0,0,1,1)), orientation_y = False)
		img = Image.new('RGBA',(int(frame.w),int(frame.h)), 'grey')
		draw = ImageDraw.Draw(img)
		draw.rectangle((1,1, frame.w-2, frame.h-2), outline=256)
		del draw
		self.il = load_pil_image(img)
		self.image = load_pil_image(img)
		self.txtbf = TextBuffer(self.load_new_text, self.got_focus)
		EventQ.add_listener(self.txtbf.event_listener)
		self.textlayer = Layer(Rect(0,0,10,10)) 
		self.focus = False
		self.last_touch = 0
		self.last_click = 0
	def got_focus(self):
		return self.focus
	def load_new_text(self):
		if self.textlayer:
			self.remove_layer(self.textlayer)
		self.textlayer = EmptyLayer(Rect(10,5,self.txtbf.text_img_s.w, self.txtbf.text_img_s.h))
		self.textlayer.tint = self.txtbf.color
		self.textlayer.image=self.txtbf.text_img
		self.set_layer(self.textlayer)
	def touch_ended(self, touch):
		if time() - self.last_touch < 0.2:
			# click
			if self.frame.intersects(Rect(touch.location.x, touch.location.y, 1,1)):
				if self.focus == False:
					self.focus = True
					e = Event()
					e.setup('input_focus','',self)
					EventQ.pass_event(e)
		self.superlayer.touch_ended(touch)
	def touch_began(self, touch):
		self.last_touch = time()
		self.superlayer.touch_began(touch)
	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click
		super(Textbox,self).touch_moved(touch)
		self.superlayer.touch_moved(touch)
			

class RootLayer(Layer):
	def __init__(self, the_scene, frame):
		super(RootLayer, self).__init__(frame)
		self.the_scene = the_scene
	def touch_began(self, touch):
		self.the_scene.touch_began(touch)
		
	def touch_ended(self, touch):
		self.the_scene.touch_ended(touch)
		
	def touch_moved(self, touch):
		self.the_scene.touch_moved(touch)

class KbdLayer(Layer):
	def __init__(self, frame, home):
		super(KbdLayer, self).__init__(frame)
		self.homedir = home
		self.row_rects = [[Rect(1, 159, 28, 38), Rect(33, 159, 28, 38), Rect(65, 159, 28, 38), Rect(97, 159, 28, 38), Rect(129, 159, 28, 38), Rect(161, 159, 28, 38), Rect(193, 159, 28, 38), Rect(225, 159, 28, 38), Rect(257, 159, 28, 38), Rect(289, 159, 28, 38)],[Rect(17, 107, 28, 38), Rect(49, 107, 28, 38), Rect(81, 107, 28, 38), Rect(113, 107, 28, 38), Rect(145, 107, 28, 38), Rect(177, 107, 28, 38), Rect(209, 107, 28, 38), Rect(241, 107, 28, 38), Rect(273, 107, 28, 38)],[Rect(1, 55, 37, 38), Rect(49, 55, 28, 38), Rect(81, 55, 28, 38), Rect(113, 55, 28, 38), Rect(145, 55, 28, 38), Rect(177, 55, 28, 38), Rect(209, 55, 28, 38), Rect(241, 55, 28, 38), Rect(281, 55, 37, 38)],[Rect(1, 2, 76, 38), Rect(81, 2, 158, 38), Rect(243, 2, 75, 38)]]
		self.n_row_rects = [[Rect(0, 157, 30, 40), Rect(32, 157, 30, 40), Rect(64, 157, 30, 40), Rect(96, 157, 30, 40), Rect(128, 157, 30, 40), Rect(160, 157, 30, 40), Rect(192, 157, 30, 40), Rect(224, 157, 30, 40), Rect(256, 157, 30, 40), Rect(288, 157, 30, 40)],[Rect(0, 105, 30, 40), Rect(32, 105, 30, 40), Rect(64, 105, 30, 40), Rect(96, 105, 30, 40), Rect(128, 105, 30, 40), Rect(160, 105, 30, 40), Rect(192, 105, 30, 40), Rect(224, 105, 30, 40), Rect(256, 105, 30, 40), Rect(288, 105, 30, 40)],[Rect(0, 53, 39, 40), Rect(56, 53, 40, 40), Rect(98, 53, 40, 40), Rect(140, 53, 40, 40), Rect(182, 53, 40, 40), Rect(224, 53, 40, 40), Rect(280, 53, 39, 40)],[Rect(0, 0, 78, 40), Rect(80, 0, 160, 40), Rect(242, 0, 77, 40)]]

		self.row_keys = []
		self.n_row_keys = []
		self.setup_keys()
		self.shift = False
		self.direct_input = None
		self.keyboard, self.kb_size = self.load_keyboard()
		self.num_keyboard, self.n_kb_size = self.load_num_keyboard()
		self.frame = Rect(self.frame.x, self.frame.y, 320, 245)
		self.background = Color(0, 0, 0)
		self.image = self.keyboard
		self.mode = 0 # 0: letters. 1: numbers
	def setup_keys(self):
		row1_keys = ['q','w','e','r','t','y','u','i','o','p']
		self.row_keys.append(row1_keys)
		row2_keys = ['a','s','d','f','g','h','j','k','l']
		self.row_keys.append(row2_keys)
		row3_keys = ['shift','z','x','c','v','b','n','m','backspace']
		self.row_keys.append(row3_keys)
		row4_keys = ['mode','space','return']
		self.row_keys.append(row4_keys)
		n_row1_keys = ['1','2','3','4','5','6','7','8','9','0']
		self.n_row_keys.append(n_row1_keys)
		n_row2_keys = ['-','/',':',';','(',')','$','&','@','"']
		self.n_row_keys.append(n_row2_keys)
		n_row3_keys = ['#+=','.',',','?','!',"'",'backspace']
		self.n_row_keys.append(n_row3_keys)
		n_row4_keys = ['mode','space','return']
		self.n_row_keys.append(n_row4_keys)
	def create_kbd(self):
		self.im = Image.new("RGBA", (320, 245), "black")
		il = ImageDraw.Draw(self.im)
		font = ImageFont.truetype("Helvetica", 24)
		i = 0
		while i < len(self.row_rects):
			n = 0
			while n < len(self.row_rects[i]):
				t = self.row_keys[i][n]
				if t == 'shift':
					t = '^'
				elif t == 'backspace':
					t = '<=]'
				elif t == 'mode':
					t = '123'
				elif t == 'backspace':
					t = 'space'
				s = il.textsize(t, font=font)
				dx = (self.row_rects[i][n].w-s[0])/2
				dy = (self.row_rects[i][n].h-s[1])/2
				il.rectangle([(self.row_rects[i][n].x, 200- self.row_rects[i][n].y), (self.row_rects[i][n].x+self.row_rects[i][n].w, 200- self.row_rects[i][n].y+self.row_rects[i][n].h)], outline=(256,0,0), fill=(0,0,0))
				il.text((self.row_rects[i][n].x +dx, 200- self.row_rects[i][n].y+dy), t, font=font, fill=(256,256,256))
				n += 1
			i += 1
		del il
		self.i=load_pil_image(self.im)
		self.im.save('kbd.png', "PNG")
	def create_nkbd(self):
		self.nim = Image.new("RGBA", (320, 245), "black")
		il = ImageDraw.Draw(self.nim)
		font = ImageFont.truetype("Helvetica", 24)
		i = 0
		while i < len(self.n_row_rects):
			n = 0
			while n < len(self.n_row_rects[i]):
				t = self.n_row_keys[i][n]
				if t == 'backspace':
					t = '<=]'
				elif t == 'mode':
					t = 'ABC'
				elif t == 'backspace':
					t = 'space'
				s = il.textsize(t, font=font)
				dx = (self.n_row_rects[i][n].w-s[0])/2
				dy = (self.n_row_rects[i][n].h-s[1])/2
				il.rectangle([(self.n_row_rects[i][n].x, 200- self.n_row_rects[i][n].y), (self.n_row_rects[i][n].x+self.n_row_rects[i][n].w, 200- self.n_row_rects[i][n].y+self.n_row_rects[i][n].h)], outline=(256,0,0), fill=(0,0,0))
				il.text((self.n_row_rects[i][n].x +dx, 200- self.n_row_rects[i][n].y+dy), t, font=font, fill=(256,256,256))
				n += 1
			i += 1
		del il
		self.ni=load_pil_image(self.nim)
		self.nim.save('nkbd.png', "PNG")
	def load_keyboard(self):
		kb_filename = "kbd.png"
		if os.path.isfile(kb_filename):
			kb_image = load_image_file(kb_filename)
			return [kb_image, Image.open(kb_filename).size]
		else:
			self.create_kbd()
			return self.load_keyboard()
	def load_num_keyboard(self):
		kb_filename = "nkbd.png"
		if os.path.isfile(kb_filename):
			kb_image = load_image_file(kb_filename)
			return [kb_image, Image.open(kb_filename).size]
		else:
			self.create_nkbd()
			return self.load_num_keyboard()
	def touch_began(self, touch):
		self.last_touch = time()
		r = None
		char = ''
		if self.mode == 0: # The alfabetical keyboard
			if touch.location.y > 156:
				i = int(touch.location.x / 32)
				r = self.row_rects[0][i]
				char = self.row_keys[0][i]
			elif touch.location.y > 104 and touch.location.y < 146:
				i = int((touch.location.x - 16)/ 32)
				if i > -1 and i < 9:
					r = self.row_rects[1][i]
					char = self.row_keys[1][i]
			elif touch.location.y > 52 and touch.location.y < 93:
				if touch.location.x < 41:
					r = self.row_rects[2][0]
					char = self.row_keys[2][0]
				elif touch.location.x > 280:
					r = self.row_rects[2][8]
					char = self.row_keys[2][8]
				else:
					i = int((touch.location.x - 48)/ 32)
					if i > -1 and i < 8:
						r = self.row_rects[2][i]
						char = self.row_keys[2][i]
			elif touch.location.y < 41:
				if touch.location.x < 79:
					r = self.row_rects[3][0]
					char = self.row_keys[3][0]
				elif touch.location.x < 240:
					r = self.row_rects[3][1]
					char = self.row_keys[3][1]
				else: 
					r = self.row_rects[3][2]
					char = self.row_keys[3][2]
		elif self.mode == 1: # Numerical keyboard
			if touch.location.y > 156:
				i = int(touch.location.x / 32)
				r = self.n_row_rects[0][i]
				char = self.row_keys[0][i]
			elif touch.location.y > 104 and touch.location.y < 146:
				i = int(touch.location.x / 32)
				r = self.n_row_rects[1][i]
				char = self.row_keys[1][i]
			elif touch.location.y > 52 and touch.location.y < 93:
				if touch.location.x < 41:
					r = self.n_row_rects[2][0] # The advanced keyboard, to be implemented
					char = self.row_keys[2][0]
				elif touch.location.x > 280:
					r = self.n_row_rects[2][6]
					char = self.row_keys[2][6]
				else:
					i = int((touch.location.x - 56)/ 40) + 1
					if i > -1 and i < 6:
						r = self.n_row_rects[2][i]
						char = self.row_keys[2][i]
			elif touch.location.y < 41:
				if touch.location.x < 79:
					r = self.n_row_rects[3][0]
					char = self.row_keys[3][0]
				elif touch.location.x < 240:
					r = self.n_row_rects[3][1]
					char = self.row_keys[3][1]
				else: 
					r = self.n_row_rects[3][2]
					char = self.row_keys[3][2]
		if r:
			self.highlight = EmptyLayer(Rect(r.x,r.y,r.w,r.h+60))
			l, s = render_text(char, font_size=32.0)
			self.high_letter = EmptyLayer(Rect((r.w-s.w)/2,r.h+60-s.h,s.w,s.h))
			self.high_letter.tint = Color(0,0,0)
			self.high_letter.image = l
			self.highlight.background = Color(1,1,1, 0.75)
			self.highlight.add_layer(self.high_letter)
			self.add_layer(self.highlight)
		self.superlayer.touch_began(touch)
		
	def touch_ended(self, touch):
		if self.highlight:
			self.remove_layer(self.highlight)
		if time() - self.last_touch < 0.2:
			char = ''
			if self.mode == 0: # The alfabetical keyboard
				if touch.location.y > 156:
					i = int(touch.location.x / 32)
					char = self.row_keys[0][i]
					if self.shift:
						char= char.upper()
						self.shift = False 
				elif touch.location.y > 104 and touch.location.y < 146:
					i = int((touch.location.x - 16)/ 32)
					if i > -1 and i < 9:
						char = self.row_keys[1][i]
						if self.shift:
							char= char.upper()
							self.shift = False 
				elif touch.location.y > 52 and touch.location.y < 93:
					if touch.location.x < 41:
						if self.shift:
							self.shift = False
						else:
							self.shift = True
						pass
					elif touch.location.x > 280:
						char = 'backspace'
					else:
						i = int((touch.location.x - 48)/ 32)
						if i > -1 and i < 8:
							char = self.row_keys[2][i]
							if self.shift:
								char= char.upper()
								self.shift = False 
				elif touch.location.y < 41:
					if touch.location.x < 79:
						self.mode = 1
						self.image = self.num_keyboard
					elif touch.location.x < 240:
						char = ' '
					else: 
						char = 'return'
			elif self.mode == 1: # Numerical keyboard
				if touch.location.y > 156:
					i = int(touch.location.x / 32)
					char = self.n_row_keys[0][i]
				elif touch.location.y > 104 and touch.location.y < 146:
					i = int(touch.location.x / 32)
					char = self.n_row_keys[1][i]
				elif touch.location.y > 52 and touch.location.y < 93:
					if touch.location.x < 41:
						pass # The advanced keyboard, to be implemented
					elif touch.location.x > 280:
						char = 'backspace'
					else:
						i = int((touch.location.x - 56)/ 40) + 1
						if i > -1 and i < 6:
							char = self.n_row_keys[2][i]
				elif touch.location.y < 41:
					if touch.location.x < 79:
						self.mode = 0
						self.image = self.keyboard
					elif touch.location.x < 240:
						char = ' '
					else: 
						char = 'return'

			if len(char) > 0:
				if self.direct_input:
					self.direct_input(char)
				else:
					e = Event()
					e.setup('KeyPress', char)
					EventQ.pass_event(e)
		self.superlayer.touch_ended(touch)
	def touch_moved(self, touch):
		if self.highlight:
			self.remove_layer(self.highlight)
		self.superlayer.touch_moved(touch)

class ListItem(EmptyLayer):
	def __init__(self, frame, text, kind, edit_mode, text_color = Color(1,1,1), count_callback = None, listname=None):
		super(ListItem, self).__init__(frame)
		self.listname = listname
		self.background = Color(0,0,0)
		self.text_color = text_color
		self.txtbf = TextBuffer(got_focus=False, font_size = 24.0)
		self.txtbf.text = text
		self.txtbf.input_char('')
		self.edit_mode = edit_mode
		self.edit_icon = 'White_Square'
		self.count_callback = count_callback 
		self.unselected_layer = EmptyLayer(Rect(0,0,40,40))
		self.unselected_layer.image = self.edit_icon
		self.edit_icon_selected = 'Checkmark_1'
		self.selected_layer = EmptyLayer(Rect(0,0,40,40))
		self.selected_layer.image = self.edit_icon_selected
		if self.edit_mode and self.txtbf.text != '..':
			self.e_margin = 45
			self.add_layer(self.unselected_layer)
		else:
			self.e_margin = 0
		self.textlayer = ()
		self.type = kind
		if self.type:
			self.icon = 'Page_Facing_Up'
		else:
			self.icon = 'Books'
			self.folder_icon_layer = EmptyLayer(Rect(self.frame.w-self.frame.h-2,0, self.frame.h, self.frame.h))
			self.folder_icon_layer.image = 'Typicons48_Next'
			self.folder_icon_layer.background = Color(0,0,0)
			self.add_layer(self.folder_icon_layer)
		self.icon_layer = EmptyLayer(Rect(self.e_margin,0, self.frame.h, self.frame.h))
		self.icon_layer.image = self.icon
		self.selected = False
		self.txtbf = TextBuffer(got_focus=False, font_size = 24.0)
		self.txtbf.text = text
		self.txtbf.input_char('')
		dy = (self.frame.h-self.txtbf.text_img_s.h)/2
		self.textlayer = EmptyLayer(Rect(self.e_margin+self.frame.h,dy,self.txtbf.text_img_s.w, self.txtbf.text_img_s.h))
		self.textlayer.tint = self.text_color
		self.textlayer.image=self.txtbf.text_img
		self.add_layer(self.icon_layer)
		self.add_layer(self.textlayer)
	def toggle_edit(self, edit_mode=False):
		if self.edit_mode == edit_mode:
			pass
		elif edit_mode == True:
			self.add_layer(self.unselected_layer)
		else:
			self.remove_layer(self.unselected_layer)
			if self.selected:
				self.remove_layer(self.selected_layer)
			self.edit_mode = False
			self.selected = False
	def toggle_selection(self):
		change = 0
		if self.selected:
			self.selected = False
			self.remove_layer(self.selected_layer)
			change = -1
		else:
			self.selected = True 
			self.add_layer(self.selected_layer)
			change = 1
		if self.count_callback:
			self.count_callback(change)
	def touch_ended(self, touch):
		if time() - self.last_touch < 0.2:
			# click
			if self.edit_mode == False:
				e = Event()
				e.setup('fs_open', self.txtbf.text, self.listname)
				EventQ.pass_event(e)
			elif self.txtbf.text != '..':
				self.toggle_selection()
		self.superlayer.touch_ended(touch)
	def touch_began(self, touch):
		self.last_touch = time()
		self.superlayer.touch_began(touch)
	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click
		self.superlayer.touch_moved(touch)

class List(ScrollLayer):
	def __init__(self, frame, edit_mode = False, name = None):
		super(List, self).__init__(frame, Layer(Rect(0,0,10,10)))
		self.name = name
		self.edit_mode = edit_mode
		self.list = []
		self.items = []
		self.list_layer = None 
		self.selected_count = 0
	def set_list(self, list):
		self.items = []
		self.selected_count = 0
		self.list = list
		w = self.frame.w
		margin = 1
		h = 40
		lh = (margin+1)*len(list)+h*(len(list))
		if lh < self.frame.h:
			lh = self.frame.h
		y = lh - h - margin
		ly = self.frame.h - (margin+1)*len(list)+h*(len(list))
		if ly <  0:
			ly == 0
		self.list_layer = EmptyLayer(Rect(0,0,w,lh))
		self.list_layer.background = Color(0.5,0.5,0.5)
		self.list_layer.edit_mode = self.edit_mode
		#self.list_layer.background = Color(0,1,0)
		for item in self.list:
			it = ListItem(Rect(0,y,w,h), item[0], item[1], self.edit_mode,count_callback = self.count_callback, listname=self.name)
			self.items.append(it)
			self.list_layer.add_layer(it)
			y -= h + margin
		self.set_layer(self.list_layer)
	def count_callback(self, change):
		self.selected_count += change
		e = Event()
		e.setup('edit_mode_selected_count', '%s' % self.selected_count)
		EventQ.pass_event(e)
			

# Thx wrenoud! :)
class filesystem:
	def __init__(self, cwd ='.'):
		self.cwd = cwd
		self.chdir(cwd)
		self.home = self.cwd
		
	def chdir(self,path):
		# see if its an absolute path
		if path.startswith('/'):
			self.cwd = path
		# it's probably a relative path,
		# let's append cwd and let os.path do its magic
		else:
			self.cwd = os.path.abspath(os.path.join(self.cwd,path))
		entries = os.listdir(self.cwd)
		self.dirs = []
		self.files = []
		self.dirs.append(['..', False])
		for entry in entries:
			if os.path.isdir(self.cwd+'/'+entry):
				self.dirs.append([entry, False])
			else:
				self.files.append([entry, True])
		
	def getcwd(self):
		return self.cwd
		
	def getdirs(self):
		return self.dirs
		
	def getfiles(self):
		return self.files
	
	def listfile(self):
		return
		
	def isdir(self, path):
		return os.path.isdir(path)
		
	def isfile(self, path):
		return os.path.isfile(path)

class ToolbarItem(EmptyLayer):
	def __init__(self, frame, kind, alignment):
		super(ToolbarItem, self).__init__(frame)
		self.alignment = alignment
		self.kind = kind
		if kind == 'fs_add_button':
			self.image = 'Typicons48_Plus'
		elif kind == 'edit_mode_button':
			self.image = 'Typicons48_Export'
		elif kind == 'fs_statusbar':
			self.set_status('Checking items')
	def set_status(self, status = 'Checking items'):
		if self.sublayers:
			del self.sublayers[0]
		self.txtobj = TextBuffer(font_size=20.0)
		self.txtobj.text = status
		self.txtobj.input_char('')
		dx = (self.frame.w - self.txtobj.text_img_s.w) / 2
		dy = (self.frame.h - self.txtobj.text_img_s.h) / 2
		self.textlayer = EmptyLayer(Rect(dx, dy, self.txtobj.text_img_s.w, self.txtobj.text_img_s.h))
		self.textlayer.tint = Color(1,1,1)
		self.textlayer.image = self.txtobj.text_img
		self.add_layer(self.textlayer)
	def touch_ended(self, touch):
		if time() - self.last_touch < 0.2:
			# click
			if self.kind == 'fs_statusbar':
				e = Event()
				e.setup('scroll_top')
				EventQ.pass_event(e)
			elif self.kind == 'fs_add_button':
				e = Event()
				e.setup('fs_add_button')
				EventQ.pass_event(e)
			elif self.kind == 'edit_mode_button':
				e = Event()
				e.setup('toggle_edit_mode')
				EventQ.pass_event(e)
		self.superlayer.touch_ended(touch)
	def touch_began(self, touch):
		self.last_touch = time()
		self.superlayer.touch_began(touch)
	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click
		self.superlayer.touch_moved(touch)
		

class Toolbar(EmptyLayer):
	def __init__(self, frame):
		super(Toolbar, self).__init__(frame)
		self.objects = []
	def add_object(self, kind, alignment=1):
		# alignment;	1 left
		#							2 center
		#							3 right
		if kind == 'fs_statusbar':
			w = 130
		else:
			w = self.frame.h
		x = 0
		if alignment == 1:
			for o in self.objects:
				if o.alignment == 1:
					x += o.frame.w + 1
		elif alignment == 2:
			if x == 0:
				x = self.frame.w/2 - w/2
			for o in self.objects:
				if o.alignment == 2:
					x += o.frame.w + 1
		else: # alignment == 3
			x = self.frame.w - w
			for o in self.objects:
				if o.alignment == 3:
					x -= (o.frame.w + 1)
		obj = ToolbarItem(Rect(x, 0, w, self.frame.h), kind, alignment)
		self.objects.append(obj)
		self.add_layer(obj)

class Button(EmptyLayer):
	def __init__(self, frame, text='Ok', on_click = None, icon = None, align=1,font_size = 32.0, foreground = Color(0,0,0), name = None):
		super(Button, self).__init__(frame)
		self.name = name
		self.on_click = on_click
		self.icon = icon
		self.icon_w = 10
		self.icon_layer = EmptyLayer(Rect(1,1,self.frame.h-2,self.frame.h-2))
		if self.icon != None:
			self.icon_w = frame.h
			self.icon_layer.image = self.icon
		self.align = align
		self.txtbuf = TextBuffer(font_size=font_size)
		self.txtbuf.text = text
		self.txtbuf.input_char('')
		w = self.txtbuf.text_img_s.w
		h = self.txtbuf.text_img_s.h
		x = self.icon_w #(self.frame.w - w)/2
		y = (self.frame.h - h)/2
		if align == 2:
			x = (self.frame.w - w)/2
		self.text_layer = EmptyLayer(Rect(x,y,w,h))
		self.text_layer.tint = Color(1,1,1,1)
		self.text_layer.image = self.txtbuf.text_img
		self.tint = Color(1,1,1,1)
		self.background = Color(1,1,1,1)
		self.foreground = foreground
		self.fg_layer = EmptyLayer(Rect(1,1,self.frame.w-2, self.frame.h - 2))
		self.fg_layer.background = self.foreground
		self.add_layer(self.fg_layer)
		self.add_layer(self.text_layer)
		if self.icon:
			self.add_layer(self.icon_layer)
	def update_text(self, text):
		if self.text_layer:
			self.remove_layer(self.text_layer)
		self.txtbuf.text = text
		self.txtbuf.input_char('')
		w = self.txtbuf.text_img_s.w
		h = self.txtbuf.text_img_s.h
		x = self.icon_w #(self.frame.w - w)/2
		y = (self.frame.h - h)/2
		if self.align == 2:
			x = (self.frame.w - w)/2
		self.text_layer = EmptyLayer(Rect(x,y,w,h))
		self.text_layer.tint = Color(1,1,1,1)
		self.text_layer.image = self.txtbuf.text_img
		self.add_layer(self.text_layer)
	def touch_ended(self, touch):
		self.fg_layer.background = self.foreground
		self.text_layer.tint = Color(1,1,1)
		if time() - self.last_touch < 0.2:
			# click
			if self.on_click:
				self.on_click()
			elif self.name:
				e = Event()
				e.setup('%s_clicked' % self.name)
				EventQ.pass_event(e)

	def touch_began(self, touch):
		self.last_touch = time()
		self.fg_layer.background = Color(1,1,1)
		self.text_layer.tint = Color(0,0,0)

	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click
		self.fg_layer.background = self.foreground
		self.text_layer.tint = Color(1,1,1)

class NewFileView(Layer):
	def __init__(self, bounds,frame,fs):
		super(NewFileView, self).__init__(bounds)
		self.fs = fs
		self.view_layer = EmptyLayer(frame)
		self.view_layer.background = Color(0,0,0,0.5)
		self.add_layer(self.view_layer)
		self.filename = ''
		self.btn_file = Button(Rect(160-125,70,250,50), on_click=self.new_file, text='New Fileâ€¦', icon = 'Typicons48_Write')
		self.view_layer.add_layer(self.btn_file)
		self.btn_folder = Button(Rect(160-125,10,250,50), on_click=self.new_folder, text='New Folderâ€¦', icon = 'Typicons48_Calendar')
		self.view_layer.add_layer(self.btn_folder)
	def new_folder(self):
		self.view_layer.remove_layer(self.btn_file)
		self.view_layer.remove_layer(self.btn_folder)
		self.filename_bf = TextBuffer(font_size=24.0)
		self.filename_bf.text = 'Filename:'
		self.filename_bf.input_char('')
		self.new_file_txt_layer = EmptyLayer(Rect((self.view_layer.frame.w-self.filename_bf.text_img_s.w)/2, self.view_layer.frame.h-self.filename_bf.text_img_s.h, self.filename_bf.text_img_s.w, self.filename_bf.text_img_s.h))
		self.new_file_txt_layer.tint = Color(1,1,1)
		self.new_file_txt_layer.image = self.filename_bf.text_img
		self.view_layer.add_layer(self.new_file_txt_layer)
		self.txtbf = Textbox(Rect(0, self.view_layer.frame.h-self.filename_bf.text_img_s.h-55, self.frame.w, 50))
		self.txtbf.focus=True 
		self.view_layer.add_layer(self.txtbf)
		
		self.btn_n_folder = Button(Rect(160-125,self.view_layer.frame.h-self.filename_bf.text_img_s.h-110,250,50), on_click=self.create_new_folder, text='Create', align=2)
		self.view_layer.add_layer(self.btn_n_folder)
		e = Event()
		e.setup('input_focus',obj = self)
		EventQ.pass_event(e)
	def create_new_folder(self):
		if len(self.txtbf.txtbf.text) > 0:
			os.mkdir(self.txtbf.txtbf.text)
		e = Event()
		e.setup('quit_new_file_view')
		EventQ.pass_event(e)
	def create_new_file_e(self):
		if len(self.txtbf.txtbf.text) > 0:
			path = self.fs.getcwd() + '/' + self.txtbf.txtbf.text
			f = open(path, 'w')
			f.write("""import os, sys

sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')]

""")
			f.close()
			editor.open_file(os.path.relpath(path))
			sys.exit()
	def create_new_file_b(self):
		content = """from scene import *
import os, sys

sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')]

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		pass
	
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		# Draw a red circle for every finger that touches the screen:
		fill(1, 0, 0)
		for touch in self.touches.values():
			ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

run(MyScene())
"""
		if len(self.txtbf.txtbf.text) > 0:
			f = open(self.txtbf.txtbf.text, 'w')
			f.write(content)
			f.close()
			editor.open_file(self.txtbf.txtbf.text)
			#sys.exit()
	def create_new_file_l(self):
		content = """from scene import *
from random import random
import os, sys

sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')]

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		# Set up the root layer and one other layer:
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()
		self.layer = Layer(Rect(center.x - 64, center.y - 64, 128, 128))
		self.layer.background = Color(1, 0, 0)
		self.layer.image = 'Snake'
		self.root_layer.add_layer(self.layer)
	
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0, 0, 0)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
	
	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
		x, y = touch.location.x, touch.location.y
		new_frame = Rect(x - 64, y - 64, 128, 128)
		self.layer.animate('frame', new_frame, 1.0, curve=curve_bounce_out)
		# Animate the background color to a random color:
		new_color = Color(random(), random(), random())
		self.layer.animate('background', new_color, 1.0)
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

run(MyScene())
"""
		if len(self.txtbf.txtbf.text) > 0:
			f = open(self.txtbf.txtbf.text, 'w')
			f.write(content)
			f.close()
			editor.open_file(self.txtbf.txtbf.text)
			#sys.exit()
	def new_file(self):
		self.view_layer.remove_layer(self.btn_file)
		self.view_layer.remove_layer(self.btn_folder)
		self.filename_bf = TextBuffer(font_size=24.0)
		self.filename_bf.text = 'Filename:'
		self.filename_bf.input_char('')
		self.new_file_txt_layer = EmptyLayer(Rect((self.view_layer.frame.w-self.filename_bf.text_img_s.w)/2, self.view_layer.frame.h-self.filename_bf.text_img_s.h, self.filename_bf.text_img_s.w, self.filename_bf.text_img_s.h))
		self.new_file_txt_layer.tint = Color(1,1,1)
		self.new_file_txt_layer.image = self.filename_bf.text_img
		self.view_layer.add_layer(self.new_file_txt_layer)
		self.txtbf = Textbox(Rect(0, self.view_layer.frame.h-self.filename_bf.text_img_s.h-55, self.frame.w, 50))
		self.txtbf.focus=True 
		self.view_layer.add_layer(self.txtbf)
		
		self.btn_n_empty = Button(Rect(160-125,self.view_layer.frame.h-self.filename_bf.text_img_s.h-110,250,50), on_click=self.create_new_file_e, text='Empty', align=2)
		self.btn_n_basic = Button(Rect(160-125,self.view_layer.frame.h-self.filename_bf.text_img_s.h-170,250,50), on_click=self.create_new_file_b, text='Basic Scene', align=2)
		self.btn_n_layers = Button(Rect(160-125,self.view_layer.frame.h-self.filename_bf.text_img_s.h-230,250,50), on_click=self.create_new_file_l, text='Scene with Layers', align=2, font_size=24.0)
		
		self.view_layer.add_layer(self.btn_n_empty)
		self.view_layer.add_layer(self.btn_n_basic)
		self.view_layer.add_layer(self.btn_n_layers)
		e = Event()
		e.setup('input_focus', obj = self)
		EventQ.pass_event(e)
	def touch_ended(self, touch):
		if time() - self.last_touch < 0.2:
			# click
			if touch.location.y < self.view_layer.frame.y and touch.location.y > 240:
				e = Event()
				e.setup('quit_new_file_view')
				EventQ.pass_event(e)

	def touch_began(self, touch):
		self.last_touch = time()

	def touch_moved(self, touch):
		self.last_touch = 0 # cancel click

class ConfirmDialogue(Layer):
	def __init__(self, question, btn_text, bounds, frame, background):
		super(ConfirmDialogue, self).__init__(bounds)
		self.yes = False
		self.confirmation_dialogue = EmptyLayer(frame)
		self.confirmation_dialogue.background = background
		self.confirm_button = Button(Rect((frame.w-220)/2,5,220,30),text=btn_text,font_size=16.0,foreground=Color(0,0,0,1), on_click=self.confirm_move_delete, align=2)
		self.confirmation_dialogue.add_layer(self.confirm_button)
	def ask(self):
		self.add_layer(self.confirmation_dialogue)
	def confirm_move_delete(self):
		self.yes = False
	def touch_ended(self, touch):
		pass
	def touch_began(self, touch):
		pass
	def touch_moved(self, touch):
		pass


class MoveDialogue(Layer):
	def __init__(self, bounds, cwd):
		super(MoveDialogue, self).__init__(bounds)
		self.bounds = bounds
		self.cwd = cwd
		h = int(self.bounds.h*0.75)
		m_y = int((self.bounds.h-self.bounds.h*0.75)/2)
		self.view_frame = Layer(Rect(0, 0, self.bounds.w, self.bounds.h))
		self.view_frame.background = Color(0,0,0,0.75)
		self.move_list = List(Rect((self.bounds.w-250)/2, 45, 250, self.bounds.h-45), name='move_list')
		self.fs = filesystem(self.cwd)
		self.move_list.set_list(self.fs.dirs + self.fs.files)
		self.move_button = Button(Rect(35, 5, 120, 35),text='Move here',font_size=16.0,foreground=Color(0,0,1,1), name='move_files_here', align=2)
		self.cancel_move_button = Button(Rect(165, 5, 120, 35),text='Cancel',font_size=16.0,foreground=Color(0.5,0.5,0.5,1), name='cancel_move_files_here', align=2)
		self.view_frame.add_layer(self.move_list)
		self.view_frame.add_layer(self.move_button)
		self.view_frame.add_layer(self.cancel_move_button)
		self.add_layer(self.view_frame)

class EditModeButtons(Layer):
	def __init__(self, frame, cwd=None):
		self.cwd = cwd
		super(EditModeButtons, self).__init__(frame)
		self.selected_count = 0
		self.background = Color(0,0,0,1)
		self.move_button = Button(Rect(50,5,100,30),text='Move (0)',font_size=16.0,foreground=Color(0,0,1,1), name='move_button')
		self.delete_button = Button(Rect(170,5,100,30),text='Delete (0)',font_size=16.0,foreground=Color(1,0,0,1), on_click=self.delete_btn_click)
		self.add_layer(self.move_button)
		self.add_layer(self.delete_button)
		self.mv_rm_confirmed = False
	def change_count(self, text):
		self.move_button.update_text('Move (%s)' % text)
		self.delete_button.update_text('Delete (%s)' % text)
	def event_listener(self, e):
		if e.msg_type == 'edit_mode_selected_count':
			self.selected_count = e.msg
			self.change_count(e.msg)
		elif e.msg_type == 'confirm_delete_clicked':
			self.remove_layer(self.confirmation_dialogue)
			self.confirmation_dialogue = None
	def delete_btn_click(self):
		self.confirm_delete()
	def confirm_delete(self):
		self.confirmation_dialogue = Layer(Rect(0,0,self.frame.w,40))
		self.confirmation_dialogue.background = Color(1,0,0,1)
		btn_text = 'Delete %s file(s)!' % self.selected_count
		self.confirm_button = Button(Rect(50,5,220,30),text=btn_text,font_size=16.0,foreground=Color(0,0,0,1), name='confirm_delete', align=2)
		self.confirmation_dialogue.add_layer(self.confirm_button)
		self.add_layer(self.confirmation_dialogue)
		

class MyScene (Scene):
	def setup(self):
		self.edit_mode = False 
		self.touch_start_t = -1
		self.touch_start = Touch(0,0,0,0,0)
		self.hold_timeout = 0
		self.root_layer = RootLayer(self, self.bounds)
		center = self.bounds.center()
		self.fs = filesystem()
		self.kbd_visible = False  
		self.klayer = KbdLayer(Rect(0, 0, 1,1),self.fs.home)
		self.input_focus = None 
		self.new_file_dialog = False
		self.listname = 'main_list'
		self.list = List(Rect(0,0,self.bounds.w,self.bounds.h-40), name = self.listname)
		self.list.set_list(self.fs.dirs + self.fs.files)
		self.root_layer.add_layer(self.list)
		self.toolbar = Toolbar(Rect(0, self.bounds.h-40, self.bounds.w, 40))
		self.toolbar.add_object('fs_add_button')
		self.toolbar.add_object('edit_mode_button')
		self.toolbar.add_object('fs_statusbar', 2)
		self.toolbar.objects[2].set_status('%i files' % len(self.fs.dirs + self.fs.files))
		self.root_layer.add_layer(self.toolbar)
		#self.root_layer.add_layer(self.klayer)
		#self.tbox = Textbox(Rect(self.bounds.w/2-125,self.bounds.h*.75-25,250,50))
		#self.root_layer.add_layer(self.tbox)
		EventQ.add_listener(self.list.event_listener)
		EventQ.add_listener(self.event_listener)
		
	def event_listener(self, e):
		if e.msg_type == 'show_keyboard':
			if self.kbd_visible == False:
				self.kbd_visible = True
				self.root_layer.add_layer(self.klayer)
		elif e.msg_type == 'hide_keyboard':
			if self.kbd_visible == True:
				self.root_layer.remove_layer(self.klayer)
				self.kbd_visible = False
		elif e.msg_type == 'input_focus':
			self.input_focus = e.obj
			if self.kbd_visible == False:
				self.kbd_visible = True
				self.root_layer.add_layer(self.klayer)
			e.obj.txtbf.got_focus = True
			self.klayer.direct_input = e.obj.txtbf.txtbf.input_char
		elif e.msg_type == 'fs_open':
			print e.obj
			if type(e.obj) == None or e.obj == 'main_list':
				for item in self.fs.dirs:
					if item[0] == e.msg or e.msg == '..':
						self.fs.chdir(e.msg)
						self.list.set_list(self.fs.dirs + self.fs.files)
						self.toolbar.objects[2].set_status('%i files' % len(self.fs.dirs + self.fs.files))
						return
				editor.open_file(os.path.relpath(self.fs.cwd + '/' + e.msg))
				sys.exit()
			elif e.obj == 'move_list':
				for item in self.move_dialogue.fs.dirs:
					if item[0] == e.msg or e.msg == '..':
						self.move_dialogue.fs.chdir(e.msg)
						self.move_dialogue.move_list.set_list(self.move_dialogue.fs.dirs + self.move_dialogue.fs.files)
		elif e.msg_type == 'fs_add_button':
			self.new_file_dialog = True
			self.new_file_view = NewFileView(self.bounds, Rect(0,self.bounds.h-250,self.bounds.w,250), self.fs)
			self.root_layer.add_layer(self.new_file_view)
		elif e.msg_type == 'toggle_edit_mode':
			if self.edit_mode:
				self.edit_mode = False 
				self.root_layer.remove_layer(self.edit_mode_buttons)
				EventQ.remove_listener(self.edit_mode_buttons.event_listener)
			else:
				self.edit_mode = True
				self.edit_mode_buttons = EditModeButtons(Rect(0, self.bounds.h-80, self.bounds.w, 40), cwd = self.fs.cwd)
				self.root_layer.add_layer(self.edit_mode_buttons)
				EventQ.add_listener(self.edit_mode_buttons.event_listener)
			self.list.edit_mode = self.edit_mode
			self.list.set_list(self.fs.dirs + self.fs.files)
		elif e.msg_type == 'confirm_delete_clicked':
			file_items = []
			dir_items = []
			for item in self.list.items:
				if item.selected:
					if item.type:
						file_items.append(item.txtbf.text)
					else:
						dir_items.append(item.txtbf.text)
			if len(file_items) > 0:
				for item in file_items:
					os.remove(self.fs.cwd + '/' + item)
			if len(dir_items) > 0:
				for item in dir_items:
					os.removedirs(self.fs.cwd + '/' + item)
			self.fs.chdir('.')
			self.list.set_list(self.fs.dirs + self.fs.files)
			self.toolbar.objects[2].set_status('%i files' % len(self.fs.dirs + self.fs.files))
			e = Event()
			e.setup('toggle_edit_mode')
			EventQ.pass_event(e)
		elif e.msg_type == 'move_button_clicked':
			self.move_dialogue = MoveDialogue(self.bounds, self.fs.cwd)
			self.root_layer.add_layer(self.move_dialogue)
		elif e.msg_type == 'cancel_move_files_here_clicked':
			self.root_layer.remove_layer(self.move_dialogue)
		elif e.msg_type == 'move_files_here_clicked':
			file_items = []
			for item in self.list.items:
				if item.selected:
					file_items.append(item.txtbf.text)
			if len(file_items) > 0:
				for item in file_items:
					shutil.move(self.fs.cwd + '/' + item, self.move_dialogue.fs.cwd + '/' + item)
			self.fs.chdir('.')
			self.list.set_list(self.fs.dirs + self.fs.files)
			self.toolbar.objects[2].set_status('%i files' % len(self.fs.dirs + self.fs.files))
			self.root_layer.remove_layer(self.move_dialogue)
			e = Event()
			e.setup('toggle_edit_mode')
			EventQ.pass_event(e)
		elif e.msg_type == 'quit_new_file_view':
			self.new_file_dialog = False
			self.root_layer.remove_layer(self.new_file_view)
			if self.kbd_visible == True:
				self.root_layer.remove_layer(self.klayer)
				self.kbd_visible = False
			self.fs.chdir('.')
			self.list.set_list(self.fs.dirs + self.fs.files)
			self.toolbar.objects[2].set_status('%i files' % len(self.fs.dirs + self.fs.files))
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0, 0, 0)
		stroke(1,0,0)
		stroke_weight(1)
		self.root_layer.update(self.dt)
		self.root_layer.draw()
	def touch_began(self, touch):
		self.touch_start = touch
		self.touch_start_t = self.t
	def touch_moved(self, touch):
		pass
	def touch_ended(self, touch):
		if self.input_focus:

			if touch.location in self.input_focus.frame or touch.location in self.klayer.frame:
				pass
			else:
				self.input_focus.focus = False 
				self.input_focus = None 
				self.klayer.direct_input = None
				if self.kbd_visible == True:
					self.root_layer.remove_layer(self.klayer)
					self.kbd_visible = False
		

EventQ = Events()
run(MyScene())
