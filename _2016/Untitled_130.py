# https://gist.github.com/jsbain/73eb2b7395e41b55e2b4b8b95f303a8b

# https://forum.omz-software.com/topic/3946/how-to-improve-speed-of-drawing-very-slow-scene-view/5

import ui,ctypes,string
from objc_util import *

import sys
sys.path.append('vfont/VariableFonts')#replace with variableTools lication, or delete if in same path

from variableTools import glyphsListConstruct
glyphs_list=[]
for g in glyphsListConstruct():
	glyphs_list.append(ObjCInstance(g))
	
	
def _get_CGColor(color):
	"""Get a CGColor from a wide range of formats."""
	return UIColor.colorWithRed_green_blue_alpha_(
	*ui.parse_color(color)
	).CGColor()
	
class AniPathView(ui.View):
	'''animates a path based on touch'''
	def __init__(self, path, color="#21abed",
	line_width=1, line_color="#0f210f",
	*args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.bg_color='white'
		# Draw the full path on one layer
		self._layer = ObjCClass("CAShapeLayer").new()
		#self._layer.acceleratesDrawing=True
		self._layer.setStrokeColor_(_get_CGColor(line_color))
		self._layer.setFillColor_(_get_CGColor(color))
		self._layer.setLineWidth_(line_width)
		self._layer.path=path
		self._path=path
		self.lasti=0
		self.setup_layer()
	def setup_layer(self):
		ObjCInstance(self).layer().addSublayer_(self._layer)
		b=ObjCInstance(self).layer().bounds()
		b.size.height-=44
		b.origin.y=44
		self._layer.frame=b
		
	def curpath(self):
		try:
			self._layer.presentationLayer().path()
		except AttributeError:
			return self._path
	def touch_began(self,touch):
		i=int(touch.location.x/self.width*len(glyphs_list))
		p=glyphs_list[i%len(glyphs_list)]
		self.setPath(p.CGPath())
	def touch_moved(self,touch):
		i=int(touch.location.x/self.width*len(glyphs_list))
		if not self.lasti == i:
			self.lasti=i
			p=glyphs_list[i%len(glyphs_list)]
			self.setPath(p.CGPath(),0.0011)
	def setPath(self,path,duration=0.3):
		animation=ObjCClass('CABasicAnimation').animationWithKeyPath('path')
		animation.fromValue = self.curpath()
		animation.duration=duration
		self._path = path
		self._layer.addAnimation(animation, forKey=None)
		self._layer.path=self._path
		
pv=AniPathView(glyphs_list[0].CGPath())


pv.present()

