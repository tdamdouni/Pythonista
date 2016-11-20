# coding: utf-8

# Version 10/03/2016

# https://github.com/humberry/DrawOnImage

# Please be patient after pressing the save button, because several tasks have to be done (ui2png, png2alpha, paste background and overlay). Closing automatically after processing.
# You can't use a black path because it's the png background color. Any suggestions?

import ui, os, sys, photos, scene
import Image, cStringIO

# class BackgroundView:
# - scaling a image (here: photo from the camera roll) in the original ratio if it is too big
# - landscape and portrait support

class BackgroundView(ui.View):
	def __init__(self,button_height):
		self.button_height = button_height
		self.touch_enabled = False
		self.image = None
		self.img_width = None
		self.img_height = None
		self.img_landscape = None
		self.img_portrait = None
		self.scr_scale = scene.get_screen_scale()
		self.ratio = 1.0
		
	def draw(self):
		if self.image:
			self.img_width, self.img_height = self.image.size
			path = ui.Path.rect(0, 0, self.width, self.height)
			ui.set_color('white')
			path.fill()
			self.image.draw(0,self.button_height,self.img_width*self.ratio/self.scr_scale,self.img_height*self.ratio/self.scr_scale)
			
	def layout(self):
		if self.image:
			self.img_width, self.img_height = self.image.size
			scr_height_real = (self.height - self.button_height) * self.scr_scale
			scr_width_real = self.width * self.scr_scale
			self.ratio = self.get_ratio(scr_width_real, scr_height_real)
			w = self.img_width*self.ratio/self.scr_scale
			h = self.img_height*self.ratio/self.scr_scale
			orientation = None
			if self.frame.height > self.frame.width:
				self.img_portrait = (w, h)
				orientation = 'portrait'
				scr_height_real = (self.width - 64 - self.button_height) * self.scr_scale
				scr_width_real = (self.height + 64) * self.scr_scale
				# +/- 64 for titlebar
			else:
				self.img_landscape = (w, h)
				orientation = 'landscape'
				scr_width_real = (self.height + 64) * self.scr_scale
				scr_height_real = (self.width - 64) * self.scr_scale
				# +/- 64 for titlebar
			ratio = self.get_ratio(scr_width_real, scr_height_real)
			w = self.img_width*ratio/self.scr_scale
			h = self.img_height*ratio/self.scr_scale
			if orientation == 'landscape':
				self.img_portrait = (w, h)
			else:
				self.img_landscape = (w, h)
				
	def get_ratio(self, scr_width_real, scr_height_real):
		ratio = 1.0
		y_ratio = scr_height_real / self.img_height
		x_ratio = scr_width_real / self.img_width
		# 1.0 = okay, <1.0 = Image to small, >1.0 = Image to big
		if x_ratio >= 1.0 and y_ratio < 1.0:
			ratio = y_ratio #shrink height
		elif x_ratio < 1.0 and y_ratio >= 1.0:
			ratio = x_ratio #shrink width
		elif x_ratio < 1.0 and y_ratio < 1.0:
			if x_ratio < y_ratio: #which side?
				ratio = x_ratio
			else:
				ratio = y_ratio
		return ratio
		
# class DrawOnImage:
# - 'Container' for all views, including the scrollview

