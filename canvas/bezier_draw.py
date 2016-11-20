# https://gist.github.com/jsbain/2d9e24f31f471f629d56912ead624538

# a simple bezier drawing program
#  divide into interface (taps), drawing code, callbacks
#       ui:
#       top menu
#.
# drawing code:
        #  single tap, add a point
        # tap + drag => addoint then create and drag locked handle
        #  dragging existing control point or point. move ''
        #. tap an existing point:show handles
# todo:
        # add pinch zoom
        # add point to existing curve.  delete points. lock handles
        # callbacks
        # "toolbar" with different tools ( shapes, pen, line, scribble, etc)

from Gestures import Gestures
import ui
class State (object):
	READY=0
	ADDPOINT=1
	MOVINGHANDLES=2
	MOVINGPOINT=3
HIT_THRESHOLD=15
class BezierCanvas(ui.View):
	def __init__(self):
		self.points=[]
		self.cps=[]
		g=Gestures()
		self.state=State.READY
		self.active=-1
		g.add_tap(self,self.handle_tap,number_of_taps_required=2)
		g.add_long_press(self,self.handle_long_press,
		allowable_movement=1000,
		minimum_press_duration=0.001)
		self.bg_color='white'
		self.frame=[0,0,576,769]
		self.g=g
	def handle_tap(self,data):
		if data.state == Gestures.ENDED:
			if self.check_cp_hit(data.location):
				self.cps[self.active][1-self.activecp] = 2*self.points[self.active] - self.cps[self.active][self.activecp]
		self.set_needs_display()
	def flash(self):
		a=self.alpha
		def dark():
			self.alpha=0.9*a
		def light():
			self.alpha=a
		ui.animate(dark,duration=0.01,completion=light)
	def check_point_hit(self,location):
		# FIND nearest point, or cp
		for i,p in enumerate(self.points):
			if abs(p-location)<=HIT_THRESHOLD:
				self.active=i
				return True
				
	def check_cp_hit(self,location):
		if not self.cps:
			return
		for j,cp in enumerate(self.cps[self.active]):
			if abs(cp-location)<=HIT_THRESHOLD:
				self.activecp=j
				return True
	def handle_long_press(self,data):
		if data.state == Gestures.BEGAN:
			#self.check_cp_hit
			if self.check_cp_hit(data.location):
				self.state=State.MOVINGHANDLES
				return
			if self.check_point_hit(data.location):
				self.state=State.MOVINGPOINT
				return
			self.active=-1
			self.points.append(data.location)
			self.cps.append([data.location,data.location])
		elif data.state == Gestures.CHANGED:
			if self.state==State.MOVINGPOINT:
				dp=data.location-self.points[self.active]
				self.points[self.active]+=dp
				self.cps[self.active][0]+=dp
				self.cps[self.active][1]+=dp
			elif self.state==State.MOVINGHANDLES:
				self.cps[self.active][self.activecp]=data.location
			else:
				self.cps[self.active] = [2*self.points[self.active] - data.location,    data.location]
		else:
			self.state=State.READY
		self.set_needs_display()
		
	def draw(self):
		pth=ui.Path()
		ui.set_color(self.tint_color)
		for p in self.points:
			ui.Path.oval(p.x-5,p.y-5,10,10).fill()
		if len(self.points)>1:
			pth=ui.Path()
			pth.move_to(self.points[0].x,self.points[0].y)
			for i in range(1,len(self.points)):
				p1=self.points[i]
				cp0=self.cps[i-1][1]
				cp1=self.cps[i][0]
				pth.add_curve(p1.x,p1.y,cp0.x,cp0.y,cp1.x,cp1.y)
				
			pth.stroke()
			lastcp=self.cps[self.active]
			for p in lastcp:
				ui.Path.oval(p.x-5,p.y-5,10,10).stroke()
			pth=ui.Path()
			pth.move_to(*lastcp[0])
			pth.line_to(*self.points[self.active])
			pth.line_to(*lastcp[1])
			pth.set_line_dash([4, 3])
			pth.stroke()
			
			
b=BezierCanvas()
b.name='Draw!'
b.present('sheet')

