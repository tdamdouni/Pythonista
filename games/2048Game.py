# coding: utf-8

# 2048-for-Pythonista
# A 2048 game for the Pythonista beta 1.6
# ![screenshot](https://www.dropbox.com/s/zabjgrtw7hqilen/2048-screenshot.PNG?raw=1)

# https://github.com/SebastianJarsve/2048-for-Pythonista

import os
import cPickle
import random

import ui
import scene
import sound
import dialogs

A = scene.Action

NORTH, SOUTH, EAST, WEST = range(4)
VERTICAL = NORTH, SOUTH
HOROZINTAL = EAST, WEST

SAVE_FOLDER = './saves/'
SCORE_FOLDER = SAVE_FOLDER + 'highscore/'
STATE_FOLDER = SAVE_FOLDER + 'save-state/'


class ButtonNode (scene.SpriteNode):
	def __init__(self, title, *args, **kwargs):
		scene.SpriteNode.__init__(self, 'pzl:Button1', *args, **kwargs)
		button_font = ('Avenir Next', 20)
		self.title_label = scene.LabelNode(
			title,
			font=button_font,
			color='black',
			position=(0, 1),
			parent=self
		)
		self.title = title
			

class MenuScene (scene.Scene):
	def __init__(self, title, subtitle, button_titles):
		scene.Scene.__init__(self)
		self.title = title
		self.subtitle = subtitle
		self.button_titles = button_titles
		
	def setup(self):
		button_font = ('Avenir Next', 20)
		title_font = ('Avenir Next', 36)
		num_buttons = len(self.button_titles)
		self.bg = scene.SpriteNode(color='#000000', parent=self)
		bg_shape = ui.Path.rounded_rect(0, 0, 240, num_buttons * 64 + 140, 8)
		bg_shape.line_width = 4
		shadow = ((0, 0, 0, 0.35), 0, 0, 24)
		self.menu_bg = scene.ShapeNode(
			bg_shape,
			'#BBADA0',
			'#CDC1B4',
			shadow=shadow,
			parent=self
		)
		self.title_label = scene.LabelNode(
			self.title,
			font=title_font,
			color='#000000',
			position=(0, self.menu_bg.size.h/2 - 40),
			parent=self.menu_bg
		)
		self.title_label.anchor_point = (0.5, 1)
		self.subtitle_label = scene.LabelNode(
			self.subtitle,
			font=button_font,
			position=(0, self.menu_bg.size.h/2 - 100),
			color='#000000',
			parent=self.menu_bg
		)
		self.subtitle_label.anchor_point = (0.5, 1)
		self.buttons = []
		for i, title in enumerate(reversed(self.button_titles)):
			btn = ButtonNode(title, parent=self.menu_bg)
			btn.position = 0, i * 64 - (num_buttons-1) * 32 - 50
			self.buttons.append(btn)
		self.did_change_size()
		self.menu_bg.scale = 0
		self.bg.alpha = 0
		self.bg.run_action(A.fade_to(0.4))
		self.menu_bg.run_action(A.scale_to(1, 0.3, scene.TIMING_EASE_OUT_2))
		self.background_color = '#FFFFFF'
		
	def did_change_size(self):
		self.bg.size = self.size + (2, 2)
		self.bg.position = self.size/2
		self.menu_bg.position = self.size/2
	
	def touch_began(self, touch):
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		for btn in self.buttons:
			if touch_loc in btn.frame:
				sound.play_effect('8ve:8ve-tap-resonant')
				btn.texture = scene.Texture('pzl:Button2')
				
	def touch_moved(self, touch):
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		for btn in self.buttons:
			if touch_loc in btn.frame:
				btn.texture = scene.Texture('pzl:Button2')
			else:
				btn.texture = scene.Texture('pzl:Button1')
	
	def touch_ended(self, touch):
		touch_loc = self.menu_bg.point_from_scene(touch.location)
		if touch.location not in self.menu_bg.frame:
			self.presenting_scene.dismiss_modal_scene()
		for btn in self.buttons:
			btn.texture = scene.Texture('pzl:Button1')
			if self.presenting_scene and touch_loc in btn.frame:
				new_title = self.presenting_scene.menu_button_selected(btn.title)
				if new_title:
					btn.title = new_title
					btn.title_label.text = new_title


