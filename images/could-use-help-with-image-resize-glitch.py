# coding: utf-8

# https://forum.omz-software.com/topic/2833/could-use-help-with-image-resize-glitch

# Sketch
# A very simple drawing 'app' that demonstrates # custom views and saving images to the camera roll.

import ui
import photos
import console

# The PathView class is responsible for tracking # touches and drawing the current stroke.
# It is used by SketchView.

class PathView (ui.View):
	def __init__(self, frame):
		self.frame = frame
		self.flex = 'WH'
		self.path = None
		self.action = None
		
	def touch_began(self, touch):
		x, y = touch.location
		self.path = ui.Path()
		self.path.line_width = 3
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.move_to(x, y)
		
	def touch_moved(self, touch):
		x, y = touch.location
		self.path.line_to(x, y)
		self.set_needs_display()
		
	def touch_ended(self, touch):
		# Send the current path to the SketchView:
		if callable(self.action):
			self.action(self)
		# Clear the view (the path has now been rendered
		# into the SketchView's image view):
		self.path = None
		self.set_needs_display()
		
	def draw(self):
		if self.path:
			self.path.stroke()
			
# The main SketchView contains a PathView for the current # line and an ImageView for rendering completed strokes.
# It also manages the 'Clear' and 'Save' ButtonItems that # are shown in the title bar.

class SketchView (ui.View):
	def __init__(self, width=1024, height=1024):
		self.bg_color = 'white'
		iv = ui.ImageView(frame=(0, 0, width, height))
		pv = PathView(frame=self.bounds)
		pv.action = self.path_action
		self.add_subview(iv)
		self.add_subview(pv)
		save_button = ui.ButtonItem()
		save_button.title = 'Save'
		save_button.action = self.save_action
		clear_button = ui.ButtonItem()
		clear_button.title = 'New    '
		clear_button.tint_color = 'red'
		clear_button.action = self.clear_action
		view_button = ui.ButtonItem()
		view_button.title = '    Files'
		view_button.action = self.view_action
		self.right_button_items = [save_button, clear_button]
		self.left_button_items = [view_button]
		self.image_view = iv
		
	def path_action(self, sender):
		path = sender.path
		old_img = self.image_view.image
		width, height = self.image_view.width, self.image_view.height
		#width, height = ui.get_screen_size()
		with ui.ImageContext(width, height) as ctx:
			if old_img:
				old_img.draw()
			path.stroke()
			self.image_view.image = ctx.get_image()
			
			
	def clear_action(self, sender):
		self.image_view.image = None
		
	@ui.in_background
	def view_action(self, sender):
		self.image_view.image = ui.Image.from_data(photos.pick_image(raw_data=True))
		
	def save_action(self, sender):
		if self.image_view.image:
			# We draw a new image here, so that it has the current
			# orientation (the canvas is quadratic).
			with ui.ImageContext(self.width, self.height) as ctx:
				self.image_view.image.draw()
				img = ctx.get_image()
				photos.save_image(img)
				console.hud_alert('Saved to Photos')
		else:
			console.hud_alert('No Image to Save', 'error')
			
			
def load(self):
	# We use a quadratic canvas, so that the same image
	# can be used in portrait and landscape orientation.
	w, h = ui.get_screen_size()
	canvas_size = max(w, h)
	
	sv = SketchView(canvas_size, canvas_size)
	sv.name = 'Sketch Pad'
	sv.present('fullscreen')
	
load(None)

