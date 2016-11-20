# coding: utf-8
# (work-in-progress, but playable)

import sk
import sound
from itertools import chain
from random import choice
from functools import partial
import gc
import ui

zoom = 1.0 if max(ui.get_screen_size()) > 768 else 0.7
player_and_effects = sk.load('PlayerAndEffects.pysk', sk.Node())
star_effect = player_and_effects['stars'][0]
standing_texture = sk.Texture('plf:AlienPink_stand')
walk_textures = [sk.Texture('plf:AlienPink_walk1'), sk.Texture('plf:AlienPink_walk2')]
jump_texture = sk.Texture('plf:AlienPink_jump')
hit_texture = sk.Texture('plf:AlienPink_hit')
spring_texture1 = sk.Texture('plf:Tile_Spring')
spring_texture2 = sk.Texture('plf:Tile_Sprung')
bg_texture = sk.Texture('plf:BG_Blue_grass')
sounds = {'coin': 'digital:PowerUp2', 'star': 'digital:PowerUp7', 'jump': 'digital:PhaserUp2', 'spring': 'digital:PhaserUp3', 'die': 'digital:ZapThreeToneDown', 'jetpack': 'digital:LowRandom', 'jetpack_empty': 'digital:PepSound1'}
g = -0.5

class ScoreHUD (sk.Node):
	def __init__(self):
		self.digit_textures = {i: sk.Texture('plf:Hud' + str(i)) for i in xrange(10)}
		self.digits = [sk.SpriteNode(self.digit_textures[0]) for i in xrange(5)]
		for i, digit in enumerate(self.digits):
			digit.position = (i * 27, 0)
			self.add_child(digit)
	
	def set_score(self, value):
		value = min(value, 99999)
		score_str = '%05i' % value
		for i, s in enumerate(score_str):
			self.digits[i].texture = self.digit_textures[int(s)]

class GameLevel (object):
	def __init__(self, name, x=0):
		self.node = sk.load(name, sk.Node())
		self.node.position = (x, 0)
		self.tiles = self.node['tile_*_*']
		edge_types = 'RLTB'
		self.max_x = x
		for t in self.tiles:
			name_comps = t.name.split('_')
			tile_type = name_comps[1]
			tile_edges = name_comps[2]
			t.edges = {edge_types.index(e) for e in tile_edges}
			t.hitbox = t.frame.translate(x, 0)
			self.max_x = max(x + t.frame.max_x, self.max_x)
			if tile_type == 'spring':
				t.edges = {2}
				t.hitbox = sk.Rect(t.frame.x + x, t.frame.y, t.frame.w, t.frame.h/2)
		self.hazards = self.node['hazard_*_*']
		spike_insets = {'T': (0, 5, 32, 5), 'B': (32, 5, 0, 5), 'L': (0, 32, 0, 0), 'R': (0, 0, 0, 32)}
		for t in self.hazards:
			name_comps = t.name.split('_')
			hazard_type = name_comps[1]
			if hazard_type == 'spikes':
				insets = spike_insets[name_comps[-1]]
				t.hitbox = t.frame.inset(*insets).translate(x, 0)
			else:
				t.hitbox = t.frame.translate(x, 0)
		self.items = self.node['item_*']
		for i in self.items:
			i.hitbox = sk.Rect(i.position.x+x-18, i.position.y-18, 36, 36)
			i.collected = False
			i.z_position = 3
		