class Tile (scene.ShapeNode):
	def __init__(self, frame, *args, **kwargs):
		x, y, w, h = frame
		path = ui.Path.rect(0, 0, w, h)
		path.line_width = 10
		scene.ShapeNode.__init__(
			self,
			path=path,
			position=(x, y),
			stroke_color='#BBADA0',
			fill_color=(0,0,0,0),
			*args, **kwargs
		)
		self.value = 0
		self.blocked = False
		self.label = self.create_label_node()
		self.update()
		
	def create_label_node(self):
		text = str(self.value) if self.value else ''
		label = scene.LabelNode(
			text,
			font=('Arial', self.size.w*0.25),
			size=self.size, position=(0, 0)
		)
		label.color = '#FFFFFF'
		self.add_child(label)
		return label
		
	def update(self):
		self.label.text = str(self.value) if self.value else ''
		fill_colors = {
			0:'#CDC1B4', 2:'#EEE4DA', 4:'#EDE0C8', 8:'#F2B179',
			16:'#F59563', 32:'#F67C5F', 64:'#F65E3B', 128:'#EDCF72',
			256:'#EDCC61', 512:'#EDC850', 1024:'#EDC53F', 2048:'#EDC22E'
		}
		self.fill_color = '#222222'
		if self.value in fill_colors:
			self.fill_color = fill_colors[self.value]
		self.label.color = '#222222' if self.value < 8 else '#FFFFFF'
		
	def reset(self):
		self.value = 0

	def block(self):
		self.blocked = True

	def unblock(self):
		self.blocked = False


class Board (scene.Node):
	def __init__(self, size, *args, **kwargs):
		scene.Node.__init__(self, *args, **kwargs)
		self.size = size
		w = self.parent.size.w/size
		h = self.parent.size.w/size
		self.tiles = [[Tile((x*w+w/2, y*h+h/2, w, h), parent=self)
								for x in range(size)] for y in range(size)]
		for t in self:
			self.add_child(t)

	def __getitem__(self, location):
		x, y = location
		return self.tiles[y][x]

	def __setitem__(self, location, items):
		x, y = location
		for key, value in items.items():
			setattr(self[x, y], key, value)
		
	def __len__(self):
		return self.size**2

	def __iter__(self):
		return iter([tile for row in self.tiles for tile in row])
		
	def __contains__(self, value):
		for t in self:
			if t.value == value:
				return True
		return False
		
	def get_filename(self):
		s = self.parent.board_size
		return STATE_FOLDER + '{}-{}x{}.txt'.format(self.parent.player, s, s)
		
	def load_state(self):
		filename = self.get_filename()
		if not os.path.exists(filename):
			self.parent._new_game()
			self.parent.score_board.load_highscore()
			return
		with open(filename, 'r') as f:
			state = cPickle.load(f)
			for i, t in enumerate(self):
				t.value = state[i]
				t.update()
			self.parent.score_board.score = state['score']
			self.parent.score_board.load_highscore()
			self.parent.score_board.update()
		
	def save_state(self):
		state = {'score':self.parent.score_board.score}
		for i, t in enumerate(self):
			state[i] = t.value
		filename = self.get_filename()
		with open(filename, 'w') as f:
			cPickle.dump(state, f)

	def test_add(self, x, y, value):
		if x < 0 or x > self.size-1 or y < 0 or y > self.size-1:
			return False
		return self[x, y].value == value

	def can_move(self):
		if 0 in self:
			return True

		for y in range(self.size):
			for x in range(self.size):
				if self.test_add(x+1, y, self[x, y].value):
					return True
				elif self.test_add(x-1, y, self[x, y].value):
					return True
				elif self.test_add(x, y+1, self[x, y].value):
					return True
				elif self.test_add(x, y-1, self[x, y].value):
					return True
		return False

	def reset(self):
		for t in self:
			t.reset()
			t.update()
		
	def set_size(self, size):
		for t in self:
			t.remove_from_parent()
		w = self.parent.size.w/size
		h = self.parent.size.w/size
		self.size = size
		self.tiles = [[Tile((x*w+w/2, y*h+h/2, w, h), parent=self)
								for x in range(size)] for y in range(size)]
		for t in self:
			self.add_child(t)
		self.load_state()


