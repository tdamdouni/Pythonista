# https://forum.omz-software.com/topic/4215/scene-nube-problems

from scene import Scene, SpriteNode, run, Point

class pt(SpriteNode):

	def __init__(self, **kargs):
		SpriteNode.__init__(self, 'plf:HudX', **kargs)
		
	scale_x = 0.5
	scale_y = 0.5
	
#class plot (SpriteNode):
	#anchor_point = Point(0,0)
	#color = '#8989ff'

class plot (SpriteNode):
	def __init__(self, **kargs):
		SpriteNode.__init__(self, **kargs)
		self.anchor_point = (0, 0)
		self.color = '#8989ff'
	
class test(Scene):

	def setup(self):
		pane = plot(parent=self)
		pane.size = (self.size.x / 2, self.size.y / 2)
		pane.position = (50,50)
		
		for x in (50, 100, 150, 200, 250, 300):
			p = pt(parent=pane)
			p.position = (x, x)
			
if __name__ == '__main__':
	tst = test()
	run(tst)

