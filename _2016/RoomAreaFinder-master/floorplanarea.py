#!python3
# coding: utf-8
# https://github.com/jsbain/RoomAreaFinder
import ui,sys,console
from Gestures import Gestures
#sys.path.append('../objc_hacks')
import swizzle
from objc_util import CGPoint, on_main_thread, ObjCInstance,ObjCClass,UIApplication
l=[]
def recognizer_should_simultaneously_recognize(gr,ogr):
	g=ObjCInstance(gr)
	o=ObjCInstance(ogr)
	ispinch=g._get_objc_classname()==b'UIPinchGestureRecognizer'
	ispan=g._get_objc_classname()==b'UIPanGestureRecognizer'
	istap=g._get_objc_classname()==b'UITapGestureRecognizer'
	if (ispinch or ispan or istap) and (g.view()==o.view()) :
		return True
	else:
		return False
def gestureRecognizer_shouldRequireFailureOfGestureRecognizer_(
	_self,_sel,gr,othergr):
	console.hud_alert('aaa')
	return True
	
cls=ObjCClass(UIApplication.sharedApplication()._rootViewControllers()[0]._get_objc_classname())
swizzle.swizzle(cls,
								'gestureRecognizer:shouldRequireFailureOfGestureRecognizer:',gestureRecognizer_shouldRequireFailureOfGestureRecognizer_,'c@:@@')
								
def math_eval(expr):
	import math
	import re
	whitelist = '|'.join(
	# oprators, digits
	['-', '\+', '/', '\\', '\*', '\^', '\*\*', '\(', '\)', '\d+' ])

	if re.match(whitelist,expr):
		return eval(expr)
	else:
		return 1.0
																									
class RoomAreaView(ui.View):
	''' top level container, consisting of an imageview and an overlay	.  
	ideally this might also contain a menu bar, for changing the mode - for instance you might have a button for enabling room drawing, another one for editing points, another for zoom/pan'''
	def scrollview_should_scroll(self,sv):
		return false
	def __init__(self,file=None, data=None):
		#create image view that fills this top level view.
		#  since this RoomAreaView is the one that gets presented, it will be resized automatically, so we want the imageview to stay tied to the full view size, so we use flex.  Also, the content mode is important to prevent the image from being squished
		iv=ui.ImageView(frame=self.bounds)
		iv.flex='wh'
		iv.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
		self.add_subview(iv)
		# right now, read in file from constructor.  a future improvement would be to have a file menu to select an image, which sets the iv.image
		if file:
			iv.image=ui.Image.named(file)
		else:
			iv.image=ui.Image.from_data(data)
		iv.touch_enabled=False
		self.iv=iv
		# add the overlay. this is the touch sensitive 'drawing' layer, and store a refernce to it.  this is set to the same size as the imageview
		rv=RoomAreaOverlay(frame=self.bounds, flex='wh')
		self.add_subview(rv)
		self.rv=rv
		self.g=Gestures(delegate=rv)
		self.pinch=self.g.add_pinch(self,self.did_pinch)
		self.pan=self.g.add_pan(self,self.did_pan,2,2)
		self.pan1=self.g.add_pan(self.rv,self.rv.touch_movedn,1,1)
		self.tap=self.g.add_tap(self.rv, self.rv.touch_movedn,1,1)
		self.tap.requireGestureRecognizerToFail_(self.pinch)
		self.tap.requireGestureRecognizerToFail_(self.pan)
		self.prevscale=1
		self.curscale=1
		self.tr=(0,0)
		self.prevtr=(0,0)
		
		clear=ui.Button(title='clear')
		clear.action=rv.clear
		self.add_subview(clear)
	def did_pinch(self, data):

		s=data.scale
		self.rv.transform=self.rv.transform.concat(self.rv.transform.scale(s,s))
		self.iv.transform=self.iv.transform.concat(self.iv.transform.scale(s,s))
		self.pinch.scale=1.0

	def did_pan(self,data):
		o=data.translation
		self.rv.transform=self.rv.transform.concat(self.rv.transform.translation(*o))
		self.iv.transform=self.iv.transform.concat(self.iv.transform.translation(*o))
		self.p=CGPoint(0,0)
		self.pan.setTranslation_inView_(self.p,self.pan.view())
	def will_close(self):
		'''upon close, dump out the current area.  do this by first getting the set of points.  The zip notation lets us convert from a tuple of the form ((x0,y0),(x1,y1),...) to x=(x0,x1,...) and y=(y0,y1,...)'''
		if self.pts:
			x,y=zip(*self.rv.pts)
			print (polygonArea(x,y,float(self.rv.scale.text)))
