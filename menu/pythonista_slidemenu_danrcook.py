# coding: utf-8

# https://gist.github.com/danrcook/b666bbddf9c7fed3abd7a4b49d4e4954

# uses https://github.com/mikaelho/pythonista-gestures
# many thanks to @jonb for help with gestures and @mikaelho for the pythonista_gestures module!

import ui
from Gestures import Gestures

'''
todo
- add delegate: see @jonb's comment
x add method: toggle_menu
x add button;
- button with @property?
x arg for menu button visibility
x rename self.menu_is_visible to self.main_is_visible for consistency
x arg for full-screen on small_screen or leave a little grab room.
x get a nice example going - web bookmarks?
x rename class to SlideMenuView, makes more sense
x add docstrings for class
- add toggle for main is visible (on start)
- good way for main button to be visible if full_screen=true on small screens
'''


class SlideMenuView(ui.View):
	def __init__(self, main_view, detail_view, full_width=False, main_button_visible=True):
		'''A custom view to show a main view (likely a tableview or some list) with the detail showing
		in the detail view. Must be instantiated with two views: main and detail. Those views will be fitted appropriatey.
		- Can toggle full width on a small screen for the slide over with full_width=True/False
		- Can toggle the menu button visibility with main_button_visible=True/False'''
		
		self.touch_enabled=False # using gestures instead
		self.g=Gestures()
		self.prev_location=None
		self.g.add_pan(self,self.did_pan)
		self.small_screen_size = False
		self.full_width = full_width #full width toggle for small screen sizes when main view is visible
		self.main_is_visible = False #used for redrawing with small_screen_size and for slide events
		self.main_button_visible = main_button_visible
		
		self.main = ui.View(frame=(-60,0,320,200), flex='H', touch_enabled=True) #-60 for effect
		if ui.get_screen_size()[0] < 768 or ui.get_screen_size()[1] < 768: #adjust for smaller screen
			self.main.width = ui.get_screen_size()[0] - 45 if not self.full_width else ui.get_screen_size()[0]
			self.small_screen_size = True
		main_view.width = self.main.width #otherwise it's at the default 100.
		main_view.y = 50
		self.main.background_color = 1
		self.main.add_subview(main_view)
		
		self.detail = ui.View(frame=(0,0,100,100), flex='WH', touch_enabled=True)
		self.detail.border_width=0.5
		self.detail.border_color=0.7
		self.detail.background_color = 1
		detail_view.y = 50
		self.detail.add_subview(detail_view)
		
		if self.main_button_visible:
			self.main_button = ui.Button(image=ui.Image.named('iob:ios7_arrow_right_32'))
			self.main_button.action = self.main_button_action
			self.main_button.x = 8
			self.main_button.y = 50 - self.main_button.height
			self.detail.add_subview(self.main_button)
			
		self.add_subview(self.main)
		self.add_subview(self.detail)
		
		self.background_color = 0.35
		self.present(hide_title_bar=True)
		
	def draw(self):
		if self.scr_orientation == 'portrait' and self.small_screen_size:
			self.main.width = ui.get_screen_size()[0] - 45 if not self.full_width else ui.get_screen_size()[0]
		elif self.scr_orientation == 'landscape' and self.small_screen_size:
			self.main.width = ui.get_screen_size()[0] - 45 if not self.full_width else ui.get_screen_size()[0]
		self.detail.x = self.main.width if self.main_is_visible else 0
		
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
			
		#setting self.main attributes during slide for visual effect
		slide_percent = self.detail.x / self.main.width
		self.main.alpha = slide_percent
		self.main.x = int(-60*(1-slide_percent))
		
		#moving self.detail according to the touch slide
		if touch.location[0] > self.touch_start[0] and x_distance < self.main.width and self.detail.x != self.main.width: #movement right
			self.detail.x = x_distance
		elif touch.location[0] < self.touch_start[0] and self.detail.x > 0 and x_distance < self.main.width: #movement left
			self.detail.x = self.main.width - x_distance
			
	def touch_ended(self, touch):
		try:                            #occasionally getting an error when closing the view with two finger swipe down
			if self.x_movement == 'right':
				self.main_is_visible = True if self.detail.x > 40 else False
			elif self.x_movement == 'left':
				self.main_is_visible = True if self.detail.x > self.main.width-40 else False
			ui.animate(self.slide_right, duration=0.4) if self.main_is_visible else ui.animate(self.slide_left, duration=0.4)
		except:
			pass
			
	def slide_left(self):
		self.detail.x = 0
		self.main.alpha = 0
		self.main.x = -60
		if self.main_button_visible:
			self.main_button.image = ui.Image.named('iob:ios7_arrow_right_32')
	def slide_right(self):
		self.detail.x = self.main.width
		self.main.alpha = 1
		self.main.x = 0
		if self.main_button_visible:
			self.main_button.image = ui.Image.named('iob:ios7_arrow_left_32')
			
	@ui.in_background #in case of loading times for webpages...
	def toggle_menu(self, slide_duration=0.7):
		'''Can be called with one argument 'slide_duration'.
		Example: a.toggle_menu(slide_duration=0.3) Note: the value is in seconds.
		Use Case: hiding the menu after selecting an item in main for display in detail'''
		ui.animate(self.slide_left, duration=slide_duration) if self.main_is_visible\
		else ui.animate(self.slide_right, duration=slide_duration)
		self.main_is_visible = True if not self.main_is_visible else False
		
	def main_button_action(self, sender):
		self.toggle_menu(0.4)
		
	def detail_title_text(self, text):
		self.detail_title.text = text[:50]
		self.detail_title.width = ui.measure_string(self.detail_title.text, font=self.detail_title.font)[0]
		self.detail_title.x = (self.detail.width - self.detail_title.width) / 2
		
		
if __name__ == '__main__':
	#simple example of a few bookmarks in main (tableview) that load in detail (webview) when tapped.
	#all of the main and detail views' functions etc lay outside of SlideMenuView. SlideMenuView simply controls the view.
	
	bookmark_list = ['http://www.google.com/', 'http://www.apple.com/', 'http://www.yahoo.com/']
	
	def open_page(sender):
		detail.load_url(sender.items[sender.selected_row])
		slide_menu_view.toggle_menu()
		slide_menu_view.detail_title_text(sender.items[sender.selected_row])
		
	main = ui.TableView()
	main_datasource = ui.ListDataSource(bookmark_list)
	main_datasource.action = open_page
	main.data_source = main.delegate = main_datasource
	main.flex = 'WH'
	
	detail = ui.WebView()
	detail.load_url('http://www.google.com')
	detail.flex = 'WH'
	detail.scales_page_to_fit = False
	
	slide_menu_view = SlideMenuView(main, detail)

