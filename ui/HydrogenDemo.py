# @ui
# https://gist.github.com/BashedCrab/5953776
#
# Hydrogen is a lightweight GUI framework for Pythonista
#
# Hydrogen        - https://gist.github.com/BashedCrab/5924965
#
# HydrogenLayouts - https://gist.github.com/BashedCrab/6103019
#
# HydrogenDemo    - https://gist.github.com/BashedCrab/5953776
#

from Hydrogen import *
from HydrogenLayouts import HColumnLayout, HBarLayout, HWindowLayout
from time import localtime

#
#	A Window base class to house the Demo Components
#
class DemoWindow(HContainer):
	def __init__(self, title='Title'):
		HContainer.__init__(self)
		self.layout = HWindowLayout(self)
		self.add_bars(title)

	def add_bars(self, title):
		titleBarInfos = (
				(title,        'move',   'top'),
				('Status Bar', 'resize', 'bottom'))
		for titleBarInfo in titleBarInfos:
			title_bar = HText(titleBarInfo[0])
			title_bar.id = titleBarInfo[1]
			title_bar.ignores_touches = False
			title_bar.touch_listeners.append(self.touch_listener)
			self.add_component(title_bar, titleBarInfo[2])
		
	def touch_listener(self, comp, type, touch):
		if type == 'began':
			self.get_scene().to_front(self)
		if type == 'moved':
			if comp.id == 'move':
				x_new = self.bounds.x + (touch.location.x - touch.prev_location.x)
				y_new = self.bounds.y + (touch.location.y - touch.prev_location.y)
				self.bounds = Rect(x_new, y_new, self.bounds.w, self.bounds.h)
			elif comp.id == 'resize':
				x_move = touch.location.x - touch.prev_location.x
				y_move = touch.location.y - touch.prev_location.y
				w = self.bounds.w + x_move
				h = self.bounds.h - y_move
				y = self.bounds.y + y_move
				self.bounds = Rect(self.bounds.x, y, w, h)
				self.do_layout()			
			
# Example widget to display the current time

class HClock(HText):
	def __init__(self):
		HText.__init__(self,'00:00:00')
		self.sec = -1
		self.laf_prefix = 'Clock '
		
	def draw_foreground(self, x, y):
		t = localtime()
		if t.tm_sec <> self.sec:
			self.sec = t.tm_sec
			self.set_text('{:02d}:{:02d}:{:02d}'.format(t.tm_hour, t.tm_min, t.tm_sec))
		HText.draw_foreground(self, x, y)
		
# Progress bar set to update with the seconds of the clock

class DemoProgressBar(HProgressBar):
	def draw_foreground(self, x, y):
		t = localtime()
		self.value = t.tm_sec / 59.0
		HProgressBar.draw_foreground(self, x, y)
		
# Example widget to display the average FPS.
class HFramesPerSecond(HText):
	def __init__(self):
		HText.__init__(self, 'FPS = 00.0')
		self.laf_prefix = 'FPS '
		self.SAMPLE_FRAMES = 30
		self.delta = 0 
		self.frame = 0
		self.fps = 0.0
		
	def draw_foreground(self, x, y):
		self.update_fps()
		HText.draw_foreground(self, x, y)
		
	def update_fps(self):
		hscene = self.get_scene()
		if(hscene <> None):
			self.delta += hscene.dt
			self.frame += 1
			if(self.frame == self.SAMPLE_FRAMES):
				self.fps = self.SAMPLE_FRAMES / self.delta
				self._text = 'FPS = {:.1f}'.format(self.fps)
				self._img = None
				self.frame = 0
				self.delta = 0
					
# Instructions to fade out over time

