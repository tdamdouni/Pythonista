# https://gist.github.com/GuyCarver/3921440
from scene import *
import random
import console
from functools import partial
from sound import load_effect, play_effect

rows = 24
cols = 20
fsize = 20
plot_size = 32
offset = Point(0, 0)

images = ['Four_Leaf_Clover', 'Cookie', 'Bomb', 'PC_Character_Boy', 'Cloud', 'Explosion']
sounds = ['Click_1', 'Explosion_2', 'Powerup_2']

MINECHANCE = 0.2
moverate = plot_size * 2.0

def rowcol( pnt ) :
	###convert screen coords into plot coords.
	pnt.x = int((pnt.x - offset.x) / plot_size)
	pnt.y = int((pnt.y - offset.y) / plot_size)
	return pnt
	
def sgn( val ) :
	###-1 if < 0 otherwise 1
	return 1 if val >= 0 else -1
	
def getrect(pos) :
	###return a rect at given plot location with size of plot.
	return Rect(pos.x * plot_size + offset.x,
			 				pos.y * plot_size + offset.y,
			 				plot_size-1, plot_size-1)	

def shakeamount(val) :
	return random.random() * val - val/2
	
def randpoint(val) :
	##adlust the given value by a random value within the plot size.
	return val + shakeamount(plot_size)
	
def randangle() :
	###getbrandom angle from 0-360
	return random.random() * 360

class explosion(Layer) :
	###flame and smoke animation.
	def __init__(self) :
		Layer.__init__(self)
		self.done = True
		self.alpha = 0 
		self.ignores_touches = True
		self.smokes = [Layer() for x in xrange(4)]
		self.fire = Layer()
		self.fire.image = images[5]
		self.fire.background = Color(1,1,1,0)
		self.fire.ignores_touches = True
		self.add_layer(self.fire)
		for s in self.smokes :
			self.add_layer(s)
			s.image = images[4]
			s.background = Color(1,1,1,0)		
			s.stroke = Color(1, 1, 1, 0)		
			s.ignores_touches = True	
		
	def isdone(self) :
		###callback for end of explosion.
		self.remove_layer()
		self.done = True
		
	def fireout(self) :
		###callback for end of fire animation.
		self.fire.animate('alpha', 0, 0.5)
		
	def start(self, scn, pos) :
		###start explosion animation.
		self.fire.frame = Rect(0, 0, plot_size-1, plot_size-1)
		self.fire.alpha = 0
		self.fire.animate('alpha', 1, 0.5, completion = self.fireout)
		self.fire.animate('rotation', randangle(), 1.0)
		for s in self.smokes :
			#set positions
			s.frame = Rect(0, 0, plot_size-1, plot_size-1)
			s.scale_x = 0.1
			s.scale_y = 0.1
			s.rotation = randangle()
			s.alpha = 1
			s.animate('scale_x', 2, 1.0)
			s.animate('scale_y', 2, 1.0)
			s.animate('rotation', randangle(), 1.0)
			topos = Rect(randpoint(s.frame.x), randpoint(s.frame.y), s.frame.w, s.frame.h)
			s.animate('frame', topos, 1.0)

		scn.add_layer(self)
		self.done = False 
		self.alpha = 1
		self.frame = getrect(pos)
		self.animate('alpha', 0, 1.1, completion = self.isdone) #end explosion when alpha anim done.

class plot(Layer) :
	###represents a square in playing area.
	def __init__( self, pos, scn ) :
		Layer.__init__(self)
		self.pos = pos
		self.ignores_touches = True		
		self.background = Color(0.9, 0.9, 0.9, 0.0)
		self.stroke = Color(1, 1, 1, 0)
		self.frame = Rect(pos.x * plot_size + offset.x,
			                pos.y * plot_size + offset.y,
			                plot_size-1, plot_size-1)
		self.reset()
		scn.add_layer(self)
		
	def reset(self) :
		###reset to unrevealed state and pick mined state.
		self.image = images[0]
		self.alpha = 1
		self.mined = random.random() <= MINECHANCE
		self.revealed = False		
		 
 	def reveal(self, fade = False) :
 		###if not revealed do so. if fade is set then also set alpha.  return true if mined.
 		if self.revealed == False :
 			self.image = images[2 if self.mined else 1]
 			self.revealed = True
 			if fade :
 				self.alpha = 0.5
 		return self.mined
 			
