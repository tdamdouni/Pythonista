# coding: utf-8

# https://gist.github.com/danrcook/b666bbddf9c7fed3abd7a4b49d4e4954

# https://forum.omz-software.com/topic/3181/ui-view-and-touch-slidemenu/9

# uses https://github.com/mikaelho/pythonista-gestures
# many thanks to @jonb for help with gestures and @mikaelho for the pythonista_gestures module!

import ui
from Gestures import Gestures

class SideMenuSlideView(ui.View):
	def __init__(self, master_view, detail_view):
		#need to instantiate with master and detail subviews as args.
		self.touch_enabled=False # using gestures instead
		self.g=Gestures()
		self.prev_location=None
		self.g.add_pan(self,self.did_pan)
		self.small_screen_size = False
		self.menu_is_visible = False #used for redrawing with small_screen_size and for slide events
		
		self.master = ui.View(frame=(-60,0,320,200), flex='H', touch_enabled=True) #-60 for effect
		if ui.get_screen_size()[0] < 768 or ui.get_screen_size()[1] < 768: #adjust for smaller screen
			self.master.width = ui.get_screen_size()[0] - 45 #leave some space to swipe back (..need to test on iphone!)
			self.small_screen_size = True
		master_view.width = self.master.width #otherwise it's at the default 100.
		self.master.add_subview(master_view)
		
		self.detail = ui.View(frame=(0,0,100,100), flex='WH', touch_enabled=True)
		self.detail.add_subview(detail_view)
		
		self.add_subview(self.master)
		self.add_subview(self.detail)
		self.background_color = 0.4
		
		self.present()
		
	def draw(self):
		if self.scr_orientation == 'portrait' and self.small_screen_size:
			self.master.width = ui.get_screen_size()[0] - 45
		elif self.scr_orientation == 'landscape' and self.small_screen_size:
			self.master.width = ui.get_screen_size()[0] - 45
		self.detail.x = self.master.width if self.menu_is_visible else 0
		
	def layout(self):
		self.scr_orientation = 'landscape' if self.width > self.height else 'portrait'
		
	def did_pan(self,data):
		data.prev_location=self.prev_location
		self.prev_location=(data.location)
		if data.state==1:
			self.touch_began(data)
		elif data.state==2:
			self.touch_moved(data)
		else:
			self.touch_ended(data)
			
	def touch_began(self, touch):
		self.touch_start = touch.location
		
	def touch_moved(self, touch):
		y_distance = abs(touch.location[1] - self.touch_start[1])
		x_distance = abs(touch.location[0] - self.touch_start[0])
		
		#determining horizontal touch direction
		if touch.location[0] > touch.prev_location[0] and x_distance > y_distance:
			self.x_movement = 'right'
		elif touch.location[0] < touch.prev_location[0] and x_distance > y_distance:
			self.x_movement = 'left'
			
		#setting self.master attributes during slide for visual effect
		slide_percent = self.detail.x / self.master.width
		self.master.alpha = slide_percent
		self.master.x = int(-60*(1-slide_percent))
		
		#moving self.detail according to the touch slide
		if touch.location[0] > self.touch_start[0] and x_distance < self.master.width and self.detail.x != self.master.width: #movement right
			self.detail.x = x_distance
		elif touch.location[0] < self.touch_start[0] and self.detail.x > 0 and x_distance < self.master.width: #movement left
			self.detail.x = self.master.width - x_distance
			
	def touch_ended(self, touch):
		def slide_left():
			self.detail.x = 0
			self.master.alpha = 0
			self.master.x = -60
			
		def slide_right():
			self.detail.x = self.master.width
			self.master.alpha = 1
			self.master.x = 0
			
		if self.x_movement == 'right':
			self.menu_is_visible = True if self.detail.x > 40 else False
		elif self.x_movement == 'left':
			self.menu_is_visible = True if self.detail.x > self.master.width-40 else False
		ui.animate(slide_right, duration=0.4) if self.menu_is_visible else ui.animate(slide_left, duration=0.4)
		
		
		
master = ui.TableView()
master.data_source = master.delegate = ui.ListDataSource(['lorem ipsum' for i in range(100)])
master.flex = 'WH'

detail = ui.WebView()
detail.load_url('http://www.google.com')
detail.flex = 'WH'
detail.scales_page_to_fit = False

a = SideMenuSlideView(master, detail)