class DrawOnImage(ui.View):
	def __init__(self):
		self.name = 'DrawOnImage'
		self.button_height = 50
		self.button_width = 127
		width, height = ui.get_screen_size()
		self.frame = (0,0,width,height)
		self.touch_enabled = False
		self.img_portrait = None
		self.img_landscape = None
		
		self.bgview = BackgroundView(self.button_height)    #background view (view for image)
		self.bgview.flex = 'WH'
		self.bgview.frame = (0,0,width,height)
		self.bgview.background_color = 'white'
		self.add_subview(self.bgview)
		
		self.scv = ui.ScrollView()            #scrollview for buttons
		self.scv.background_color = 'white'
		self.scv.frame = (0,0,width,self.button_height)
		self.scv.content_size = (2000,self.button_height)
		self.scv.flex = 'W'
		self.add_subview(self.scv)
		
		#just add two lines for each button and don't forget the action method with the same name
		#config_button(button, name, frame, title)
		self.scv_btn_quit = ui.Button()
		self.config_button(self.scv_btn_quit, 'btn_quit', (0,0,self.button_width,self.button_height), 'Quit')
		self.scv_btn_load = ui.Button()
		self.config_button(self.scv_btn_load, 'btn_load', (1*self.button_width,0,self.button_width,self.button_height), 'Load')
		self.scv_btn_save = ui.Button()
		self.config_button(self.scv_btn_save, 'btn_save', (2*self.button_width,0,self.button_width,self.button_height), 'Save')
		self.scv_btn_undo = ui.Button()
		self.config_button(self.scv_btn_undo, 'btn_undo', (3*self.button_width,0,self.button_width,self.button_height), 'Undo')
		self.scv_btn_color = ui.Button()
		self.config_button(self.scv_btn_color, 'btn_color', (4*self.button_width,0,self.button_width,self.button_height), 'Color')
		self.scv_btn_path_width = ui.Button()
		self.config_button(self.scv_btn_path_width, 'btn_path_width', (5*self.button_width,0,self.button_width,self.button_height), '')
		self.colors = ['white', 'grey', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
		self.color_nr = 2    #red
		self.path_widths = [3, 6, 12, 24]
		self.path_w_nr = 1          #6
		self.scv_btn_color.tint_color = self.colors[self.color_nr]
		self.set_button_actions()
		
		self.olview = OverlayView(self)
		self.olview.frame=(0,self.button_height,width,height-self.button_height)
		self.olview.flex = 'WH'
		self.olview.color = self.colors[self.color_nr]
		self.olview.path_width = self.path_widths[self.path_w_nr]
		self.path_width()
		self.add_subview(self.olview)
		self.image = None
		self.present('full_screen')
		
	def path_width(self):
		with ui.ImageContext(self.button_width, self.button_height) as ctx:
			ui.set_color(self.colors[self.color_nr])
			path = ui.Path()
			path.line_width = self.path_widths[self.path_w_nr]
			path.line_join_style = ui.LINE_JOIN_ROUND
			path.line_cap_style = ui.LINE_CAP_ROUND
			path.move_to(20,self.button_height/2)
			path.line_to(107,self.button_height/2)
			path.stroke()
			image = ctx.get_image()
			self.scv_btn_path_width.background_image = image
			
	def layout(self):
		if self.width > self.height:
			self.olview.scr_orientation = 'landscape'
		else:
			self.olview.scr_orientation = 'portrait'
		if self.bgview.image:
			if self.frame.height > self.frame.width:
				w, h = self.bgview.img_portrait
			else:
				w, h = self.bgview.img_landscape
			self.olview.frame = (0,self.button_height,w,h)
			
	def config_button(self, button, name, frame, title):
		button.name = name
		button.frame = frame
		button.title = title
		button.border_width = 1
		button.corner_radius = 3
		button.border_color = 'blue'
		button.font = ('<system-bold>', 30)
		self.scv.add_subview(button)
		
	def btn_quit(self, sender):
		self.close()
		
	@ui.in_background
	def btn_load(self, sender):
		self.bgview.image = ui.Image.from_data(photos.pick_image(raw_data=True))
		self.bgview.layout()
		self.name = 'Size: ' + str(int(self.bgview.image.size[0])) + ', ' + str(int(self.bgview.image.size[1]))
		self.olview.org_size = self.bgview.image.size
		self.layout()
		self.bgview.set_needs_display()
		if self.bgview.image:
			self.olview.bgview_image = True
			
	def btn_save(self, sender):
		bg_image = self.ui2pil(self.bgview.image)
		fo_image = self.ui2pil(self.olview.image)
		width = int(self.bgview.img_width)
		height = int(self.bgview.img_height)
		fo_image = fo_image.resize((width,height), Image.ANTIALIAS)
		fo_image = fo_image.convert('RGBA')
		pixel = fo_image.load()
		for y in xrange(0,fo_image.size[1]):
			for x in xrange(0,fo_image.size[0]):
				if pixel[x,y] == (0,0,0,255):
					pixel[x,y] = (0,0,0,0)
		bg_image.paste(fo_image, (0,0), fo_image)    #skip this if you want only the overlay image
		bg_image.save('test.jpg', quality=95, optimize=True, progressive=True)
		self.btn_quit(None)
		
	def btn_undo(self, sender):
		self.olview.delete_path()
		
	def btn_color(self, sender):
		if self.color_nr < len(self.colors) - 1:
			self.color_nr += 1
		else:
			self.color_nr = 0
		self.scv_btn_color.tint_color = self.colors[self.color_nr]
		self.olview.color = self.colors[self.color_nr]
		self.path_width()
		
	def btn_path_width(self, sender):
		if self.path_w_nr < len(self.path_widths) - 1:
			self.path_w_nr += 1
		else:
			self.path_w_nr = 0
		self.olview.path_width = self.path_widths[self.path_w_nr]
		self.path_width()
		
	def set_button_actions(self):
		for subview in self.scv.subviews:
			if isinstance(subview, ui.Button):
				subview.action = getattr(self, subview.name)
				
	#from pythonista forum
	def ui2pil(self, image):
		mem = cStringIO.StringIO(image.to_png())
		out = Image.open(mem)
		out.load()
		mem.close()
		return out
		
# class OverlayView:
# - get touch events
# - display the drawn path

class OverlayView(ui.View):
	def __init__(self, fwv):
		self.fwv = fwv
		self.path = None
		self.paths = []
		self.image = None
		self.border_color = 'red'    #frame for drawing canvas
		self.border_width = 1
		self.color = None
		self.path_width = None
		self.bgview_image = False
		self.org_size = None
		self.scr_orientation = None    #delete path needs orientation and/or screen size
		
	def layout(self):
		pass
		
	def draw(self):
		if not self.bgview_image:        #if no bgview.image exists...
			self.image = None            #...delete path
			self.paths = []
			self.path = None
		if self.path:                    #draw current path
			ui.set_color(self.color)
			self.path.stroke()
		if self.image:
			self.image.draw(0,0,self.width,self.height)    #draw path image (complete path)
		self.set_needs_display()
		
	def delete_path(self):
		path_count = len(self.paths)
		if path_count > 0:
			self.paths.pop()
			path_count -= 1
			self.image = None
			for i in xrange(0, path_count):
				old_img = self.image
				width, height = self.paths[i][1]
				with ui.ImageContext(width, height) as ctx:
					if old_img:
						old_img.draw(0,0,width,height)
					ui.set_color(self.paths[i][2])
					self.paths[i][0].stroke()
					self.image = ctx.get_image()
			self.set_needs_display()
			
	def touch_began(self, touch):
		x, y = touch.location
		self.path = ui.Path()
		self.path.line_width = self.path_width
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.move_to(x, y)
		
	def touch_moved(self, touch):
		x, y = touch.location
		if self.org_size:
			x1 = (self.org_size[0] / self.width) * x
			y1 = (self.org_size[1] / self.height) * y
			if x1 < 0:
				x1 = 0
			elif x1 > self.org_size[0]:
				x1 = self.org_size[0]
			if y1 < 0:
				y1 = 0
			elif y1 > self.org_size[1]:
				y1 = self.org_size[1]
			self.fwv.name = 'x=' + str(int(x1)) + ', y=' + str(int(y1))
		self.path.line_to(x, y)
		self.set_needs_display()
		
	def touch_ended(self, touch):
		width, height = self.width, self.height    #screen size
		self.paths.append((self.path, (width, height), self.color))
		old_img = self.image
		with ui.ImageContext(width, height) as ctx:
			if old_img:
				old_img.draw(0,0,width,height)    # previous paths
			if self.path:
				ui.set_color(self.color)
				self.path.stroke()
				self.image = ctx.get_image()    # add path to image
		self.path = None
		self.layout()
		self.set_needs_display()
		
DrawOnImage()

