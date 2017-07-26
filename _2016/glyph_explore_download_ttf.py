# https://gist.github.com/jsbain/7a766eb282c71bf7d27bd13fb4926482

import ui,ctypes,string,os
from objc_util import *
UIFont=ObjCClass('UIFont')
CAKeyframeAnimation=ObjCClass('CAKeyframeAnimation')
if sizeof(ctypes.c_size_t)==8:
	CGFloat=ctypes.c_double
else:
	CGFloat=ctypes.c_float
CGGlyph=ctypes.c_ushort
	
import sys
def errcheck(ret,func,args):
	if func.restype==c_void_p:
		if not ret:
			raise Exception('{} returned void pointer with args\n{}'.format(func.__name__,args))
	return ret
	

file='PanvariaGX_downloaded.ttf'
if not os.path.exists(file):
	print('downloading font')
	import requests	
	r=requests.get('https://www.dropbox.com/s/cbeqxxuk9dg8jz1/PanvariaGX.ttf?dl=1')
	with open(file,'wb') as f:
		f.write(r.content)
		

c.CTFontCreatePathForGlyph.restype = c_void_p
c.CTFontCreatePathForGlyph.argtypes = [c_void_p, CGGlyph, c_void_p]
c.CTFontCreatePathForGlyph.errcheck=errcheck

c.CTFontCreateWithGraphicsFont.restype=c_void_p
c.CTFontCreateWithGraphicsFont.argtypes=[c_void_p, CGFloat, c_void_p, c_void_p]
c.CTFontCreateWithGraphicsFont.errcheck=errcheck

c.CGDataProviderCreateWithCFData.restype=c_void_p
c.CGDataProviderCreateWithCFData.argtypes=[c_void_p]
c.CGDataProviderCreateWithCFData.errcheck=errcheck

c.CGFontCreateWithDataProvider.restype=c_void_p
c.CGFontCreateWithDataProvider.argtypes=[c_void_p]
c.CGFontCreateWithDataProvider.errcheck=errcheck

c.CFRelease.argtypes=[c_void_p]
c.CFRelease.restype=None

c.CGFontCopyVariations.restype=c_void_p
c.CGFontCopyVariations.argtypes=[c_void_p]
c.CGFontCopyVariations.errcheck=errcheck

c.CGFontCopyVariationAxes.restype=c_void_p
c.CGFontCopyVariationAxes.argtypes=[c_void_p]
c.CGFontCopyVariationAxes.errcheck=errcheck

c.CTFontCreateWithGraphicsFont.restype=c_void_p
c.CTFontCreateWithGraphicsFont.argtypes=[c_void_p, CGFloat, c_void_p, c_void_p]
c.CTFontCreateWithGraphicsFont.errcheck=errcheck

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

import os

def setupGlyphs(size=512,axis=0, letter='a'):
	'''return a list of paths for letter=letter, size=size, = variation axis =axis
	returns [paths, variation_values]
	'''

	if not os.path.exists(file):
		raise FileNotFoundError()
	inData=NSData.dataWithContentsOfFile_(os.path.abspath(file))
	if not inData:
		raise Exception('No data in file')
	provider = ObjCInstance(c.CGDataProviderCreateWithCFData(inData));
	basefont = c.CGFontCreateWithDataProvider(provider);
	c.CFRelease(provider)
	vardict=ObjCInstance(c.CGFontCopyVariations(basefont))
	varaxes=ObjCInstance(c.CGFontCopyVariationAxes(basefont))
	glphcode=ObjCInstance(c.CTFontCreateWithGraphicsFont(basefont,size,None, None)).glyphWithName_(letter)
	rng=(varaxes[0]['kCGFontVariationAxisMinValue'].intValue(),
			varaxes[0]['kCGFontVariationAxisMaxValue'].intValue())
	varvalues=[]
	for i in range(rng[0],rng[1]+1,10):
		vardict.setValue_forKey_(i,str(varaxes[0]['kCGFontVariationAxisName']))
		cgfont=ObjCInstance(c.CGFontCreateCopyWithVariations(basefont,vardict))
		ctfont=ObjCInstance(c.CTFontCreateWithGraphicsFont(cgfont,size,None, None))		
		t=CGAffineTransform(1,0,0,-1,0*ctfont.advancementForGlyph(glphcode).width,ctfont.capHeight())
		glyphs_list.append(UIBezierPath.bezierPathWithCGPath_(ObjCInstance(
									createPath(ctfont,glphcode,pointer(t)))))
		varvalues.append(i)
	c.CFRelease(basefont)
	return (glyphs_list, varvalues)
	
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
        
    def curpath(self):
        '''get current path, interpolated'''
        try:
           self._layer.presentationLayer().path()
        except AttributeError:
           return self._path
           
    def touch_began(self,touch):
        i=(touch.location.x)/(self.width)*len(glyphs_list)
        if i<0:
           i=0
           val=variation_values[i]
        elif i>len(glyphs_list)-1:
           i=len(glyphs_list)-1
           val=variation_values[i]
        else:
            val=variation_values[int(i)]+(i-int(i))*(variation_values[int(i)+1]-variation_values[int(i)])
        self.name='Variation value: {:0.2f}'.format(val)
        self._layer.timeOffset=i
    def touch_moved(self,touch):
        self.touch_began(touch)

if __name__=='__main__':
	[glyphs_list, variation_values]=setupGlyphs(size=512,letter='e')
	a=PathAnimation(glyphs_list)
	pv=AniPathView(glyphs_list)		
	pv.present()

