# https://forum.omz-software.com/topic/4252/how-to-use-scene-rect/4

from scene import *
import random
A = Action
class Rock (SpriteNode):
	def __init__(self, **kwargs):
	
		SpriteNode.__init__(self, 'spc:MeteorBrownSmall1', **kwargs)
		
		
class Gamefield (Scene):
	def setup (self):
		self.items = []
		self.background_color = '#0c1037'
		score_font = ('Futura', 30)
		self.score_label = LabelNode('0', score_font, parent=self)
		self.score_label.position = (20,1000)
		self.score_label.z_position = 1
		self.score = 0
		
		
		self.ship = SpriteNode('spc:PlayerShip3Red')
		self.ship.position = (100,40)
		self.add_child(self.ship)
		
	def touch_began(self, touch):
		x, y = touch.location
		move_action = Action.move_to(x, y , 0.9, TIMING_SINODIAL)
		self.ship.run_action(move_action)
		
		
		
		
	def update(self):
	
		self.check_item_collisions()
		
		if random.random() < 0.006:
			self.spawn_item()
			
	def spawn_item(self):
	
		rock = Rock(parent=self)
		rock.position = (random.uniform(10, self.size.w-10), self.size.h + 30)
		
		d = random.uniform(2.0, 19.0)
		
		actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
		rock.run_action(A.sequence(actions))
		self.items.append(rock)
		self.score += 1
		self.score_label.text = str(self.score)
		
		
	def check_item_collisions(self):
	
	
		for item in list(self.items):
			if item.frame.intersects(self.ship.frame):
				exit()
				
				
				
				
run(Gamefield())

