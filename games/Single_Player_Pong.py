# https://gist.github.com/SebastianJarsve/5297676

from scene import *
from random import randint, choice
from math import cos, sin

screen_size = Size(768, 1024)
score = 0

def update_score(n=1):
	global score
	if n == 'reset':
		score = 0
	else: 
		score += n

class Field(object):
	def __init__(self):
		size = screen_size
		self.lines = [(0, 0, 0, size.h), (size.w, 0, size.w, size.h), (0, size.h, size.w, size.h), (0, screen_size.h/2, screen_size.w, screen_size.h/2)]
		
	def draw(self):
		stroke_weight(3)
		ellipse(screen_size.w/2-10, screen_size.h/2-10, 20, 20)
		for l in self.lines:
			line(*l)
		
		
class Player(object):
	def __init__(self):
		self.rect = Rect(screen_size.w/2-50, 50, 100, 20)
		self.pos = self.rect.center()
		self.size = self.rect.size()
		self.lives = 3
		
	def update(self):
		g = gravity()
		self.rect.x += g.x * 50
		self.rect.x = min(screen_size.w - 100, max(0, self.rect.x))
			
	def draw(self):
		rect(*self.rect)


class Ball(object):
	def __init__(self):
		self.radius = 10
		self.pos = Point(screen_size.w/2-self.radius, screen_size.h/2-self.radius)
		self.rect = Rect(self.pos.x, self.pos.y, self.radius*2, self.radius*2)
		self.vx = choice((randint(-4, -1), randint(1, 4)))
		self.vy = randint(3, 5)
	
	def collide_with_paddle(self, object1):
		if self.rect.intersects(object1.rect):
			self.rect.y = object1.rect.top()
			self.bounce('y')
			update_score()
			pos = self.rect.center().x - object1.rect.center().x
			self.vx = pos/10
		
	def bounce(self, direction='y'):
		if direction == 'y':
			self.vy *= -1 
		elif direction =='x':
			self.vx *= -1
	
	def update(self):
		self.rect.x += self.vx
		self.rect.y += self.vy
		if self.rect.x + self.radius >= screen_size.w:
			self.rect.x = screen_size.w - self.radius
			self.bounce('x')
		if self.rect.x - self.radius <= 0:
			self.rect.x = self.radius
			self.bounce('x')
		if self.rect.y + self.radius >= screen_size.h:
			self.rect.y = screen_size.h - self.radius
			self.bounce('y')
	
	def draw(self):
		fill(1,1,0)
		no_stroke()
		ellipse(*self.rect)
	
	
class Game(Scene):
	def setup(self):
		self.frame_count = 0
		self.field = Field()
		self.p1 = Player()
		self.balls = []
		
	def add_ball(self, n=1):
		self.balls.append(Ball())
	
	def draw(self):
		self.frame_count = (self.frame_count + 1) % 1600
		if self.frame_count % 1600 == 0:
			self.add_ball()
		if len(self.balls) == 0:
			self.add_ball()
		text('Score: %s' % score, x=screen_size.w/2, y=screen_size.h-50, font_size=25)
		text('Lives: %s' % self.p1.lives, x=100, y=screen_size.h-50, font_size=24)
		text('Balls: %s' % len(self.balls), x=screen_size.w-100, y=screen_size.h-50, font_size=24)
		self.field.draw()
		
		self.p1.update()	
		self.p1.draw()
		
		for ball in self.balls:
			ball.update()
			ball.draw()
			ball.collide_with_paddle(self.p1)
			if ball.rect.y < -ball.rect.h/2:
				self.p1.lives -= 1
				del self.balls[self.balls.index(ball)]
		
		if self.p1.lives < 1:
			main_scene.switch_scene(GameoverScreen())
		
				
class StartScreen(Scene):
	def setup(self):
		self.pos = Point(screen_size.w/2, screen_size.h/2)
		self.info = '''
The goal of the game is to keep the ball(s) inside the field for as long as you possibly
can. Whenever a ball bounces on the paddle, you are rewarded with a point. You have three
lives. If a ball passes the paddle, you will loose a life.
		
Touch anywhere on the screen to start'''
		
	def draw(self):
		text(self.info, x=self.pos.x, y=self.pos.y, font_size=18, alignment=5)
	
	def touch_began(self, touch):
		main_scene.switch_scene(Game())
		

class GameoverScreen(Scene):
	def setup(self):
		self.text = 'Game Over!'
	
	def draw(self):
		text(self.text, x=screen_size.w/2, y=screen_size.h/2, font_size=64, alignment=5)
	
	def touch_began(self, touch):
		main_scene.switch_scene(Game())


class MultiScene (Scene):
	def __init__(self, start_scene):
		self.active_scene = start_scene
		self.tmp_t = 0
	def switch_scene(self, new_scene):
		self.active_scene = new_scene
		self.setup()
	def setup(self):
		global screen_size
		screen_size = self.size
		self.tmp_t = self.t
		self.active_scene.setup()
	def draw(self):
		background(0,0,0)
		fill(1,1,1)
		self.active_scene.touches = self.touches
		self.active_scene.t = self.t - self.tmp_t
		self.active_scene.draw()
	def touch_began(self, touch):
		self.active_scene.touch_began(touch)
	def touch_moved(self, touch):
		self.active_scene.touch_moved(touch)
	def touch_ended(self, touch):
		self.active_scene.touch_ended(touch)


main_scene = MultiScene(StartScreen())

run(main_scene, PORTRAIT)
