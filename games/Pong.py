# coding: utf-8

# https://gist.github.com/wcaleb/8174375

from scene import *
import random

BALL_RADIUS = 20
POINT_RADIUS = 5
GUTTER = 120
PAD_WIDTH = 100
PAD_HEIGHT = 20
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
right = True
paused = True
score1 = 5
score2 = 5
screen_size = Size(768, 1024)
		 
def ball_init(right):
		global ball_pos, ball_vel # these are vectors stored as lists
		ball_pos = [screen_size.w / 2 - BALL_RADIUS, screen_size.h / 2 - BALL_RADIUS]
		if right==True:
			ball_vel = [- random.randrange(60, 180) / 40, (random.randrange(120, 140) / 40)]
		else:
			ball_vel = [- random.randrange(60, 180) / 40, - random.randrange(120, 140) / 40]
			
class MyScene (Scene):
	def setup(self):
		'''initialize paddle positions and spawn ball'''
		global pad1_pos, pad2_pos
		pad1_pos = int(screen_size.w / 2 - 50)
		pad2_pos = int(screen_size.w / 2 - 50)
		ball_init(not right)
		
	def draw(self):
		global ball_pos, ball_vel, score1, score2, paused
		
		# Draw table layout
		background(0, 0, 0)
		stroke_weight(1)
		line(0, screen_size.h/2, screen_size.w, screen_size.h/2)
		line(0, GUTTER, screen_size.w, GUTTER)
		line(0, screen_size.h - GUTTER, screen_size.w, screen_size.h - GUTTER)
		
		# Draw paddles
		rect(pad1_pos, GUTTER - PAD_HEIGHT, PAD_WIDTH, PAD_HEIGHT)
		rect(pad2_pos, screen_size.h - GUTTER, PAD_WIDTH, PAD_HEIGHT)
		
		# Register ball position
		if (ball_pos[1] <= GUTTER):
			if pad1_pos + PAD_WIDTH >= ball_pos[0] >= pad1_pos: 
				ball_vel[1] = - int(ball_vel[1] * 1.3)
			else:
				score1 -= 1
				ball_init(right)
		elif (ball_pos[1] + BALL_RADIUS + PAD_HEIGHT >= screen_size.h - GUTTER): 
			if (pad2_pos + PAD_WIDTH >= ball_pos[0] >= pad2_pos): 
				ball_vel[1] = - int(ball_vel[1] * 1.3)
			else:
				score2 -= 1
				ball_init(not right)
		elif (ball_pos[0] <= 0) or (ball_pos[0] + BALL_RADIUS * 2 >= screen_size.w):
			ball_vel[0] = -ball_vel[0]       
		
		# Check game status and draw text or ball
		if score1 == 0 or score2 == 0:
			paused = True
		if paused == True:
			if (score1 + score2) == 10:
				text('Tap to start!', 'Courier', 30, screen_size.w / 2 + 120, screen_size.h / 4, 7)
			elif score1 == 0:
				text('Winner!', 'Courier', 50, screen_size.w / 2 + 100, screen_size.h - screen_size.h / 4, 7)
			elif score2 == 0:
				text('Winner!', 'Courier', 50, screen_size.w / 2 + 100, screen_size.h / 4, 7)
		else:
			ball_pos[0] += ball_vel[0]
			ball_pos[1] += ball_vel[1]
			text(str(score1), 'Courier', 50, screen_size.w / 2, screen_size.h / 4, 7)
			text(str(score2), 'Courier', 50, screen_size.w / 2, screen_size.h - screen_size.h / 4, 7)	
			ellipse(ball_pos[0], ball_pos[1], BALL_RADIUS * 2, BALL_RADIUS * 2)	
	
	def touch_moved(self, touch):
		global pad1_pos, pad2_pos
		if touch.location.y < GUTTER and pad1_pos <= touch.prev_location.x <= pad1_pos + PAD_WIDTH:
			if touch.location.x - PAD_WIDTH < 0:
				pad1_pos = 0
			else:
				pad1_pos = touch.location.x - PAD_WIDTH
		elif touch.location.y > screen_size.h - GUTTER and pad2_pos <= touch.prev_location.x <= pad2_pos + PAD_WIDTH:
			if touch.location.x - PAD_WIDTH < 0:
				pad2_pos = 0
			else:
				pad2_pos = touch.location.x - PAD_WIDTH

	def touch_ended(self, touch):
		global score1, score2, paused
		if paused == True:
			score1 = 5
			score2 = 5
			paused = False

run(MyScene(), PORTRAIT)