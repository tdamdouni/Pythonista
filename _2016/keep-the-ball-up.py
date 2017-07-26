# coding: utf-8

# https://forum.omz-software.com/topic/3881/keep-the-ball-up

from scene import *
A = Action


class TouchBall(Scene):
	def setup(self):
	
		ball_size = 1
		bend = 10 # higher value puts less bend on the ball
		
		self.background_color = 'green'
		
		self.ball = SpriteNode('emj:White_Circle',parent=self,color='yellow')
		self.ball.position = (self.size.x/2,200)
		self.ball.scale = ball_size
		
		self.x_motion = 0
		self.y_motion = 0
		
		self.bend = bend
		
		self.can_hit = True
		
	def update(self):
	
		self.ball_move_logic()
		self.wall_collision_logic()
		self.reset()
		
	def ball_move_logic(self):
	
		x, y = self.ball.position
		
		x += self.x_motion
		y += self.y_motion
		
		self.ball.position = (x,y)
		
	def wall_collision_logic(self):
		ball_x, ball_y = self.ball.position
		half_ball_x_size = (self.ball.frame[2]/2)
		half_ball_y_size = (self.ball.frame[3]/2)
		x, y = self.size
		
		if ball_x < (0+half_ball_x_size):
			self.x_motion -= (self.x_motion*2)
			
		if ball_x > (x-half_ball_x_size):
			self.x_motion -= (self.x_motion*2)
			
		if ball_y > (y-half_ball_y_size):
			self.y_motion -= (self.y_motion*2)
			self.can_hit = True
			
	def reset(self):
		x, y = self.size
		ball_pos_x, ball_pos_y = self.ball.position
		
		if ball_pos_y < (0-self.ball.frame[3]):
			self.can_hit = True
			self.ball.position = (self.size.x/2,200)
			self.x_motion = 0
			self.y_motion = 0
			
	def touch_began(self, touch):
		x, y = touch.location
		ball_pos_x, ball_pos_y, ball_size_x, ball_size_y = self.ball.frame
		
		if ball_pos_x < x < (ball_pos_x + ball_size_x) and ball_pos_y < y < (ball_pos_y + ball_size_y) and self.can_hit == True:
			self.can_hit = False
			side = (ball_pos_x + (ball_size_x/2)) - x
			self.x_motion += side/self.bend
			if self.y_motion == 0:
				self.y_motion += 10
			else:
				self.y_motion -= (self.y_motion*2)
				
		#touch graffic
		cross = SpriteNode('shp:x4',parent=self)
		cross.position = (x, y)
		fade_out = A.fade_to(0)
		cross.run_action(fade_out)
		
		
run(TouchBall(),PORTRAIT)
# --------------------

