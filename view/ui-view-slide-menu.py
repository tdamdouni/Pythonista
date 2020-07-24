# https://forum.omz-software.com/topic/3181/ui-view-and-touch

# coding: utf-8

import ui

class SideMenuSlideView(ui.View):
	def __init__(self, main_view, detail_view):
		#need to instantiate with main and detail subviews as args.
		self.main = ui.View()
		self.main.frame = (0,0,250,200)
		self.main.flex = 'H'
		self.main.background_color = 0.3
		self.main.touch_enabled = False
		main_view.width = self.main.width #otherwise it's at the default 100.
		self.main.add_subview(main_view)
		
		self.detail = ui.View()
		self.detail.frame = (0,0,200,200)
		self.detail.flex = 'WH'
		self.detail.background_color = 0.8
		self.detail.touch_enabled = False
		self.detail.add_subview(detail_view)
		
		self.add_subview(self.main)
		self.add_subview(self.detail)
		self.background_color = 0.8
		self.present()
		
	def touch_began(self, touch):
		self.touch_start = touch.location
		
	def touch_moved(self, touch):
		if touch.location[0] > touch.prev_location[0]:
			self.x_movement = 'right'
		elif touch.location[0] < touch.prev_location[0]:
			self.x_movement = 'left'
		if touch.location[0] > self.touch_start[0]:
			diff = int(touch.location[0] - self.touch_start[0])
			if diff < self.main.width and self.detail.x != self.main.width:
				self.detail.x = diff
			slide_percent = self.detail.x / self.main.width
			self.main.alpha = slide_percent
			
		elif touch.location[0] < self.touch_start[0]:
			diff = int(self.touch_start[0] - touch.location[0])
			if self.detail.x > 0 and diff < self.main.width:
				self.detail.x = self.main.width - diff
			slide_percent = self.detail.x / self.main.width
			self.main.alpha = slide_percent
			
	def touch_ended(self, touch):
		def slide_left():
			self.detail.x = 0
			self.main.alpha = 0
		def slide_right():
			self.detail.x = self.main.width
			self.main.alpha = 1
		if self.x_movement == 'right':
			ui.animate(slide_right, duration=0.4)
		elif self.x_movement == 'left':
			ui.animate(slide_left, duration=0.4)
			
main = ui.WebView()
main.load_html('main')
main.flex = 'WH'
main.scales_page_to_fit = False
detail = ui.WebView()
detail.load_url('http://www.google.com/')
detail.flex = 'WH'
detail.scales_page_to_fit = False

a = SideMenuSlideView(main, detail)

# --------------------

