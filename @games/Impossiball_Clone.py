# https://gist.github.com/SebastianJarsve/5809279
from scene import *
from random import randint

screen_size = Size()

class Ball (object):
	def __init__(self, pos=None, size=Size(70, 70), c=(1,0,0)):
		load_image('White_Circle')
		if pos is None:
			pos = Point(randint(0, screen_size.w), randint(0, screen_size.h))
		self.pos = pos
		self.size = size
		self.colour = c
		if self.colour == (1,0,0):
			self.vel = Point(randint(-5, 5), randint(-5, 5))
			while self.vel.x == 0 and self.vel.y == 0:
				self.vel = Point(randint(-5, 5), randint(-5, 5))
		else: 
			self.vel = Point(0, 0)
		self.touched = False
		
	def random_pos(self):
		self.pos.x = randint(self.size.w/2, screen_size.w-self.size.w/2)
		self.pos.y = randint(self.size.h/2, screen_size.h-self.size.h/2)
		
	def bbox(self):
		return Rect(self.pos.x-self.size.w/2, self.pos.y-self.size.h/2, *self.size)
		
	def hit(self, ball):
		return self.pos.distance(ball.pos) < self.size.w/2 + ball.size.w/2
		
	def update(self):
		self.pos.x += self.vel.x
		self.pos.y += self.vel.y
		if self.bbox().left() <= 0:
			self.pos.x = self.size.w/2
			self.vel.x = abs(self.vel.x)
		if self.bbox().right() >= screen_size.w:
			self.pos.x = screen_size.w-self.size.w/2
			self.vel.x = -abs(self.vel.x)
		if self.bbox().top() >= screen_size.h:
			self.pos.y = screen_size.h-self.size.h/2
			self.vel.y = -abs(self.vel.y)
		if self.bbox().bottom() <= 0:
			self.pos.y = self.size.h/2
			self.vel.y = abs(self.vel.y)
			
	def draw(self):
		self.update()
		tint(*self.colour)
		image('White_Circle', *self.bbox())

class Game (Scene):
	def setup(self):
		bottom = 0
		top = screen_size.h
		left = 0
		right = screen_size.w
		self.walls = [(left, bottom, left, top), (left, top, right, top),
		              (right, top, right, bottom), (right, bottom, left, bottom)]
		self.player = Ball(Point(screen_size.w/2, screen_size.h/2), c=(0,0,1))
		self.gem = Ball(size=Size(50, 50), c=(0,1,0))
		self.enemies = [Ball()]
		global score; score = 0
	
	def draw(self):
		global score
		background(0.00, 0.00, 0.00)
		no_stroke()
		self.player.draw()
		self.gem.draw()
		if self.player.hit(self.gem):
			self.gem.random_pos()
			new_ball = Ball()
			while self.player.pos.distance(new_ball.pos) < 400:
				new_ball = Ball()
			self.enemies.append(new_ball)
			score += 1
		for enemy in self.enemies:
			enemy.draw()
			if self.player.hit(enemy):
				main_scene.switch_scene(GameOver)
		no_tint()
		text(str(score), x=screen_size.w/2, y=screen_size.h-50, font_size=24)
		stroke_weight(4)
		stroke(1,1,1)
		for wall in self.walls:
			line(*wall)
	
	def touch_began(self, touch):
		if touch.location in self.player.bbox():
			self.player.touched = True  
			
	def touch_moved(self, touch):
		if self.player.touched:
			self.player.pos = touch.location
			
	def touch_ended(self, touch):
		self.player.touched = False 
		
		
class Start (Scene):
	def draw(self):
		background(0, 0, 0)
		tint(0, 0, 1)
		image('White_Circle', screen_size.w/4, screen_size.h/2, 70, 70)
		tint(1, 0, 0)
		image('White_Circle', screen_size.w/4*2, screen_size.h/2, 70, 70)
		tint(0,1,0)
		image('White_Circle', screen_size.w/4*3, screen_size.h/2, 70, 70)
		no_tint()
		text('This is you.', x=(screen_size.w/3)-50, y=100+screen_size.h/2, font_size=24)
		text('Avoid this.', x=(screen_size.w/4*2)+40, y=100+screen_size.h/2, font_size=24)
		text('Catch this.', x=40+(screen_size.w/4*3), y=100+screen_size.h/2, font_size=24)
		text('Touch screen to start.', x=screen_size.w/2, y=screen_size.h-100, font_size=32)
		
	def touch_ended(self, touch):
		main_scene.switch_scene(Game)
		
		
class GameOver (Scene):
	def setup(self):
		self.button = Button(Rect((screen_size.w/2)-100, (screen_size.h/2)-50, 200, 100), 'RESTART')
		self.button.action = self.restart
		self.add_layer(self.button)
		
	def restart(self):
		main_scene.switch_scene(Game)
		
	def draw(self):
		background(0,0,0)
		self.button.draw()
		no_tint()
		text('Your score was: {0}'.format(score), x=screen_size.w/2, y=screen_size.h-50, font_size=24)
		
		
class MultiScene (Scene):
	def __init__(self, start_scene):
		self.active_scene = start_scene()
		
	def switch_scene(self, new_scene):
		self.active_scene = new_scene()
		self.setup()
		
	def setup(self):
		global screen_size
		screen_size = self.size
		self.active_scene.add_layer = self.add_layer
		self.active_scene.size = self.size
		self.active_scene.setup()
		
	def draw(self):
		self.active_scene.touches = self.touches
		self.active_scene.draw()
		
	def touch_began(self, touch):
		self.active_scene.touch_began(touch)
		
	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
		
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)

main_scene = MultiScene(Start)
run(main_scene)