class HDemoInstructions(HText):
	def __init__(self):
		HText.__init__(self, 'To get started, drag the left bar onto the screen.')
		self.laf_prefix = 'Instructions '
		self.alpha = 1.0
		self.delay = 3.0
		self.fade = 3.0
		
	def set_alpha(self):
		hscene = self.get_scene()
		if(hscene <> None):
			secs = hscene.t
			if(secs > self.delay + self.fade):
				self.alpha = 0.0
				self.is_visible = False
			elif(secs > self.delay):
				self.alpha = (self.fade + self.delay - secs) / self.fade
			else:
				self.alpha = 1.0

	def h_draw(self, x_offset, y_offset):
		self.set_alpha()
		r, g, b, a = self.laf['Background']
		self.laf['Background'] = (r, g, b, self.alpha)
		r, g, b, a = self.laf['Border']
		self.laf['Border'] = (r, g, b, self.alpha)
		r, g, b, a = self.laf['Foreground']
		self.laf['Foreground'] = (r, g, b, self.alpha)
		HText.h_draw(self, x_offset, y_offset)
		
class Demo(HScene):
	def setup(self):
		self.add_local_laf()
		self.add_instructions()
	        self.text_demo        = self.add_text_demo()
        	self.image_demo       = self.add_image_demo()
		self.slider_demo      = self.add_slider_demo()
        	self.switch_demo      = self.add_switch_demo()
        	self.progress_demo    = self.add_progress_demo()
        	self.lookandfeel_demo = self.add_lookandfeel_demo()
        	self.clock            = self.add_clock()
        	self.fps              = self.add_fps()
		self.side_bar         = self.add_side_bar() 

	def add_local_laf(self):
		LAF['Clock Font Size'] = 20
		LAF['Clock Foreground'] = (0.50, 0.00, 0.00, 1.00)
		LAF['Clock Show Background'] = False
		LAF['Clock Show Border'] = False
		LAF['FPS Font Size'] = 20
		LAF['FPS Foreground'] = (0.00, 0.50, 0.00, 1.00)
		LAF['FPS Show Background'] = False
		LAF['FPS Show Border'] = False
		LAF['Instructions Font Size'] = 30
		LAF['Instructions Show Background'] = False
		LAF['Instructions Show Border'] = False
		LAF['Top Selection Bar Background'] = (1.00, 1.00, 1.00, 1.00)
		LAF['Top Selection Bar Shape'] = round_top_rect
		LAF['Bottom Selection Bar Background'] = (1.00, 1.00, 1.00, 1.00)
		LAF['Bottom Selection Bar Shape'] = round_bottom_rect
		LAF['Selection Bar Background'] = (1.00, 1.00, 1.00, 1.00)
		LAF['Selection Bar Shape'] = rectangle
		LAF['Spacer Show Background'] = False 
		LAF['Spacer Show Border'] = False 
		

	def add_instructions(self):
		instructions = HDemoInstructions()
		self.add_component(instructions)
		instructions.bounds.x = (self.bounds.w - instructions.bounds.w) / 2
		instructions.bounds.y = (self.bounds.h - instructions.bounds.h) / 2

	def add_text_demo(self):
		panel = HContainer()
		panel.insets = HInset(10, 10, 5, 5)
		panel.layout = HColumnLayout(panel)
		panel.layout.pad = HInset(0,0,-0.5,0)
		panel.layout.fill_width = False
		lines = '''Demonstration text components
		Simple control that will write text label on screen
		Choose any font available in Pythonista
		And any font size or colour
		Borders and Backgrounds can be configured
		with the Look-And-Feel
		Just like all of the other components'''
		for line in lines.splitlines():
			panel.add_component(HText(line.strip()))
		window = DemoWindow('HText Components')
		window.add_component(panel, 'center')
		window.is_visible = False
		self.add_component(window)
		panel.laf['Shape'] = rectangle
		return window
		
	def add_image_demo(self):
		img_control = HImage()
		img_control.set_image('Test_Mandrill', Size(265, 256))
		img_control.stretch = True
		window = DemoWindow('HImage Component')
		window.add_component(img_control)
		window.is_visible = False
		self.add_component(window)
		return window
		
	def add_slider_demo(self):
		panel = HContainer()
		panel.insets = HInset(10, 10, 0, 10)
		panel.layout = HColumnLayout(panel)
		panel.layout.pad = HInset(0, 0, 4, 0)
		panel.add_component(HText('Sliders Adjust Background'))
		r, g, b = self.laf['Background']
		slider = HSlider()
		slider.id = 'red'
		slider.value = r
		slider.change_listeners.append(self.slider_moved)
		panel.add_component(slider)
		slider = HSlider()
		slider.id = 'green'
		slider.value = g
		slider.change_listeners.append(self.slider_moved)
		panel.add_component(slider)
		slider = HSlider()
		slider.id = 'blue'
		slider.value = b
		slider.change_listeners.append(self.slider_moved)
		panel.add_component(slider)
		self.slider_text = HText()
		self.slider_moved(slider)
		panel.add_component(self.slider_text)
		window = DemoWindow('HSlider Components')
		window.add_component(panel)
		window.is_visible = False
		self.add_component(window)
		panel.laf['Shape'] = rectangle
		return window
		
	def add_switch_demo(self):
		clock = HClock()
		clock.is_visible = False
		self.add_component(clock)
		clock.bounds.x = (self.bounds.w - clock.bounds.w) / 2
		clock.bounds.y = self.bounds.h - (2 * clock.bounds.h)
		fps = HFramesPerSecond()
		fps.is_visible = False
		self.add_component(fps)
		fps.bounds.x = (self.bounds.w - fps.bounds.w) / 2
		fps.bounds.y = fps.bounds.h
		panel = HContainer()
		panel.insets = HInset(10, 10, 0, 10)
		panel.layout = HColumnLayout(panel)
		panel.layout.pad = HInset(0,0,2,2)
		panel.layout.fill_width = False
		switch_clock = HSwitch()
		switch_clock.id = clock
		switch_clock.change_listeners.append(self.switch_flipped)
		switch_fps = HSwitch()
		switch_fps.id = fps
		switch_fps.change_listeners.append(self.switch_flipped)
		panel.add_component(HText('Use Switches to control On/Off functions'))
		panel.add_component(HText('Activate Time Display'))
		panel.add_component(switch_clock)
		panel.add_component(HText('Activate Frame Rate Display'))
		panel.add_component(switch_fps)
		window = DemoWindow('HSwitch Components')
		window.add_component(panel)
		window.is_visible = False
		self.add_component(window)
		panel.laf['Shape'] = rectangle
		return window
		
	def add_progress_demo(self):
		panel = HContainer()
		panel.layout = HColumnLayout(panel)
		panel.insets = HInset(10, 10, 0, 10)
		panel.add_component(HText('Progress bar linked to clock seconds'))
		panel.add_component(DemoProgressBar())
		window = DemoWindow('HProgressBar Component')
		window.add_component(panel)
		window.is_visible = False
		self.add_component(window)
		panel.laf['Shape'] = rectangle
		return window
		
	def set_laf_demo_labels(self):
		self.font_label.set_text(LAF["Font"])
		self.font_size_label.set_text(str(LAF["Font Size"]))
		self.font_colour_label.set_text(str(LAF["Text Foreground"]))
		self.shape_label.set_text(LAF["Shape"].__name__)
		self.radius_label.set_text(str(LAF["Edge Radius"]))
		self.background_label.set_text(str(LAF["Background"]))
		self.border_label.set_text(str(LAF["Border"]))
		self.border_on_label.set_text(str(LAF["Show Border"]))
		self.border_width_label.set_text(str(LAF["Border Width"]))
		
	def set_laf_1(self):
		LAF["Shape"] = round_rect
		LAF["Text Foreground"] = (0.00, 0.00, 0.00, 1.00)
		LAF["Button Foreground"] = (0.00, 0.00, 0.00, 1.00)
		LAF["Background"] = (0.90, 0.90, 0.90, 1.00)
		LAF["Button Background"] = (0.80, 0.80, 0.80, 1.00)
		LAF["Button Selected"] = (0.60, 0.60, 0.60, 1.00)
		LAF["Border"] = (0.50, 0.50, 0.50, 1.00)
		LAF["Border Width"] = 1
		LAF["Font"] = 'AppleSDGothicNeo-Medium'
		LAF["Font Size"] = 16
		LAF["Edge Radius"] = 6
		LAF["Show Background"] = True
		LAF["Show Border"] = True
		
	def set_laf_2(self):
		LAF["Shape"] = rectangle
		LAF["Text Foreground"] = (0.25, 0.00, 0.25, 1.00)
		LAF["Button Foreground"] = (0.25, 0.00, 0.25, 1.00)
		LAF["Background"] = (0.30, 0.30, 0.50, 1.00)
		LAF["Button Background"] = (0.50, 0.75, 1.00, 1.00)
		LAF["Button Selected"] = (0.25, 0.40, 0.50, 1.00)
		LAF["Border"] = (0.15, 0.15, 0.30, 1.00)
		LAF["Border Width"] = 3
		LAF["Font"] = 'Avenir-Heavy'
		LAF["Font Size"] = 14
		LAF["Edge Radius"] = 8
		LAF["Show Background"] = True
		LAF["Show Border"] = True
		
	def set_laf_3(self):
		LAF["Shape"] = round_right_rect
		LAF["Text Foreground"] = (0.00, 0.25, 0.00, 1.00)
		LAF["Text Foreground"] = (0.00, 0.25, 0.00, 1.00)
		LAF["Background"] = (0.70, 0.90, 0.70, 1.00)
		LAF["Button Background"] = (0.60, 0.80, 0.80, 1.00)
		LAF["Button Selected"] = (0.40, 0.60, 0.60, 1.00)
		LAF["Border"] = (0.50, 0.50, 0.50, 1.00)
		LAF["Border Width"] = 0
		LAF["Font"] = 'Futura-Medium'
		LAF["Font Size"] = 18
		LAF["Edge Radius"] = 8
		LAF["Show Background"] = True
		LAF["Show Border"] = False
		
	def add_lookandfeel_demo(self):
		buttonInfos = (
			(self.set_laf_1, 'left'),
			(self.set_laf_2, 'center'),
			(self.set_laf_3, 'right'))
		self.font_label         = HText()
		self.font_size_label    = HText()
		self.font_colour_label  = HText()
		self.shape_label        = HText()
		self.radius_label       = HText()
		self.background_label   = HText()
		self.border_label       = HText()
		self.border_on_label    = HText()
		self.border_width_label = HText()
		barInfos = (
			('Top ',	'Font Name',	self.font_label),
			('',		'Font Size',	self.font_size_label),
			('',		'Font Colour',  self.font_colour_label),
			('',		'Shape',        self.shape_label),
			('',		'Radius',       self.radius_label),
			('',		'Background',   self.background_label),
			('',		'Border',       self.border_label),
			('',		'Border On',    self.border_on_label),
			('Bottom ',	'Border Width', self.border_width_label))
		panel = HContainer()
		panel.layout = HColumnLayout(panel)
		panel.layout.pad = HInset(0, 0, -0.5, -0.5)
		panel.insets = HInset(10, 10, 10, 10)
		panel.add_component(HText("A sample of the LookAndFeel properties"))
		bar = HContainer()
		bar.layout = HBarLayout(bar)
		bar.layout.pad = HInset(5, 5, 0, 0)
		bar.insets = HInset(5,5,10,10)
		for i, buttonInfo in enumerate(buttonInfos):
			button = HButton('Sample L&F {}'.format(i))
			button.id = buttonInfo[0]
			button.click_listeners.append(self.laf_button_clicked)
			bar.add_component(button, buttonInfo[1])
		panel.add_component(bar)
		spacer = HComponent()
		spacer.laf_prefix = "Spacer "
		spacer.preferred_size = Size(10, 10)
		panel.add_component(spacer)
		for barInfo in barInfos:
			bar = HContainer()
			bar.laf_prefix = '{}Selection Bar '.format(barInfo[0])
			bar.layout = HBarLayout(bar)
			bar.add_component(HText(barInfo[1]), 'left')
			bar.add_component(barInfo[2], 'right')
			panel.add_component(bar)
		self.set_laf_demo_labels()
		window = DemoWindow('Look and Feel Demo')
		window.add_component(panel)
		window.is_visible = False
		self.add_component(window)
		panel.laf['Shape'] = rectangle
		return window

	def add_simple_window(self, inComponent, inTitle):
		panel = HContainer()
		panel.layout = HColumnLayout(panel)
		panel.add_component(inComponent)
		window = DemoWindow(inTitle)
		window.add_component(panel)
		window.is_visible = False
		self.add_component(window)
		return window

	def add_clock(self):
		return self.add_simple_window(HClock(), 'Clock')
		
	def add_fps(self):
		return self.add_simple_window(HFramesPerSecond(), 'Frames Per Second')

	def add_side_bar(self):
		buttonInfos = (
			('Text Component Demo',                self.text_demo),
			('Image Component Demo',               self.image_demo),
			('Slider Component Demo',              self.slider_demo),
			('Switch Component Demo',              self.switch_demo),
			('Progress Bar Component Demo',        self.progress_demo),
			('Look and Feel Demo',                 self.lookandfeel_demo),
			('Sample Clock Component',             self.clock),
			('Sample Frames Per Second Component', self.fps))

		side_bar = HContainer()
		side_bar.insets = HInset(20, 20, 20, 20)
		side_bar.layout = HColumnLayout(side_bar)
		side_bar.layout.pad = HInset(0, 0, 4, 0)
		for buttonInfo in buttonInfos:
			button = HButton(buttonInfo[0])
			button.id = buttonInfo[1]
			button.click_listeners.append(self.button_clicked)
			side_bar.add_component(button)
		self.add_component(side_bar)
		side_bar.laf['Shape'] = round_right_rect  
		y = (self.bounds.h - side_bar.bounds.h) / 2
		x = -side_bar.bounds.w + 20
		side_bar.bounds.x = x
		side_bar.bounds.y = y
		side_bar.touch_listeners.append(self.drag_side_bar)
		return side_bar
		
	def drag_side_bar(self, comp, type, touch):
		if type == 'began':
			self.get_scene().to_front(comp)
		if type == 'moved':
			x_new = comp.bounds.x + (touch.location.x - touch.prev_location.x)
			if x_new > 0:
				x_new = 0
			elif x_new < -comp.bounds.w + 20:
				x_new = -comp.bounds.w + 20
			comp.bounds.x = x_new
	
	def button_clicked(self, button):
		comp = button.id
		comp.bounds.x = (self.bounds.w - comp.bounds.w) / 2
		comp.bounds.y = (self.bounds.h - comp.bounds.h) / 2
		comp.is_visible = not comp.is_visible
		self.to_front(comp)
		
	def laf_button_clicked(self, button):
		button.id.__call__()
		self.set_laf_demo_labels()
		self.load_lookandfeel()
		
	def slider_moved(self, slider):
		r, g, b = self.laf['Background']
		if(slider.id == 'red'):
			r = slider.value
		elif(slider.id == 'green'):
			g = slider.value
		elif(slider.id == 'blue'):
			b = slider.value
		self.laf['Background'] = (r, g, b)
		self.slider_text.set_text('Colour ({:.2f}, {:.2f}, {:.2f})'.format(r, g, b))
		
	def switch_flipped(self, switch):
		switch.id.is_visible = switch.is_selected
		
	def to_front(self, comp):
		self.components.remove(comp)
		self.components.append(comp)

run(Demo())