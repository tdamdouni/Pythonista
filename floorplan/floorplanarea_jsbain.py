# coding: utf-8

# https://github.com/jsbain/RoomAreaFinder

from __future__ import print_function
import ui
class RoomAreaView(ui.View):
	def __init__(self,file):
		iv=ui.ImageView(frame=self.bounds)
		iv.flex='wh'
		iv.content_mode=ui.CONTENT_SCALE_ASPECT_FIT
		self.add_subview(iv)
		iv.image=ui.Image.named(file)
		iv.touch_enabled=False
		rv=RoomAreaOverlay(frame=self.bounds, flex='wh')
		self.add_subview(rv)
		self.rv=rv
	def will_close(self):
		x,y=zip(*self.rv.pts)
		print(polygonArea(x,y,float(self.rv.scale.text)))
class RoomAreaOverlay(ui.View):
	def __init__(self,*args,**kwargs):
		ui.View.__init__(self,*args,**kwargs)
		self.touch_enabled=True
		self.pts=[]
		self.currpt=[]
		self.scale=ui.TextField(frame=(50,0,100,30))
		self.scale.action=self.set_scale
		self.add_subview(self.scale)
		self.scale.text=str(0.08)
		self.lbl=ui.Label(frame=(200,0,130,30))
		self.lbl.text='Area'
		self.add_subview(self.lbl)
	def set_scale(self,sender):
		self.update_area()
		self.set_needs_display()
	def update_area(self):
		x,y=zip(*self.pts)
		area=polygonArea(x,y,float(self.scale.text))
		self.lbl.text='Area: {} squnits'.format(area)
	def touch_began(self,touch):
		self.currpt=(touch.location.x,touch.location.y)
		self.set_needs_display()
	def touch_moved(self,touch):
		self.currpt=(touch.location.x,touch.location.y)
		self.set_needs_display()
	def touch_ended(self,touch):
		self.pts.append((touch.location.x, touch.location.y))
		self.currpt=[]
		self.set_needs_display()
		self.update_area()
	def draw(self):
		ui.set_color((1,0,0))
		drawpts=[p for p in self.pts]
		if self.currpt:
			drawpts+=[self.currpt]
		if drawpts:
			pth=ui.Path()
			pth.move_to(*drawpts[0])
			p0=drawpts[0]
			for p in drawpts[1:]:
				if p:
					pth.line_to(*p)
					L=(ui.Point(*p)-ui.Point(*p0))
					P0=ui.Point(*p0)
					p0=p
					H=P0+L/2
					ui.draw_string('%3.2f'%abs(L*float(self.scale.text)),(H.x,H.y,0,0),color='red')
			pth.stroke()
			ui.Path.oval(drawpts[-1][0]-5,drawpts[-1][1]-5,10,10).fill()
			
def polygonArea(X, Y,scale):
	area = 0
	j = len(X) - 1
	for i in range(len(X)):
		area = area + (X[j] + X[i]) * (Y[j] - Y[i])*scale**2
		j = i
	return abs(area/2)
	
	
v=RoomAreaView('203723572.jpg')
v.present('fullscreen')

