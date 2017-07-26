# https://gist.github.com/jsbain/cc991097ddc6b5f28efe22c38105138b

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

import logging

logger = logging.getLogger('glyph_explore')
if not logger.handlers:
	hdlr = logging.FileHandler('glyphlog.txt','w')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 

#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
logger.info('logging started')


import ctypes


class loggingCDLL(ctypes.CDLL):
	'''CDLL that logs all calls and arguments'''
	class _FuncPtr(ctypes._CFuncPtr):
		_flags_ = ctypes._FUNCFLAG_CDECL | ctypes._FUNCFLAG_USE_ERRNO
		_restype_ = ctypes.c_int
		def __call__(self, *args):
			logger.debug('call:'+ self.__name__)
			logger.debug('. args:'+args.__repr__())
			ret = ctypes._CFuncPtr.__call__(self, *args)
			logger.debug('. ret:'+ret.__repr__())
			return ret
	def __init__(self, *args, **kw):
		ctypes.CDLL.__init__(self, *args, **kw)
		del self._FuncPtr

c=loggingCDLL(None)

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

c.CGFontCreateCopyWithVariations.argtypes=[c_void_p, c_void_p]
c.CGFontCreateCopyWithVariations.restype=c_void_p
c.CGFontCreateCopyWithVariations.errcheck=errcheck

createPath=c.CTFontCreatePathForGlyph
glyphs_list=[]

class PathAnimation(object):
	def __init__(self,pathList,variation_values):
		a=CAKeyframeAnimation.animationWithKeyPath_('path')
		a.values=ns([p.CGPath() for p in pathList])
		a.duration=len(pathList)
		a.removedOnCompletion=False
		self.animation=a
		self.variation_values=variation_values
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
    def __init__(self, ani, color="#21abed",
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
        ani.copyToLayer(self._layer)
        self.variation_values=ani.variation_values
    def setup_layer(self):
        ObjCInstance(self).layer().addSublayer_(self._layer)
        
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
           val=self.variation_values[i]
        elif i>len(glyphs_list)-1:
           i=len(glyphs_list)-1
           val=self.variation_values[i]
        else:
            val=self.variation_values[int(i)]+(i-int(i))*(self.variation_values[int(i)+1]-self.variation_values[int(i)])
        self.name='Variation value: {:0.2f}'.format(val)
        self._layer.timeOffset=i
    def touch_moved(self,touch):
        self.touch_began(touch)

if __name__=='__main__':
	[glyphs_list, variation_values]=setupGlyphs(size=512,letter='b')
	a=PathAnimation(glyphs_list,variation_values)
	pv=AniPathView(a)
	pv.present()

