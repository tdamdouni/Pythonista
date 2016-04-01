# https://gist.github.com/GuyCarver/4142882
#Pythonista
#For use with the rc tank in https://gist.github.com/4141545
#I run this on my iPhone to control the tank on my iPad.

from scene import *
from sound import *
from socket import *
from struct import *

host = 'guys-ipad.local' #Change this to your iPad name running the tank program.
port = 50007
hp = (host, port)
udinterval = 1.0 / 30.0
turnscale = .0125 #convert linear movement to angular radians/second.
movescale = 1.0
debug = True

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		self.lvel = 0.0
		self.rvel = 0.0
		self.tvel = 0.0
		self.mgvel = 0.0
		self.fire = False
		self.mgfire = 0
		self.state = self.run
		self.timestamp = 0
		self.senttimer = 0.0

		#the following need only be different from the above. The actual value is unimportant.
		self.sentlvel = 1.0
		self.sentrvel = 1.0
		self.senttvel = 1.0
		self.sentmgvel = 1.0
		self.sentfire = True
		self.sentmgfire = 1
		self.sentstate = self.paused

		w = self.size.w
		h = self.size.h
		w3 = w / 2 #1/5th Screen width.
		w6 = w3 / 2 #1/10th Screen width.

		self.lmoverect = Rect(0, 0, w6, w3) #Set movement button rectangle.
		self.rmoverect = Rect(w - w6, 0, w6, w3) #Set fire button rectangle.
		self.mgmoverect = Rect(0, w3 + w6, w3,  w6) #Set fire button rectangle.
		self.tmoverect = Rect(w3, w3 + w6, w3, w6) #Set fire button rectangle.

		self.lmovepos = self.lmoverect.center()
		self.rmovepos = self.rmoverect.center()
		self.tmovepos = self.tmoverect.center()
		self.mgmovepos = self.mgmoverect.center()

		self.pausetxt = render_text('Pause', 'Copperplate', 28)
		c = self.bounds.center()
		ww = self.pausetxt[1].w
		hh = self.pausetxt[1].h
		self.pauserect = Rect(c.x - ww * .5, h - hh, ww, hh)
		self.con = socket(AF_INET, SOCK_DGRAM)

	def checksend(self):
		if self.sentlvel != self.lvel: return True
		if self.sentrvel != self.rvel: return True
		if self.senttvel != self.tvel: return True
		if self.sentmgvel != self.mgvel: return True
		if self.sentfire != self.fire: return True
		if self.sentmgfire != self.mgfire: return True
		if not self.sentstate is self.state: return True
		return False

	def send(self):
		self.sentlvel = self.lvel
		self.sentrvel = self.rvel
		self.senttvel = self.tvel
		self.sentmgvel = self.mgvel
		self.sentfire = self.fire
		self.sentmgfire = self.mgfire
		self.sentstate = self.state
		mgon = (self.mgfire != 0)
		ps = (self.sentstate == self.paused)
		self.timestamp += 1
		data = pack('iffff???', self.timestamp, self.lvel, self.rvel, self.tvel,
		            self.mgvel, self.fire, mgon, ps)
		self.con.sendto(data, hp)
		self.fire = False

	def paused(self, dt):
		self.senttimer -= dt
		if self.sentstate != self.paused:
			if self.senttimer <= 0:
				self.send()

	def run(self, dt):
		self.senttimer -= dt
		if self.senttimer <= 0:
			self.senttimer = udinterval
			if self.checksend():
				self.send()

	def drawcontrols(self):
		###Draw control boxes.
		fill(0,0,0,0)
		stroke(0, 0, .5, 1)
		stroke_weight(2)
		rect(*self.lmoverect)
		stroke(1.00, 0.50, 0.00)
		rect(*self.rmoverect)
		stroke(.5, 0, .5, 1)
		rect(*self.tmoverect)
		stroke(0.00, 1.00, 0.00)
		rect(*self.mgmoverect)

		if debug:
			tint(1,1,1)

			def drawit(p, v): text(str(v), x=p.x, y=p.y, alignment=9)

			drawit(self.lmovepos, self.lvel)
			drawit(self.rmovepos, self.rvel)
			drawit(self.tmovepos, self.tvel)
			drawit(self.mgmovepos, self.mgvel)

		c = self.bounds.center()
		clr = Color(1,1,0) if self.state == self.paused else Color(0.80, 0.40, 1)
		tint(*clr)
		s = self.pausetxt[1]
		image(self.pausetxt[0], self.pauserect.x, self.pauserect.y, *s)

	def draw(self):
		self.state(self.dt)
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		self.drawcontrols()

	def checkpause(self, loc):
		###Check to see if pause button pressed.
		if self.pauserect.intersects(Rect(loc.x, loc.y, 1, 1)):
			play_effect('Ding_2')
			if self.state == self.paused:
				self.state = self.prevstate
			else:
				self.prevstate = self.state
				self.state = self.paused

	def setchange(self, v1, v2):
		self.change |= (v1 != v2)

	def setlvel(self, touch):
		self.lvel = (touch.location.y - self.lmovepos.y) * movescale

	def setrvel(self, touch):
		self.rvel = (touch.location.y - self.rmovepos.y) * movescale

	def settvel(self, touch):
		self.tvel = (touch.location.x - self.tmovepos.x) * turnscale

	def setmgvel(self, touch):
		self.mgvel = (touch.location.x - self.mgmovepos.x) * turnscale

	def setfire(self, val):
		self.fire = val

	def setmgfire(self, val):
		self.mgfire = max(0, self.mgfire + val)

	def touch_began(self, touch):
		#Check left/right button pressed, return true if handled.
		if self.state != self.paused:
			tl = touch.location
			if tl in self.lmoverect: #If movement rectangle touched.
				self.setlvel(touch)
				return
			if tl in self.rmoverect: #If fire rectangle touched.
				self.setrvel(touch)
				return
			if tl in self.tmoverect:
				self.settvel(touch)
				return
			if tl in self.mgmoverect:
				self.setmgvel(touch)
				self.setmgfire(1)

	def touch_moved(self, touch):
		if self.state != self.paused:
			tl = touch.location

			if tl in self.lmoverect: #If movement rectangle touched.
				self.setlvel(touch)
				return

			tpl = touch.prev_location
			if tpl in self.lmoverect: #If previous location was in movement rectangle then stop movement.
				return

			if tl in self.rmoverect: #If fire rectangle touched calculate anguler velocity.
				self.setrvel(touch)
				return

			if tpl in self.rmoverect: #If previous location was in movement rectangle then stop movement.
				return

			if tl in self.tmoverect: #If fire rectangle touched calculate anguler velocity.
				self.settvel(touch)
				return

			if tpl in self.tmoverect: #If previous location was in movement rectangle then stop movement.
				return

			if tl in self.mgmoverect: #If fire rectangle touched calculate anguler velocity.
				self.setmgvel(touch)
				return

			if tpl in self.mgmoverect: #If previous location was in movement rectangle then stop movement.
				self.setmgfire(-1)

	def touch_ended(self, touch):
		#Touch ends.
		if self.state != self.paused:
			tl = touch.location
			if tl in self.lmoverect: #If no longer touching movement button decrement control count.
				self.lvel = 0.0
				return
			if tl in self.rmoverect: #If no longer touching movement button decrement control count.
				self.rvel = 0.0
				return
			if tl in self.tmoverect: #If no longer touching movement button decrement control count.
				self.tvel = 0.0
				self.setfire(True)
				return
			if tl in self.mgmoverect: #If no longer touching movement button decrement control count.
				self.mgvel = 0.0
				self.setmgfire(-1)
				return

		self.checkpause(touch.location) #Check for pause button press.

run(MyScene())