class soldier(Layer) :
	###represents the player.
	def __init__(self, pos, scn) :
		Layer.__init__(self)
		self.ignores_touches = True
		self.image = images[3]
		self.background = Color(0.0, 0.2, 0.3, 0.0)
		self.stroke = Color(1,1,1)
		self.setpos(pos)
		self.moving = False
		self.test = False
		self.rotation = 180		
		scn.add_layer(self)
		
	def setframe(self) :
		###set position rect.
		self.frame = getrect(self.pos)

	def setpos(self, pos) :
		###force soldier to a position.
		self.pos = pos
		self.moving = False
		self.setframe()
		
	def face(self, dir) :
		###set facing angle based on movement direction and animate to it.
		if dir.x > 0 :
			rot = 90
		elif dir.x < 0 :
			rot = 270
		elif dir.y > 0 :
			rot = 180
		else:
			rot = 0
		self.animate('rotation', rot, 0.2)
		
	def testtime(self) :
		###return true if we should test and we stopped moving.
		if self.test and not self.moving :
			self.test = False
			return True
			
		return False 

	def moveit(self, dir) :
		###if not moving then start movement anims in the given direction.
		if not self.moving :
			play_effect(sounds[0])
			pos = Point(0, 0)
			self.face(dir) #turn to face direction we are moving.
			pos.x = self.pos.x + dir.x
			pos.x = min(max(0, pos.x), cols-1) #clamp x within columns.
			pos.y = self.pos.y + dir.y
			pos.y = min(max(-1, pos.y), rows) #clamp y to row count which includes empty row at top.
																				# also allow -1 for empty row at bottom.
			self.moving = True
			self.test = True #set to test plot we are on once movement stops.
			torect = getrect(pos)
			fun = partial(self.setpos, pos) #set position when animation is done.
			self.animate('frame', torect, 0.3, curve=curve_linear, completion = fun)

class MyScene (Scene):
	###the scene consists of a grid of plots each of which may be mined.  the player is to
	### navigate to the top of the screen throughnthe mine field.
	def setup(self):
		global plot_size
		global offset
		global cols
		global rows

		if self.size.w <= 700 :
			rows = 16

		self.tstart = Point(0,0)
		self.shaker = 0
		self.finished = False
		self.setscore(1)
		self.scorepos = Point(self.bounds.w - 100, self.bounds.h - 20)
		
		self.root_layer = Layer(self.bounds)
		plot_size = self.size.h / (rows + 2)
		moverate = plot_size * 2.0
		cols = int(self.size.w / plot_size - 2)
		offset.x = int((self.size.w - (cols * plot_size)) / 2)
		offset.y = int((self.size.h - (rows * plot_size)) / 2)
				
		for image in images:
			load_image(image)
			
		for snd in sounds :
			load_effect(snd)
			
		self.soldierpos = Point(cols / 2, -1)
			
		#add n rows of n columns of spots
		self.plots = [ [plot(Point(c, r), self) for c in xrange(cols)] for r in xrange(rows) ]
		self.soldier = soldier(self.soldierpos, self)
		self.explosion = explosion()

	def setscore(self, val) :
		###set score and text to print.
		self.count = val
		self.score = 'score: ' + str(val)

	def reset(self) :
		##reset game.
		self.soldier.setpos(self.soldierpos)
		self.setscore(1)
		for r in self.plots :
			for p in r :
				p.reset()

	def movedir(self, pos) :
		###calculate movement direction.
		pos.x -= self.tstart.x
		pos.y -= self.tstart.y
		ax = abs(pos.x)
		ay = abs(pos.y)
		if ax > ay :
			return Point(sgn(pos.x), 0)

		return Point(0, sgn(pos.y))
				
	def reveal(self, pos) :
		###reveal plot at given position.
		if pos.y < 0 :
			return False

		p = self.plots[pos.y][pos.x]
		return p.reveal()
	
	def revealall(self) :
		###reveal all of plots.
		for r in self.plots :
			for p in r :
				p.reveal(True)

	def testsoldier(self) :
		###test to see if soldier suceeded or died.
		if self.soldier.testtime() :
			if self.soldier.pos.y >= rows :
				play_effect(sounds[2])
				self.revealall()
				self.finished = True
			elif self.reveal(self.soldier.pos) :
				self.killsoldier()		

	def shake(self) :
		###shake screen.
		self.root_layer.frame = Rect(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
		self.shaker -= 1
		if self.shaker :
			self.root_layer.frame.x += shakeamount(6)
			self.root_layer.frame.y += shakeamount(6)
		
	def draw(self):
		background(0.0, 0.2, 0.3)
		
		self.root_layer.update(self.dt)
		if self.shaker :
			self.shake()
		else:
			self.testsoldier()
		
		self.root_layer.draw()
		text(self.score, 'Copperplate-Bold', fsize, self.scorepos.x, self.scorepos.y)
		if self.finished :
			s = 40 if self.size.w > 700 else 17
			text('You won!', 'Futura', s, *self.bounds.center().as_tuple())		

	def killsoldier(self) :
		###kill soldier and play explosion.
		play_effect(sounds[1])
		self.setscore(self.count + 1)
		self.explosion.start(self, self.soldier.pos)
		self.shaker = 10
		self.soldier.setpos(self.soldierpos)
		
	def canmove(self) :
		###return true if soldier is in a state where it can move.
		return self.shaker == 0 and not self.soldier.moving
		
	def touch_began(self, touch) :
		self.tstart = touch.location

	def touch_ended(self, touch) :
		###move soldier in direction of the gesture.
		if self.finished :
			self.finished = False
			self.reset()
		else:
			if self.canmove() :
				d = self.movedir(touch.location)
				self.soldier.moveit(d)

run(MyScene())