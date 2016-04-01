'''Tap anywhere on the screen to generate colorful fireworks. You can also tap with multiple fingers.'''

import sk
import sound
from ui import Path
from math import pi
from random import random, randint, choice

COLORS = ['#ffa849', '#c8ff49', '#49ffe7', '#86b0ff', '#fa86ff', '#ff3131']
TRAIL_TEXTURE = sk.Texture('shp:Spark')
STAR_TEXTURE = sk.Texture('pzl:Particle1')
EXPL_TEXTURES = [STAR_TEXTURE, TRAIL_TEXTURE]
NUM_STARS = 20
BG_COLOR = '#0c001c'

class FireworksScene (sk.Scene):
	
	def did_start(self):
		self.background_color = BG_COLOR
		self.background_node = None
		self.generate_star_background()
	
	def generate_star_background(self):
		if self.background_node:
			self.background_node.remove_from_parent()
		self.background_node = sk.Node()
		w, h = self.size
		for i in xrange(NUM_STARS):
			star = sk.SpriteNode(STAR_TEXTURE)
			star.position = random()*w, random()*h + 150
			star.alpha = 0.5 + random() * 0.5
			fade_in = sk.Action.fade_alpha_to(0.5 + random() * 0.5)
			fade_in.duration = random() * 2 + 1.5
			fade_out = sk.Action.fade_out()
			fade_out.duration = random() * 2 + 1.5
			fade = sk.Action.sequence([fade_out, fade_in])
			star.run_action(sk.Action.repeat_forever(fade))
			self.background_node.add_child(star)
		self.add_child(self.background_node)
		
	def did_change_size(self, old_size):
		self.generate_star_background()
	
	def add_random_explosion(self, x, y, color):
		e = sk.EmitterNode()
		e.p_size = 12, 12
		e.p_speed = randint(50, 350)
		e.p_speed_range = randint(0, 100)
		e.p_color = color
		e.p_texture = choice(EXPL_TEXTURES)
		e.p_rotation_speed = 2000
		e.p_rotation_range = 2*pi
		e.p_color_blend_factor = 1.0
		e.emission_angle_range = 2*pi
		e.p_alpha = 1
		e.p_alpha_speed = -0.8
		e.p_scale_speed = -0.5
		e.p_lifetime = 2
		e.p_blend_mode = sk.BLEND_ADD
		e.p_birth_rate = 10000
		e.num_particles_to_emit = 200
		e.y_acceleration = -200
		e.position = x, y
		e.run_action(sk.Action.sequence([sk.Action.wait(2), sk.Action.call(e.remove_from_parent)]))
		self.add_child(e)
	
	def shoot_rocket(self, x, y):
		rocket = sk.SpriteNode(TRAIL_TEXTURE)
		rocket.size = 10, 10
		rocket.position = self.size[0] / 2, 0
		color = choice(COLORS)
		rocket.color_blend_factor = 1
		rocket.color = color
		trail = sk.EmitterNode()
		trail.target_node = self
		trail.p_texture = TRAIL_TEXTURE
		trail.p_alpha_speed = -0.5
		trail.p_size = 15, 15
		trail.p_alpha = 0.4
		trail.p_speed = 5
		trail.p_birth_rate = 200
		path = Path()
		path.add_quad_curve(x - self.size[0]/2, y, 0, y/2)
		d = abs(rocket.position - (x, y))
		duration = max(0.7, d/500.0)
		shoot = sk.Action.follow_path(path, duration)
		self.add_child(rocket)
		def add_explosion():
			rocket.remove_from_parent()
			num_explosions = randint(1, 3)
			sound.play_effect('arcade:Explosion_' + str(num_explosions))
			for i in xrange(num_explosions):
				self.add_random_explosion(x, y, choice(COLORS))
		shoot.timing_mode = sk.TIMING_EASE_IN_EASE_OUT
		trail.position = rocket.position
		trail.num_particles_to_emit = int(200 * duration)
		self.add_child(trail)
		trail.run_action(shoot)
		trail.run_action(sk.Action.sequence([sk.Action.wait(duration+1.0), sk.Action.call(trail.remove_from_parent)]))
		explode = sk.Action.call(add_explosion)
		animation = sk.Action.sequence([shoot, explode])
		rocket.run_action(animation)
		sound.play_effect('game:Woosh_2')
		
	def touch_began(self, node, touch):
		self.shoot_rocket(*touch.location)
		
scene = FireworksScene()
scene_view = sk.View()
#sv.shows_fps = True
#sv.shows_node_count = True
scene_view.run_scene(scene)
scene_view.present()