# https://forum.omz-software.com/topic/3218/pythonista-3-bug-report/4

import scene

fmt = """Tilt your device to change colors...
        x={}
        y={}
        z={}"""

#class MyScene(scene.Scene):
        #def __init__(self):  # This scene runs itself
                #scene.run(self, frame_interval=15)  # Lower the FPS

class MyScene(scene.Scene):
	def __init__(self):
		scene.Scene.__init__(self) # <== IMPORTANT!
		scene.run(self, frame_interval=2)
		
	def setup(self):
		self.center = self.bounds.center()
		
	def draw(self):
		x, y, z = scene.gravity()
		r, g, b = abs(x), abs(y), abs(z)  # No negative colors
		scene.background(r, g, b)
		scene.tint(1-r, 1-g, 1-b)
		scene.text(fmt.format(x, y, z), font_size=32,
		x=self.center.x, y=self.center.y)
		
MyScene()  # This scene runs itself