class ScoreBoard (scene.ShapeNode):
	def __init__(self, *args, **kwargs):
		w = scene.get_screen_size().w*0.8
		h = scene.get_screen_size().h*0.25
		path = ui.Path.rounded_rect(0, 0, w, h, 10)
		path.line_width = 8
		scene.ShapeNode.__init__(
			self, path=path,
			fill_color='#CDC1B4',
			stroke_color='#BBADA0',
			*args, **kwargs
		)
		board = self.parent.board
		box = scene.Rect(
			board.bbox.x, board.bbox.y+board.bbox.h,
			board.bbox.w, self.parent.size.h-board.bbox.h
		)
		self.position = box.center()
		self.score = 0
		self.highscore = dict()
		self.load_highscore()
		self.score_label = self.create_score_label()
		self.highscore_label = self.create_highscore_label()
		self.create_title_label()
		self.player_label = self.create_player_label()
		
	def get_top_list(self):
		size = self.parent.board.size
		suffix = '-{}x{}.txt'.format(size, size)
		scores = dict()
		template = '{} - {}\n'
		for filename in os.listdir(SCORE_FOLDER):
			if not filename.endswith(suffix):
				continue
			with open(SCORE_FOLDER+filename, 'r') as f:
				scores[filename.replace(suffix, '')]=cPickle.load(f)['score']
		txt = ''
		for k, v in sorted(scores.items(), reverse=1):
			txt += template.format(k, v)
		return txt
		
	def get_filename(self):
		s = self.parent.board_size
		return SCORE_FOLDER + '{}-{}x{}.txt'.format(self.parent.player, s, s)

	def load_highscore(self):
		filename = self.get_filename()
		if os.path.exists(filename):
			with open(filename, 'r') as f:
				self.highscore = cPickle.load(f)
				return 
		self.highscore = {'score':0, 'tile':0}
		
	def save_highscore(self):
		filename = self.get_filename()
		with open(filename, 'w') as f:
			cPickle.dump(self.highscore, f)
		
	def create_title_label(self):
		label = scene.LabelNode('2048', ('Arial', self.bbox.w*0.15))
		label.anchor_point = (0, 0.5)
		label.position = (-self.bbox.w/2+20, self.bbox.h/2-label.bbox.h/2-10)
		self.add_child(label)
		
	def create_player_label(self):
		label = scene.LabelNode(
			self.parent.player,
			('Arial', self.bbox.w*0.1)
		)
		label.anchor_point = (0, 0)
		label.position = (0, label.bbox.h/2+15)
		self.add_child(label)
		return label
		
	def create_score_label(self):
		label = scene.LabelNode(
			'Score: '+str(self.score),
			('Arial', self.bbox.w*0.08)
		)
		label.anchor_point = (0, 0.5)
		label.position = (-self.bbox.w/2+10, -self.bbox.h*0.2)
		self.add_child(label)
		return label
		
	def create_highscore_label(self):
		size = str(self.parent.board.size)
		label = scene.LabelNode(
			'Highscore: '+str(self.highscore['score']),
			('Arial', self.bbox.w*0.08)
		)
		label.anchor_point = (0, 0.5)
		label.position = (0-self.bbox.w/2+10, -self.bbox.h*0.35)
		self.add_child(label)
		return label
		
	def update(self, value=0):
		size = str(self.parent.board.size)
		self.score += value
		self.score_label.text = 'Score: ' + str(self.score)
		self.highscore_label.text = 'Highscore: '+str(self.highscore['score'])
		if self.score > self.highscore['score']:
			self.highscore['score'] = self.score
			self.highscore_label.text = 'Highscore: ' + str(self.score)
			#self.save_highscore()


