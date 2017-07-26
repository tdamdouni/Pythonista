# https://gist.github.com/dyyybek/0e93006203c034a98522601644aff013

import ui,ctypes,string
from ui import Path
from objc_util import *
UIFont=ObjCClass('UIFont')
import sys
c.CTFontCreatePathForGlyph.restype = c_void_p
c.CTFontCreatePathForGlyph.argtypes = [c_void_p, c_void_p, c_void_p]
createPath=c.CTFontCreatePathForGlyph

l = [[[[(265.0, -15.0), (348.0, -15.0), (405.0, 38.0), (438.0, 100.0)],
 [(438.0, 100.0), (438.0, 0.0)],
 [(438.0, 0.0), (488.0, 0.0)],
 [(488.0, 0.0), (488.0, 460.0)],
 [(488.0, 460.0), (438.0, 460.0)],
 [(438.0, 460.0), (438.0, 362.0)],
 [(438.0, 362.0), (406.0, 422.0), (350.0, 470.0), (265.0, 470.0)],
 [(265.0, 470.0), (162.0, 470.0), (59.0, 388.0), (59.0, 226.0)],
 [(59.0, 226.0), (59.0, 60.0), (168.0, -15.0), (265.0, -15.0)]],
 [[(265.0, 31.0), (169.0, 31.0), (109.0, 116.0), (109.0, 225.0)],
 [(109.0, 225.0), (109.0, 333.0), (169.0, 424.0), (265.0, 424.0)],
 [(265.0, 424.0), (354.0, 424.0), (437.0, 342.0), (437.0, 225.0)],
 [(437.0, 225.0), (437.0, 115.0), (354.0, 31.0), (265.0, 31.0)]]],
 [[[(275.0, -20.0), (339.0, -20.0), (388.0, 11.0), (421.0, 54.0)],
 [(421.0, 54.0), (421.0, 0.0)],
 [(421.0, 0.0), (591.0, 0.0)],
 [(591.0, 0.0), (591.0, 470.0)],
 [(591.0, 470.0), (421.0, 470.0)],
 [(421.0, 470.0), (421.0, 419.0)],
 [(421.0, 419.0), (389.0, 460.0), (342.0, 490.0), (278.0, 490.0)],
 [(278.0, 490.0), (162.0, 490.0), (53.0, 403.0), (53.0, 231.0)],
 [(53.0, 231.0), (53.0, 61.0), (169.0, -20.0), (275.0, -20.0)]],
 [[(324.0, 124.0), (265.0, 124.0), (227.0, 175.0), (227.0, 238.0)],
 [(227.0, 238.0), (227.0, 300.0), (265.0, 351.0), (324.0, 351.0)],
 [(324.0, 351.0), (377.0, 351.0), (421.0, 308.0), (421.0, 238.0)],
 [(421.0, 238.0), (421.0, 170.0), (380.0, 124.0), (324.0, 124.0)]]]]

def make_glyph(glyphs):
	tempPath = None
	for paths in glyphs:
		path = Path()
		for segment in paths:
			if len(segment) == 4:
				start_x = segment[0][0]
				start_y = segment[0][1]
				cp1_x = segment[1][0]
				cp1_y = segment[1][1]
				cp2_x = segment[2][0]
				cp2_y = segment[2][1]
				end_x = segment[3][0]
				end_y = segment[3][1]
				if path.bounds.height == 0 and path.bounds.width == 0:
					path.move_to(start_x, start_y)
					path.add_curve(end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y)
				else:
					path.add_curve(end_x, end_y, cp1_x, cp1_y, cp2_x, cp2_y)
			elif len(segment) == 2:
				start_x = segment[0][0]
				start_y = segment[0][1]
				end_x = segment[1][0]
				end_y = segment[1][1]
				if path.bounds.height == 0 and path.bounds.width == 0:
					path.move_to(start_x, start_y)
					path.line_to(end_x, end_y)
				else:
					path.line_to(end_x, end_y)
		if tempPath:
			tempPath.append_path(path)
		else:
			tempPath = path
	return tempPath
	
	
def glyphsListConstruct(list_of_glyphs=l):
	return [make_glyph(glyphs) for glyphs in list_of_glyphs]
	
glyphs_list=[]
for g in glyphsListConstruct():
	glyphs_list.append(ObjCInstance(g))
	
#choose any two glyphs, but must have same number of points, in same order
# this works very well with original glyphpath, not so much with ondevice generated ones
lastglyph = len(glyphs_list) - 1
glyphs_list=[glyphs_list[0],glyphs_list[lastglyph]]


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
		self._layer.setStrokeColor_(_get_CGColor(line_color))
		self._layer.setFillColor_(_get_CGColor(color))
		self._layer.setLineWidth_(line_width)
		self._layer.path=path
		self.setupani()
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
		#print(i)
		self._layer.timeOffset=touch.location.x/self.width
		#self.setPath(p.CGPath())
	def touch_moved(self,touch):
		i=int(touch.location.x/self.width*len(glyphs_list))
		'''if not self.lasti == i:
		self.lasti=i
		p=glyphs_list[i%len(glyphs_list)]
		self.setPath(p.CGPath(),0.2)'''
		self._layer.timeOffset=(touch.location.x/self.width)
	@on_main_thread
	def setupani(self):
		animation=ObjCClass('CABasicAnimation').animationWithKeyPath('path')
		animation.fromValue = glyphs_list[0].CGPath()
		animation.toValue = glyphs_list[1].CGPath()
		animation.removedOnCompletion=False
		animation.duration=1.
		self._layer.speed=0.
		self._layer.timeOffset=0.
		self._layer.addAnimation(animation, forKey='a')
		
		self.a=animation
		#return self.curpath()
	def setPath(self,path,duration=0.3):
		animation=ObjCClass('CABasicAnimation').animationWithKeyPath('path')
		animation.fromValue = self.curpath()
		animation.duration=duration
		self._path = path
		self._layer.addAnimation(animation, forKey=None)
		self._layer.path=self._path
		#print(self._path)
		
pv=AniPathView(glyphs_list[0].CGPath())
pv.present()
#pv.setupani(0)

