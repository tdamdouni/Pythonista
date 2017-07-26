# https://gist.github.com/jsbain/8fe4aa269b15a7071633e256456786ca

import ui,ctypes,string
from objc_util import *
UIFont=ObjCClass('UIFont')
CAKeyframeAnimation=ObjCClass('CAKeyframeAnimation')

import sys
c.CTFontCreatePathForGlyph.restype = c_void_p
c.CTFontCreatePathForGlyph.argtypes = [c_void_p, c_void_p, c_void_p]
createPath=c.CTFontCreatePathForGlyph
glyphs_list=[]

class PathAnimation(object):
	def __init__(self,pathList):
		a=CAKeyframeAnimation.animationWithKeyPath_('path')
		a.values=ns([p.CGPath() for p in pathList])
		a.duration=len(pathList)
		a.removedOnCompletion=False
		self.animation=a
		self._len=len(pathList)
	@on_main_thread
	def copyToLayer(self,layer):
		'''Given a CAShapeLayer, add animation'''
		layer.timeOffset=0
		layer.speed=0
		layer.addAnimation(self.animation, forKey='a')
	def __len__(self):
		return self._len
		
'''
set to false for funny alternative'''
usePredefined=True
if usePredefined:
	sys.path.append('vfont/VariableFonts')
	from variableTools import glyphsListConstruct
	g=glyphsListConstruct()
	for G in g[0::20]:
		glyphs_list.append(ObjCInstance(G))

else:

	glyphs_list=[]
	for w in [-1, -0.5, 0., 0.5, 1]:
		f=UIFont.systemFontOfSize_weight_(512,w)
		glph=f.glyphWithName_('O')
		glyphs_list.append(UIBezierPath.bezierPathWithCGPath_(ObjCInstance(createPath(f,glph,None))))


a=PathAnimation(glyphs_list)

def _get_CGColor(color):
    """Get a CGColor from a wide range of formats."""
    return UIColor.colorWithRed_green_blue_alpha_(
        *ui.parse_color(color)
    ).CGColor()

class AniPathView(ui.View):
    '''animates a path based on touch'''
    def __init__(self, pathList, color="#21abed",
                 line_width=1, line_color="#0f210f",
                 *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.bg_color='white'
        # Draw the full path on one layer
        self._layer = ObjCClass("CAShapeLayer").new()
        self._layer.setStrokeColor_(_get_CGColor(line_color))
        self._layer.setFillColor_(_get_CGColor(color))
        self._layer.setLineWidth_(line_width)
        self.setup_layer()
        a.copyToLayer(self._layer)
    def setup_layer(self):
        ObjCInstance(self).layer().addSublayer_(self._layer)
        b=ObjCInstance(self).layer().bounds()
        b.size.height-=44
        b.origin.y=44
        self._layer.frame=b
        
    def curpath(self):
        '''get current path, interpolated'''
        try:
           self._layer.presentationLayer().path()
        except AttributeError:
           return self._path
           
    def touch_began(self,touch):
        i=(5+touch.location.x)/(self.width-10)*len(glyphs_list)
        if i<0:
           i=0
        if i>len(glyphs_list):
           i=len(glyphs_list)
        self._layer.timeOffset=i
        self.name=str(i)
    @on_main_thread
    def touch_moved(self,touch):
        i=(5+touch.location.x)/(self.width-10)*len(glyphs_list) 
        if i<0:
           i=0
        if i>len(glyphs_list):
           i=len(glyphs_list)
        self._layer.timeOffset=i
        self.name=str(i)


pv=AniPathView(glyphs_list)

	
pv.present()
#pv.setupani(0)