class RoomAreaOverlay(ui.View):
	'''A touch sensitive overlay.  Touches add to a list of points, which are then used to compute area.  Lengths are shown for each line segment, snd a scaling parameter is used to adjust the length of drawn lines to known dimensions'''
	def __init__(self,*args,**kwargs):
		# call View.__init__ so we can handle any standard view constructor arguments, such as frame, bg_color, etc
		ui.View.__init__(self,*args,**kwargs)
		self.touch_enabled=True
		# store list of points, and also current point for use in dragging
		self.pts=[]
		self.curridx=-1
		# create a textfield to set scale.  could be a slider instead
		# scale is in units of feet/pixel, or really measurementunits/pixel
		# it might be easier to have user enter this as 1/scale (pixel/measunit), so that it will be a number >1.  
		# If using a Slider instead, use self.scale.value instead of float(self.scale.text) elsewhere 
		self.scale=ui.TextField(frame=(50,0,100,30))
		self.scale.action=self.set_scale
		self.add_subview(self.scale)
		self.scale.text=str(0.08)
		# create a label showing current computer room area
		self.lbl=ui.Label(frame=(200,0,130,30))
		self.lbl.text='Area'
		self.add_subview(self.lbl)
		self.lbl.bg_color='white'
	def clear(self,sender):
		self.pts=[]
		self.set_needs_display()
	def get_text_scale(self):

		return math_eval(self.scale.text)
	def set_scale(self,sender):
		'''action for self.scale. called whenever scale is changed.  when that happens we update the computation of room area, and also call set_needs_display, which forces a redraw, thus redrawing distance units'''
		self.update_area()
		self.set_needs_display()
	def update_area(self):
		'''update the area label by computing the polygon area with current scale value''' 
		try:
			x,y=zip(*self.pts)
			area=polygonArea(x,y,self.get_text_scale())
			self.lbl.text='Area: {} squnits'.format(area)
		except ValueError:
			pass
	def tap_handler(self,touch):
		pass
	def touch_begann(self,touch):
		'''when starting a touch, fiest check if there are any points very near by.  if so, set currpt to that to allow dragging prsvious points,
		if not, add a new point.
		'''
		self.curridx=-1
		currpt=(touch.location.x,touch.location.y)
		#search existing points for a near match
		for i,p in enumerate(self.pts):
			if abs(ui.Point(*p)-ui.Point(*currpt))<20:
				self.curridx=i
		# if not match found, add a new point
		if self.curridx==-1:
			self.pts.append(currpt)
		self.set_needs_display()	
	def touch_movedn(self,touch):
		''' update the current point, and redraw'''
		if touch.state==1:
			self.touch_begann(touch)
			return
		elif touch.state==2:
			self.pts[self.curridx]=(touch.location.x,touch.location.y)
		elif touch.state==3:
			self.touch_endedn(touch)
			return
		else:
			print(touch.state)
		self.set_needs_display()	
	def touch_endedn(self,touch):
		''' called when lifting finger.  append the final point to the permanent list of pts, then clear the current point, and redraw'''
		if self.curridx==-1:
			self.touch_begann(touch)
		self.curridx=-1
		self.set_needs_display()
		self.update_area()
	def recognizer_should_simultaneously_recognize(self,g,og):
		return recognizer_should_simultaneously_recognize(g,og)
	def draw(self):
		''' called by iOS whenever set_needs_display is called, or whenever os decides it is needed, for instance view rotates'''
		# set color to red
		ui.set_color((1,0,0))
		# create a copy of self.pts, and append the current point
		drawpts=self.pts

		if drawpts:
			# move path to first point:
			pth=ui.Path()
			pth.move_to(*drawpts[0])
			p0=drawpts[0]
			for p in drawpts[1:]:
				# for each point after the first, draw a line from the previous point, compute length vector L			
				#draw the line segment
				pth.line_to(*p) 
				# compute point which is halfway along line between the start/end point.  L is the vector pointing from start to finish.  H is the Point at the halfway, referenced back to global origin
				L=(ui.Point(*p)-ui.Point(*p0)) 
				P0=ui.Point(*p0)
				H=P0+L/2 #halfway point
				# put text at the halfway point, containing length ofmsegment * scale
				ui.draw_string('%3.2f'%abs(L*float(self.get_text_scale())),(H.x,H.y,0,0),color='red')
				# set starting point for next line segment
				p0=p
			pth.stroke() # draw the path
			if len(drawpts)>2: # 'close' the path to show area computed
				with ui.GState():
					pth=ui.Path()
					pth.move_to(*drawpts[-1])
					pth.line_to(*drawpts[0])
					pth.set_line_dash([2,3])
					ui.set_color((1,.5,.5,.5))
					pth.stroke()
			# create a 10 pixel circle at last entered point
			ui.Path.oval(drawpts[-1][0]-5,drawpts[-1][1]-5,10,10).fill()
			# show circles for previously entered points. smaller and lighter
			ui.set_color((1,.5,.5))
			for p in drawpts[0:-1]:
				ui.Path.oval(p[0]-3,p[1]-3,6,6).fill()
def polygonArea(X, Y,scale):
	'''compute scaled area of polygon,assuming it is closed '''
	area = 0
	j = len(X) - 1
	for i in range(len(X)):
		area = area + (X[j] + X[i]) * (Y[j] - Y[i])*scale**2
		j = i
	return abs(area/2)
	
if __name__=='__main__':
	import photos, time
	@on_main_thread
	def pick_image():
		data=photos.pick_image(raw_data=True)
		return data
	data=pick_image()
	time.sleep(1.)
	v=ui.View()
	#rv=RoomAreaView(file='203723572.jpg')
	rv=RoomAreaView(data=data)
	rv.flex='wh'
	v.add_subview(rv)
	v.frame=(100,100,600,600)
	v.present('sheet')
