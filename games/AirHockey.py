# Hockey
#
# A air hockey game for two players. First to
# seven wins.
# Most of the game is drawn with the scene
# module. Goal and winner messages are animated
# with layers. 

from scene import *
from sound import *
from copy import copy


class Player (object):
	def __init__(self, name, color):
		self.color = color
		self.score = 0
		self.name = name

	def __str__(self):
		return self.name


class Puck (object):
	def __init__(self, pos, scene):
		self.vector = Vector3(0, 0, 0)
		self.pos = pos

	def reverse_vector(self):
		v = self.vector
		self.vector = Vector3(-v.x, -v.y, 0)


class HockeyScene (Scene):
	def setup(self):
		self.left_player = Player("Red Player", Color(1, 0, 0))
		self.right_player = Player("Blue Player", Color(0, 0, 1))
		self.players = (self.left_player, self.right_player)

		for s in ('Drums_06', 'Woosh_1', 'Powerup_2'):
			load_effect(s)

		center = self.size.w / 2
		middle = self.size.h / 2
		
		# goal height
		gh = self.size.h / 4
		
		self.puck_radius = gh / 2.5
		self.puck = self.centered_puck()
		# the last time the puck was hit. Used to animate its slow down
		self.puck_start_t = 0
		pr = self.puck_radius

		self.line_width = self.puck_radius / 6
		lw = self.line_width
		
		self.red_line = Rect(center - lw / 2, 0, lw, self.size.h)
		
		self.red_circle = Rect(w=gh, h=gh)
		self.red_circle.center(self.bounds.center())
		
		self.left_goal = Rect(w=gh, h=gh)
		self.right_goal = Rect(w=gh, h=gh)
		self.left_goal.center(0, middle)
		self.right_goal.center(self.size.w, middle)

		# when someone reaches 7 goals, save them to show a message
		self.winner = None 


	def score_goal(self, player):
		player.score += 1

		self.puck = self.centered_puck()

		for p in self.players:
			if p.score >= 7:
				self.winner = p
				break

		overlay = Layer(self.bounds)
		def hide_overlay():
			overlay.animate('alpha', 0.0, 1, completion=lambda: overlay.remove_layer())

		if self.winner:
			message = "%s Wins" % (self.winner)
			on_completion = None
			self.hide_overlay = hide_overlay
		else: 
			message = "Goal!"
			on_completion = hide_overlay
			# restart the puck on the other player's side
			if player == self.left_player:
				self.puck.pos.x += self.size.w / 4 + self.puck_radius
			else:
				self.puck.pos.x -= self.size.w / 4 + self.puck_radius

		size = self.puck_radius * 1.5
		text_layer = TextLayer(message, 'Futura', size)
		text_layer.frame.center(self.bounds.center())
		text_layer.frame.y += self.size.h / 4
		text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		overlay.add_layer(text_layer)

		start_color, end_color = copy(player.color), copy(player.color)
		start_color.a = 0
		end_color.a = .5
		overlay.background = start_color
		overlay.animate('background', end_color, .7, completion=on_completion)
		self.add_layer(overlay)
		play_effect('Woosh_1')


	def centered_puck(self):
		pos = Rect(w=self.puck_radius, h=self.puck_radius)
		pos.center(self.bounds.center())
		return Puck(pos, self)


	def move_puck(self):
		puck = self.puck

		ease_x = (self.t - self.puck_start_t) / 4.0
		ease = max(0, 1 - curve_ease_out(ease_x))

		puck.pos.x += puck.vector.x * ease
		puck.pos.y += puck.vector.y * ease

		if puck.pos.right() > self.size.w and not puck.pos.intersects(self.right_goal):
			puck.vector.x *= -1
			play_effect('Drums_06')
			puck.pos.x = min(self.size.w - puck.pos.w, puck.pos.x)

		if puck.pos.left() > self.size.w:
			self.score_goal(self.left_player)
			return

		if puck.pos.left() < 0 and not puck.pos.intersects(self.left_goal):
			puck.vector.x *= -1
			play_effect('Drums_06')
			puck.pos.x = max(0, puck.pos.x)

		if puck.pos.right() < 0:
			self.score_goal(self.right_player)
			return

		if puck.pos.top() > self.size.h or puck.pos.bottom() < 0: 
			puck.vector.y *= -1
			play_effect('Drums_06')
			puck.pos.y = max(0, puck.pos.y)
			puck.pos.y = min(self.size.h - puck.pos.h, puck.pos.y)


	def draw(self):
		stroke_weight(self.line_width)
		background(1, 1, 1)

		# red lines on ice in middle
		stroke(1.00, 0.40, 0.40)
		fill(1.00, 0.40, 0.40)
		rect(*self.red_line.as_tuple())
		fill(1, 1, 1)
		ellipse(*self.red_circle.as_tuple())

		# red goal markers
		for goal in (self.left_goal, self.right_goal):
			rect(*goal.as_tuple())

		for touch in self.touches.values():
			self.handle_touch(touch)

		# black puck
		no_stroke()
		fill(0, 0, 0)
		ellipse(*self.puck.pos.as_tuple())

		self.draw_scores()

		self.move_puck()

		if self.root_layer:
			self.root_layer.update(self.dt)
			self.root_layer.draw()

		if self.winner is not None:
			c = Rect()
			c.center(self.bounds.center())
			tint(1, 1, 1)
			message = "Tap to Play Again"
			y_offset = self.size.h / 4
			size = self.puck_radius
			text(message, x=c.x, y=c.y-y_offset, font_size=size, font_name='Futura')


	def draw_scores(self):
		for p, x in zip(self.players, (50, self.size.w - 50)):
			tint(*p.color.as_tuple())
			text(str(p.score), x=x, y=self.size.h- 50, font_size=32, font_name='Futura')


	def handle_touch(self, touch):
		if self.winner:
			# check for Winner overlay and clear.
			# This is Tap to Play Again
			self.winner = None
			self.hide_overlay()
			del self.hide_overlay
			self.left_player.score = 0
			self.right_player.score = 0
			return

		tx = touch.location.x
		ty = touch.location.y
		finger = Rect(tx - 20, ty - 20, 40, 40)

		if finger.intersects(self.puck.pos):
			dx = tx - touch.prev_location.x
			dy = ty - touch.prev_location.y

			# Super simple richochet off "unmoving" finger. Just reverse it
			if abs(dx) < 5 and abs(dy) < 5:
				self.puck.reverse_vector()
				# Slide puck out from the finger. No puck holding.
				if dx == 0: dx = self.puck.vector.x
				if dy == 0: dy = self.puck.vector.y
				if not any([dx, dy]): return
				while finger.intersects(self.puck.pos):
					self.puck.pos.x += dx
					self.puck.pos.y += dy
			else:
				self.step = 0
				self.puck_start_t = self.t
				self.puck.vector = Vector3(dx * .8, dy * .8, 0)
				self.puck.pos.x += dx
				self.puck.pos.y += dy


run(HockeyScene(), LANDSCAPE)