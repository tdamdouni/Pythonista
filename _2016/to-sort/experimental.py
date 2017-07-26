# https://gist.github.com/anonymous/10619306d98bb75b77338a66576518b1

# Allows simple, yet amazing image drawing abilities.

import ui
import Image

class Paper (ui.View):
	def __init__(self, frame):
		self.frame = frame
		
		# create the imageview that actually shows the image you're drawing.
		self.canvas = ui.ImageView()
		self.canvas.frame = frame
		with ui.ImageContext(self.width,self.height) as setup:
			background = ui.Path()
			ui.set_color("white")
			ui.fill_rect(0,0,self.width,self.height)
			bg = background.rect(0,0,self.width,self.height)
			self.canvas.image = setup.get_image()
		
		self.add_subview(self.canvas)
		
		self.color = "black"
		self.brush_size = 8
		
		self.path = None
	
	def touch_began(self, touch):
		self.path = ui.Path()
		self.path.line_cap_style = ui.LINE_CAP_ROUND
		self.path.line_join_style = ui.LINE_JOIN_ROUND
		self.path.line_width = self.brush_size
		self.path.move_to(touch.location[0],touch.location[1])
		self.path.line_to(touch.location[0],touch.location[1])
		self.path.fill()
	def touch_moved(self, touch):
		self.path.line_to(touch.location[0],touch.location[1])
		self.path.fill()
		self.update_paper()
	def touch_ended(self, touch):
		pass
		
	def update_paper(self):
		previousImage = self.canvas.image
		with ui.ImageContext(self.width,self.height) as newImageCtx:
			if previousImage:
				previousImage.draw()
			ui.set_color(self.color)
			self.path.stroke()
			self.canvas.image = newImageCtx.get_image()
	
	def get_image(self):
		return self.canvas.image

