# http://omz-forums.appspot.com/pythonista/post/5808662551461888
# change the draw() method below to draw your plot
# using the ui.Path drawing commands documented at
# http://omz-software.com/pythonista/docs/ios/ui.html#path

import ui

class PlotView(ui.View):
	def __init__(self, parent = None):
		self.frame = (0, 0, 255, 255)
		if parent:
			parent.add_subview(self)
			inset_in_pixels = 4
			self.width  = parent.width  - inset_in_pixels * 2
			self.height = parent.height - inset_in_pixels * 2
			self.center = parent.center
			self.y = inset_in_pixels
		self.background_color = 'blue'
		
	def draw(self):
		path = ui.Path.oval(0, 0, self.width, self.height)
		ui.set_color('red')
		path.fill()
		
view = ui.View(background_color = 'ivory')
view.present()
plot_view = PlotView(view)

