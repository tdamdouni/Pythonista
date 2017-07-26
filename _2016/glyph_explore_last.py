# https://gist.github.com/jsbain/5f56c0c9e16a98df04b2e23a6198b020

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
import ctypes

def errcheck(ret,func,args):
	if func.restype==c_void_p:
		if not ret:
			raise Exception('{} returned void pointer with args\n{}'.format(func.__name__,args))
	return ret
	


		

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
def getcgfont(file):
	if not os.path.exists(file):
		raise FileNotFoundError()
		
	inData=NSData.dataWithContentsOfFile_(os.path.abspath(file))
	if not inData:
			raise Exception('No data in file')
	provider = ObjCInstance(c.CGDataProviderCreateWithCFData(inData));
	basefont = c.CGFontCreateWithDataProvider(provider);
	c.CFRelease(provider)
	return basefont

import os
class FontWithVariation(object):
	def __init__(self,basefont):
		'''basefont: cgfont'''
		varaxes=ObjCInstance(c.CGFontCopyVariationAxes(basefont))
		rng=(varaxes[0]['kCGFontVariationAxisMinValue'].intValue(),
				varaxes[0]['kCGFontVariationAxisMaxValue'].intValue())
		vardict=ObjCInstance(c.CGFontCopyVariations(basefont))
		varaxes=ObjCInstance(c.CGFontCopyVariationAxes(basefont))
		rng=(varaxes[0]['kCGFontVariationAxisMinValue'].intValue(),
				varaxes[0]['kCGFontVariationAxisMaxValue'].intValue())
		self.varaxes=varaxes
		self.range=rng
		self.basefont=basefont
		self.vardict=vardict
	def getFont(self,size=32, variation=0):
		'''return ct font for scaled variation 0..1'''
		v=self.range[0]+variation*(self.range[1]-self.range[0])
		self.vardict.setValue_forKey_(v,str(self.varaxes[0]['kCGFontVariationAxisName']))
		cgfont=ObjCInstance(c.CGFontCreateCopyWithVariations(
			self.basefont,self.vardict))
		ctfont=ObjCInstance(c.CTFontCreateWithGraphicsFont(
			cgfont,size,None, None))
		return ctfont	
class LabelledSlider(ui.View):
	'''Slider with label'''
	def __init__(self,limits=[0,1],*args,**kwargs):
		self.frame=(0,0,100,44)
		ui.View.__init__(self,*args,**kwargs)		
		self.limits=limits
		self.sldr=ui.Slider()
		self.sldr.frame=(25,0,60,44)
		self.lbl=ui.Label()
		self.lbl.frame=(0,0,25,44)
		self.sldr.action=self._action
		self.action=None
		self.sldr.flex='wl'
		self.lbl.flex='w'
		self.add_subview(self.lbl)
		self.add_subview(self.sldr)
		self.update_label()
	def update_label(self):
		'''Update label to read name:value'''
		self.lbl.text='{}:{}'.format(self.name,self.value)
	@property
	def value(self):
		'''scaled value between limits'''
		return self.limits[0]+self.sldr.value*(self.limits[1]-self.limits[0])
	@value.setter
	def value(self,value):
		self.sldr.value=(value- self.limits[0])/(self.limits[1]-self.limits[0])
		self.update_label()
	def _action(self,sldr):
		self.update_label()
		if callable(self.action):
			self.action(self)
import ui

class FontExploreView(ui.View):
	def __init__(self,font, *args,**kwargs):
		'''font: ctfontref'''
		self.font=font 
		ui.View.__init__(self,*args,**kwargs)
		text=ui.TextView(name='text')
		text.frame=[0,88,self.width,self.height-44]
		self.bg_color='white'
		text.text='Move the sliders above to adjust the font weight and size.\n\nThe quick brown fox jumped over the lazy dog.\n\nTHE QUICK BROWN FOX JUMPED OVER THE LAZY DOG.\n\nThis textfield is editable'
		text.flex='wh'
		self.add_subview(text)
		# weight slider
		weight=LabelledSlider(name='weight')
		weight.action=self.slider_action
		weight.frame=[0,0,self.width,44]
		weight.flex='w'
		self.add_subview(weight)
		#size slider
		size=LabelledSlider(name='size',limits=[10,64])
		size.action=self.slider_action
		size.frame=[0,44,self.width,44]
		size.flex='w'
		size.value=32
		self.add_subview(size)
	
	def layout(self):
		#called when first presented. crashes if called during init
		self.slider_action(None)
	def change_font(self,size,weight):
		'''get a new ctfont for size and weight, then set font of textview'''
		fontvar=self.font.getFont(size,weight)	
		ObjCInstance(self['text']).font=fontvar
	def slider_action(self,slider):
		'''callbacks for sliders'''
		size=self['size'].value
		weight=self['weight'].value
		self.change_font(size,weight)

if __name__=='__main__':
	
	file='PanvariaGX_downloaded.ttf'
	if not os.path.exists(file):
		print('downloading font')
		import requests	
		r=requests.get('https://www.dropbox.com/s/cbeqxxuk9dg8jz1/PanvariaGX.ttf?dl=1')
		with open(file,'wb') as f:
			f.write(r.content)
	
	cgfont=getcgfont(file)
	# can try other fonts, exception raised if no variation axes
	# did not work for me,but your results may vary
	#cgfont=UIFont.systemFontOfSize_(32)._backingCGSFont()
	#cgfont=UIFont.fontWithName_size_('Menlo',32)._backingCGSFont()
	base=FontWithVariation(cgfont)
	fev=FontExploreView(base)
	fev.present('')

