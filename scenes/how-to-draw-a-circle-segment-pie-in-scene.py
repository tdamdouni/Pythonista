# coding: utf-8

# https://forum.omz-software.com/topic/2603/how-to-draw-a-circle-segment-pie-in-scene

def draw(self):
	with ui.ImageContext(200, 200) as ctx:
		path = ui.Path()
		path.move_to(180, 100)
		path.add_arc(100, 100,  80, 0, radians(170))
		path.line_width = 5
		ui.set_color('blue')
		path.stroke()
		ui_image = ctx.get_image()
	pil_image = Image.open(io.BytesIO(ui_image.to_png()))
	scene_image = load_pil_image(pil_image)
	image(scene_image)
	
#==============================

# coding: utf-8

import math, scene, ui

def circle_segment_path(r, angle):
	'''Path for circle segment (i.e. 'pizza slice') of radius r and angle degrees'''
	path = ui.Path()
	path.move_to(0, 0)
	path.line_to(r, 0)
	path.add_arc(0, 0, r, 0, -math.radians(angle), False)
	path.line_to(0, 0)
	return path
	
def circle_segment_shape(point, r, angle):
	'''Blue & red shape for circle segment of radius r and angle degrees at point'''
	return scene.ShapeNode(path=circle_segment_path(r, angle),
	fill_color='blue', stroke_color='red', position=point)
	
class MyScene (scene.Scene):
	def setup(self):
		self.add_child(circle_segment_shape(self.size/2, 200, 45))
		
if __name__ == '__main__':
	scene.run(MyScene(), show_fps=True)
	
#==============================

class MyScene (scene.Scene):
	def setup(self):
		for x in xrange(0, int(self.size.w)+50, 50):
			for y in xrange(0, int(self.size.h)+50, 50):
				self.add_child(circle_segment_shape((x, y), 50, 45))

