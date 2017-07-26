# https://forum.omz-software.com/topic/4215/scene-nube-problems/3

from scene import Scene, SpriteNode, run, EffectNode

class pt(SpriteNode):

	def __init__(self, **kargs):
		SpriteNode.__init__(self, 'plf:HudX', **kargs)
		self.scale = 0.5
		
class plot (SpriteNode):
	def __init__(self, **kargs):
		SpriteNode.__init__(self, **kargs)
		self.anchor_point = (0, 0)
		self.color = '#8989ff'
		
class test(Scene):

	def setup(self):
		clip = EffectNode(parent=self)
		clip.crop_rect = (0, 0, self.size.x / 2, self.size.y / 2)
		pane = plot(parent=clip)
		pane.size = (self.size.x / 2, self.size.y / 2)
		clip.position = (50, 50)
		
		for x in (50, 100, 150, 200, 250, 300, 350, 400):
			p = pt(parent=pane)
			p.position = (x, x)
			
if __name__ == '__main__':
	tst = test()
	run(tst)