class GameScene (scene.Scene):
	def setup(self):
		sound.set_volume(1)
		self.folder_setup()
		self.player = 'Player'
		self.moved = False
		self.background_color = '#00002A'
		self.first_touch = None
		self.board_size = 3
		self.load_game()
		
		self.board = Board(self.board_size, parent=self)
		self.score_board = ScoreBoard(parent=self)
		self.add_child(self.board)
		self.add_child(self.score_board)
		
		self.score_board.load_highscore()
		self.board.load_state()
		
		self.show_menu()
		
	def load_game(self):
		filename = SAVE_FOLDER+'game.txt'
		if os.path.exists(filename):
			with open(filename, 'r') as f:
				game = cPickle.load(f)
				for k, v in game.items():
					setattr(self, k, v)
		
	def save_game(self):
		filename = SAVE_FOLDER+'game.txt'
		with open(filename, 'w') as f:
			game = {'player':self.player, 'board_size':self.board.size}
			cPickle.dump(game, f)
		
	def folder_setup(self):
		for folder in [SAVE_FOLDER, STATE_FOLDER, SCORE_FOLDER]:
			if not os.path.exists(folder):
				os.mkdir(folder)
		
	def _new_game(self):
		self.score_board.score = 0
		self.score_board.update()
		self.board.reset()
		self.add_tile()
		self.add_tile()

	def add_tile(self, value=None):
		if not value:
			value = 2 if random.random() <= 0.8 else 4
		x = random.randrange(self.board.size)
		y = random.randrange(self.board.size)
		while self.board[x, y].value:
			x = random.randrange(self.board.size)
			y = random.randrange(self.board.size)
		self.board[x, y] = {"value":value}
		self.board[x, y].update()

	def _move(self, x, y, direction):
		d = [-1, 1, 1, -1][direction]
		current = self.board[x, y]
		if direction in VERTICAL:
			new = self.board[x, y+d]
		else:
			new = self.board[x+d, y]
		if (new.value and new.value == current.value and not new.blocked
				and not current.blocked):
			current.value = 0
			new.value *= 2
			new.blocked = True
			self.score_board.update(new.value)
			self.moved = True
		elif not new.value and current.value:
			new.value = current.value
			current.value = 0
			self.moved = True
		current.update()
		new.update()
		if direction in VERTICAL:
			if d > 0 and y+d < self.board.size-1 or d < 0 and y+d > 0:
				self._move(x, y+d, direction)
		else:
			if d > 0 and x+d < self.board.size-1 or d < 0 and x+d > 0:
				self._move(x+d, y, direction)

	def move(self, direction):
		self.moved = False
		
		i_ranges = [
			range(self.board.size),
			range(self.board.size),
			range(self.board.size-2, -1, -1),
			range(1, self.board.size)
		]
		j_ranges = [
			range(1, self.board.size),
			range(self.board.size-2, -1, -1),
			range(self.board.size),
			range(self.board.size)
		]
		for i in i_ranges[direction]:
			for j in j_ranges[direction]:
				if self.board[i, j].value:
					self._move(i, j, direction)
					
		if self.moved:
			self.add_tile()

		for t in self.board:
			t.unblock()
			
	def show_menu(self):
		self.present_modal_scene(
			MenuScene(
				'Menu',
				'This is a 2048 game!',[
					'Continue',
					'New Game',
					'Board size',
					'Change player',
					'Highscores'
				]
			)
		)
		
	def change_player(self):
		self.player = dialogs.input_alert('Player:', '', self.player, 'Ok')
		self.player = self.player if self.player else 'Player'
		self.score_board.player_label.text = self.player
		self.score_board.load_highscore()
		self.board.load_state()
			
	def menu_button_selected(self, title):
		if title in ['Dismiss', 'Continue']:
			pass
		elif title in ['Restart', 'New Game']:
			self._new_game()
		elif title == 'Board size':
			self.dismiss_modal_scene()
			action = lambda: self.present_modal_scene(
				MenuScene(
					title,
					'',
					['3x3', '4x4', '5x5', 'Custom']
				)
			)
			self.delay(0.1, action)
		elif title == 'Custom':
			try:
				size = int(dialogs.input_alert('Board size:', '', '4'))
				size = max(2, min(8, size))
				self.board_size = size
				self.board.set_size(size)
			except ValueError:
				dialogs.hud_alert(
					'Invalid input: Use a single integer', 'error', 2
				)
				return 
			except KeyboardInterrupt:
				return 
		elif title[0].isdigit():
			size = int(title[0])
			self.board_size = size
			self.board.set_size(size)
		elif 'player' in title:
			try:
				self.change_player()
			except KeyboardInterrupt:
				pass
			return 
		elif title in ['Highscores']:
			self.dismiss_modal_scene()
			action = lambda: self.present_modal_scene(
				MenuScene(title, self.score_board.get_top_list(), [])
			)
			self.delay(0.1, action)
		else:
			return 
		self.dismiss_modal_scene()

	def persistence_saving(self):
		if self.score_board.score > self.score_board.highscore:
			self.score_board.save_highscore()
		self.board.save_state()
		self.save_game()

	def pause(self):
		self.persistence_saving()
		
	def stop(self):
		self.persistence_saving()

	def touch_began(self, touch):
		self.first_touch = touch
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		old = self.first_touch.location
		new = touch.location
		if abs(old - new) < 30:
			if touch.location in self.score_board.frame:
				self.show_menu()
		else:
			if abs(old.x - new.x) > abs(old.y - new.y):
				if old.x - new.x > 0:
					self.move(WEST)
				else:
					self.move(EAST)
			else:
				if old.y - new.y > 0:
					self.move(NORTH)
				else:
					self.move(SOUTH)
		if not self.board.can_move() and touch.location in self.board.bbox:
			self.delay(0.2, lambda: self.present_modal_scene(
				MenuScene('Game Over', 'Play again?', ['New Game']))
			)


if __name__ == '__main__':
	scene.run(GameScene(), scene.PORTRAIT, show_fps=True)