class Game (sk.Scene):
	def __init__(self):
		self.music = sound.Player('Music/FranticLevel.m4a')
		self.music.number_of_loops = -1
		self.music.volume = 0.1
		self.game_paused = True
		self.background_color = '#ccf4f7'
		self.tiled_bg = sk.TiledSpriteNode(bg_texture, (1024, 512))
		self.tiled_bg.position = 512, 256
		self.add_child(self.tiled_bg)
		self.t = 0
		self.ground_t = 0
		self.standing = False
		self.jump_t = 0
		self.jump_down = False
		self.game_over = False
		self.game_finished = False
		self.score = 0
		self.highscore = 0
		self.last_score = 0
		try:
			with open('.Highscore.txt', 'r') as f:
				self.highscore = int(f.read())
		except IOError:
			pass
		self.jetpack_active = False
		self.jetpack_fuel = 0
		self.v = sk.Vector2(0, 0)
		self.player_speed = 4
		self.player = player_and_effects['player'][0].__copy__()
		self.player.position = 50, 97
		self.jetpack = self.player['jetpack'][0]
		self.jetpack['jetpack_flame'][0].hidden = True
		self.jetpack.alpha = 0
		self.player.z_position = 2
		self.player_sprite = self.player['sprite'][0]
		self.foreground_layer = sk.Node()
		self.foreground_layer.x_scale = zoom
		self.foreground_layer.y_scale = zoom
		self.foreground_layer.add_child(self.player)
		self.dust_effect = player_and_effects['dust'][0].__copy__()
		self.dust_effect.num_particles_to_emit = 0
		self.foreground_layer.add_child(self.dust_effect)
		self.add_child(self.foreground_layer)
		self.levels = []
		self.load_levels()
		self.score_hud = ScoreHUD()
		self.add_child(self.score_hud)
		self.highscore_label = sk.LabelNode()
		self.highscore_label.font_name = 'Avenir Next Condensed'
		self.highscore_label.font_size = 17
		self.highscore_label.font_color = '#68c3d1'
		self.highscore_label.text = 'last: 0 / high: %i' % self.highscore
		self.add_child(self.highscore_label)
		paused_label = sk.LabelNode()
		paused_label.font_name = 'Avenir Next Condensed'
		paused_label.font_size = 50
		paused_label.text = 'Tap to play'
		self.paused_overlay = sk.SpriteNode()
		self.paused_overlay.size = 1024, 1024
		self.paused_overlay.color = (0, 0, 0, 0.4)
		self.paused_overlay.z_position = 10
		self.paused_overlay.add_child(paused_label)
		self.add_child(self.paused_overlay)
			
	def load_levels(self):
		level_names = ['Levels/Level_%i.pysk' % i for i in xrange(8)]
		level_nodes = [level.node for level in self.levels]
		map(sk.Node.remove_from_parent, level_nodes)
		self.levels = []
		self.current_level_idx = 0
		x = 0
		for name in level_names:
			level = GameLevel(name, x)
			x = level.max_x
			self.levels.append(level)
			self.foreground_layer.add_child(level.node)
		
	def did_change_size(self, old_size):
		self.score_hud.position = (36, self.size.h - 32)
		self.paused_overlay.position = self.size.w/2, self.size.h/2
		self.highscore_label.position = 90, self.size.h - 80
		
	def touch_began(self, node, touch):
		if self.game_paused:
			self.game_paused = False
			self.paused_overlay.run_action(sk.fade_out(0.3))
			self.music.play()
		if not self.game_over and self.standing:
			self.jump_down = True
			self.jump_t = self.t
			self.jump()
			self.show_dust_effect(self.player.position - (10, 32))
			self.play_sound('jump')
		elif not self.game_over and self.jetpack_fuel > 0:
			self.jetpack_active = True
			self.jetpack['jetpack_flame'][0].hidden = False
			self.play_sound('jetpack')
		if self.game_over or self.game_finished:
			self.start_new_game()
	
	def touch_ended(self, node, touch):
		self.jump_down = False
		self.jetpack_active = False
		self.jetpack['jetpack_flame'][0].hidden = True
	
	def update(self):
		if self.game_paused: return
		self.t += 1
		self.update_player()
		self.resolve_collisions()
		self.update_player_textures()
		self.collect_items()
		self.score_hud.set_score(self.score)
		self.check_hazards()
		self.update_camera()
		if self.player.position.y < 0 and not self.game_finished:
			self.player_died()
		if self.player.position.x > self.levels[-1].max_x - self.size.w:
			if not self.game_finished:
				self.game_finished = True
				self.update_highscore()
		max_x = self.levels[self.current_level_idx].max_x
		px = self.player.position.x
		if px > max_x and self.current_level_idx < len(self.levels) - 1:
			self.current_level_idx += 1
			self.player_speed += 0.33
		
	def play_sound(self, name):
		effect_name = sounds.get(name, None)
		if effect_name:
			sound.play_effect(effect_name, 0.4)
	
	def start_new_game(self):
		self.load_levels()
		gc.collect()
		self.game_over = False
		self.game_finished = False
		self.player.position = 50, 100
		self.player_speed = 4
		self.score = 0
		self.jetpack_fuel = 0
		self.jetpack.alpha = 0.0
		self.highscore_label.text = 'last: %i / high: %i' % (self.last_score, self.highscore)
	
	def update_player(self):
		max_v = sk.Vector2(self.player_speed, 15)
		a = 0.05
		v = self.v
		vx = max(-max_v.x, min(max_v.x, v.x + a * (self.player_speed - v.x)))
		vy = max(-max_v.y, min(max_v.y, v.y))
		if self.jetpack_active:
			jetpack_power = 0.5
			vy = max(-max_v.y, min(max_v.y, vy + jetpack_power))
			self.jetpack_fuel = max(0, self.jetpack_fuel - 1)
			if self.jetpack_fuel == 0:
				self.jetpack_active = False
				self.jetpack.run_action(sk.fade_out(0.3))
				self.play_sound('jetpack_empty')
		elif (not self.jump_down or self.t - self.jump_t > 15):
			vy = max(-max_v.y, min(max_v.y, vy + g))
		self.v = sk.Vector2(vx, vy)
		
	def update_player_textures(self):
		if self.game_over:
			self.player_sprite.texture = hit_texture
		elif self.standing:
			if abs(self.v.x) > 1:
				self.player_sprite.texture = walk_textures[self.t/6 % 2]
				self.jetpack.position = (-15, -22+self.t/6 % 2 * 2)
			else:
				self.player_sprite.texture = standing_texture
				self.jetpack.position = (-15, -22)
		else:
			self.player_sprite.texture = jump_texture
			self.jetpack.position = (-15, -22)
		fuel_bar = self.jetpack['jetpack_fuel_hud_full'][0]
		fuel_bar_width = (self.jetpack_fuel/300.0)*50.0
		fuel_bar.size = fuel_bar_width, 4
		fuel_bar.position = -25+16 + fuel_bar_width/2, fuel_bar.position.y
	
	def resolve_collisions(self):
		tiles = self.levels[self.current_level_idx].tiles
		p = self.player
		v = self.v
		if self.game_over:
			p.position += v
			return
		collision_tiles = []
		result_pos = list(p.position + self.v)
		result_v = list(self.v)
		p_hitbox = sk.Rect(p.position.x-16, p.position.y-31, 32, 63)
		hit_ground = False
		for a1, a2 in enumerate((1, 0)):
			if v[a1] == 0:
				continue
			d = 1.0 if v[a1] > 0 else -1.0
			p_edge = p_hitbox.max(a1) if d > 0 else p_hitbox.min(a1)
			p_edge_min, p_edge_max = (f(p_edge, p_edge+v[a1]) for f in (min, max))
			target_frame = p_hitbox.translate(v.x, v.y)
			tile_edge_idx = (a1 * 2) + (1 if v[a1] > 0 else 0)
			for tile in tiles:
				if tile_edge_idx not in tile.edges: continue
				t_frame = tile.hitbox
				if t_frame.min(a2) >= target_frame.max(a2) or t_frame.max(a2) <= target_frame.min(a2):
					continue
				tile_edge = t_frame.min(a1) if d > 0 else t_frame.max(a1)
				if p_edge_max >= tile_edge >= p_edge_min:
					if a1 == 1 and tile_edge_idx == 2:
						self.ground_t = self.t
					result_pos[a1] = tile_edge - d*p_hitbox[a1+2]/2 - d*0.5
					result_v[a1] = 0
					collision_tiles.append(tile)
					break
			v = sk.Vector2(*result_v)
		p.position = result_pos
		self.v = v
		self.standing = self.t - self.ground_t < 4
		
		for t in collision_tiles:
			if t.name.startswith('tile_spring'):
				t.texture = spring_texture2
				reset = sk.call(partial(setattr, t, 'texture', spring_texture1))
				t.run_action(sk.sequence([sk.wait(0.2), reset]))
				self.jump(24)
				self.play_sound('spring')
	
	def check_hazards(self):
		if self.game_over: return
		p_hitbox = sk.Rect(self.player.position.x-16, self.player.position.y-31, 32, 63)
		current_level = self.levels[self.current_level_idx]
		for h in current_level.hazards:
			if h.hitbox.intersects(p_hitbox):
				h.run_action(sk.repeat(sk.sequence([sk.colorize(0.6, 0.15, 'red'), sk.colorize(0.0, 0.15)]), 3))
				self.player_died()
				break
	
	def collect_items(self):
		if self.game_over: return
		p_hitbox = sk.Rect(self.player.position.x-16, self.player.position.y-31, 32, 63)
		current_level = self.levels[self.current_level_idx]
		collected = []
		for i in current_level.items:
			if not i.collected and i.hitbox.intersects(p_hitbox):
				collected.append(i)
		for i in collected:
			i.collected = True
			if i.name == 'item_coin' or i.name == 'item_fuel':
				self.play_sound('coin')
				self.score += 50
				if i.name == 'item_fuel':
					if self.jetpack_fuel == 0:
						self.jetpack.run_action(sk.fade_in(0.3))
					self.jetpack_fuel = min(300, self.jetpack_fuel + 100)
				i.run_action(sk.move_by(0, 100))
				i.run_action(sk.fade_out())
			if i.name == 'item_star':
				self.play_sound('star')
				self.score += 1000
				i.hidden = True
				stars = star_effect.__copy__()
				stars.num_particles_to_emit = 20
				stars.position = i.position
				stars.z_position = 3
				stars.advance_simulation_time(0.1)
				i.parent.add_child(stars)
	
	def player_died(self):
		if self.game_over: return
		self.jetpack_active = False
		self.player_speed = 0
		self.v = sk.Vector2(0, 0)
		self.jump(7)
		self.game_over = True
		self.play_sound('die')
		self.update_highscore()
	
	def update_highscore(self):
		self.last_score = self.score
		if self.score > self.highscore:
			self.highscore = self.score
			with open('.Highscore.txt', 'w') as f:
				f.write(str(self.highscore))
			self.highscore_label.text = 'New Highscore!'
	
	def update_camera(self):
		if self.game_finished: return
		player_pos = self.player.position
		center = sk.Point(self.size.w/5 / zoom, self.size.h/2/zoom)
		cam_pos = min(0, center.x - player_pos.x), min(0, center.y - player_pos.y)
		cam_pos = (cam_pos[0] * zoom, cam_pos[1] * zoom)
		self.foreground_layer.position = cam_pos
		self.tiled_bg.tile_offset = ((-self.foreground_layer.position.x * 0.75) % 512.0, 0)
		self.tiled_bg.position = (512, 256 + cam_pos[1] * 0.75)
	
	def show_dust_effect(self, pos):
		self.dust_effect.num_particles_to_emit = 5
		self.dust_effect.position = pos
		self.dust_effect.reset_simulation()
		self.dust_effect.advance_simulation_time(0.2)
		
	def jump(self, strength=6.5):
		self.v = sk.Vector2(self.v.x, min(15, strength))
		self.standing = False
		self.ground_t = 0
	
	def did_stop(self):
		self.music.stop()

scene_view = sk.View()
game = Game()
scene_view.run_scene(game)
scene_view.present(orientations=['landscape'])