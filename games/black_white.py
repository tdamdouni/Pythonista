# coding: utf-8

# https://gist.github.com/chriswilson1982/b45974c547c493d590a8

# https://forum.omz-software.com/topic/2718/crash-when-using-sleep-in-scene-module/3

from scene import *
import console
import sound
from random import choice, randint
from time import sleep
from math import pi


# Ideas!
# Timer and visual representation
# Changing (progressive vs random) grid sizes
# Level counter
# High score table (console or dialog module)
# Info and exit pages (console or dialog module)
# Bonus points for no whites
# Message board below title


#---Rows & Columns
rows = 10
cols = 6

#---Colour Setup
color1 = "#000000"
color2 = "#ffffff"
color3 = "#ff0000"
color4 = "#00ff00"
background_color = "#ffffff"
timer_color = '#dfdfdf'
colors = (color1, color2)
all_colors = (color1, color2, color3, color4)

#---Screen Size Setup
screen_w, screen_h = get_screen_size()
centre = (screen_w / 2, screen_h / 2)
square_size = int(screen_w / 8)
top_left = (screen_w / 2.0 - square_size * (cols / 2.0 - 0.5), (screen_h / 2 + square_size * (rows / 2.0 - 0.5)))

#---Sounds
tap_sound = 'digital:PepSound2'
button_sound = 'ui:click1'
win_sound = 'digital:PowerUp1'
fail_sound = 'digital:ZapThreeToneDown'
no_white_sound = 'digital:PowerUp11'
new_game_sound = 'digital:PowerUp5'

#---Actions
A = Action
pressed_action = A.sequence(A.scale_to(1.2, 0.2), A.scale_to(1.0, 0.2))
toggle_action = A.sequence(A.group(A.scale_to(0.8, 0.2), A.rotate_by(pi / 2, 0.2)), A.scale_to(1.0, 0.2))
go_action = A.sequence(A.scale_to(2, 0.01), A.scale_to(1.0, 0.1))
score_action = A.sequence(A.move_by(0, screen_h / 2 - 100, 1, TIMING_EASE_OUT_2), A.wait(2), A.fade_to(0, 0.5), A.remove())


#---Classes
class Game (Scene):
	def setup(self):
		self.background_color = background_color
		
		self.title = LabelNode("black & white", font = ('Helvetica', 40), color = "black", position = (screen_w / 2, screen_h - 50))
		self.add_child(self.title)
		
		self.black_count = LabelNode("0", font = ('Helvetica', 30), color = color2, position = (-100, -100), z_position = 0.5)
		self.add_child(self.black_count)
		
		self.white_count = LabelNode("0", font = ('Helvetica', 30), color = color1, position = (-100, -100), z_position = 0.5)
		self.add_child(self.white_count)
		
		self.backdrop1 = SpriteNode(color = color1, position = centre, size = (square_size * cols + 20, square_size * rows + 20))
		self.add_child(self.backdrop1)
		
		self.backdrop2 = SpriteNode(color = color2, position = centre, size = (square_size * cols + 10, square_size * rows + 10))
		self.backdrop2.z_position = 0.1
		self.add_child(self.backdrop2)
		
		horizontal = top_left[0]
		vertical = top_left[1]
		self.squares = []
		for x in range(cols):
			for y in range(rows):
				self.square = Square(col = x + 1, row = y + 1, position = (horizontal, vertical), size = (square_size, square_size), state = choice((1, 2)), color = None)
				self.add_child(self.square)
				self.squares.append(self.square)
				vertical -= square_size
			vertical = top_left[1]
			horizontal += square_size
		
		self.start = StartFinish(row = randint(1, rows), type = "start")
		self.add_child(self.start)

		self.finish = StartFinish(row = randint(1, rows), type = "finish")
		self.add_child(self.finish)
		
		self.backdrop3a = SpriteNode(position = self.start.position, size = (2 * square_size, square_size + 10), color = color1)
		self.backdrop3a.anchor_point = self.start.anchor_point
		self.add_child(self.backdrop3a)
		
		self.backdrop3b = SpriteNode(position = self.finish.position, size = (2 * square_size, square_size + 10), color = color1)
		self.backdrop3b.anchor_point = self.finish.anchor_point
		self.add_child(self.backdrop3b)
		
		self.backdrop4 = SpriteNode(color = color1, position = (screen_w / 2, 50), size = (2 * square_size, 50))
		self.backdrop4.z_position = 0.7
		self.add_child(self.backdrop4)
		
		self.backdrop5 = SpriteNode(color = color4, position = (screen_w / 2, 50), size = (2 * square_size - 10, 40))
		self.backdrop5.z_position = 0.7
		self.add_child(self.backdrop5)
		
		self.commit_button = LabelNode("GO", font = ('Helvetica', 30), color = color1, position = (screen_w / 2, 50), size = (square_size, square_size))
		self.commit_button.z_position = 0.7
		self.add_child(self.commit_button)
		
		self.restart_button = SpriteNode(texture = Texture('iob:ios7_refresh_32'), position = (screen_w - square_size * 1.5, 50), scale = 1)
		self.add_child(self.restart_button)
		
		self.score = LabelNode("0", font = ('Helvetica', 40), color = "black", position = (square_size * 1.5, 50), size = (square_size, square_size), z_position = 0.7)
		self.add_child(self.score)
		
		self.can_play = True
		self.win = False
		self.no_whites = False
		self.green_list = []
		
		self.new_game(False)
		
		
	def commit(self):
		self.can_play = False
		sound.play_effect(button_sound)
		for square in self.squares:
			if square.row == self.start.row and square.col == 1 and square.state == 2:
				square.state = 3
				square.color = color4
				self.go(square)
				return
			elif square.row == self.start.row and square.col == 1 and square.state != 2:
				self.check_win()

	
	@ui.in_background
	def go(self, start_square):
		try:
			self.green_list.remove(start_square)
		except:
			pass
		for square in start_square.white_neighbours(self.squares):
			self.green_list.append(square)
			square.run_action(go_action)
			square.state = 3
			square.color = color4
			sleep(0.004)
			self.go(square)
		if len(self.green_list) == 0:
			sleep(0.004)
			self.check_win()


	def check_win(self):
		self.can_play = False
		for square in self.squares:
			square.rotation = 0.0
			if square.row == self.finish.row and square.col == cols:
				if square.state == 3:
					square.state = 4
					self.win = True
					self.can_play = False
					self.winning()
					return
				elif square.state == 4:
					return		
		self.can_play = False
		self.losing()


	def winning(self):
		black_list = []
		white_list = []
		add_score = 0
		for square in self.squares:
			square.run_action(toggle_action)
			if square.state == 1:
				black_list.append(square)
			elif square.state == 2:
				white_list.append(square)
			elif square.state >= 3:
				add_score += 1
		self.black_count.text = str(len(black_list))
		self.white_count.text = str(len(white_list))

		self.score_change(add_score, self.win)
		self.restart_button.texture = Texture('iob:checkmark_circled_32')
		self.restart_button.run_action(A.repeat(A.sequence(A.scale_to(2, 0.5), A.scale_to(1, 0.5)), 5))
		
		self.move_counters()
		
		if self.no_whites:
			sound.play_effect(no_white_sound)
			self.score_label2.text = "no whites!"
			self.score_label2.font = ('Helvetica', 30)
			self.score_label_back.size = (4 * square_size, 4 * square_size)
		else:
			sound.play_effect(win_sound)
			

	def losing(self):
		sound.play_effect(fail_sound)
		for square in self.squares:
			if square.state == 3:
				square.state = 0
				square.color = color3
			self.start.color = color3
			self.finish.color = color3
		self.score_change(-1 * int(self.score.text), self.win)
		self.score.text = "0"
		self.backdrop5.color = color3
		self.move_counters()


	def score_change(self, num, win):
		if num > 0:
			text = "+"+str(num)
		elif num < 0:
			text = str(num)
		else:
			text = ""
		
		red_count = 0
		for square in self.squares:
			if square.state == 0:
				red_count += 1
		if win:	
			self.score_label1 = LabelNode(text, font = ('Helvetica', 40), color = color4, position = (screen_w / 2, 150), size = (square_size, square_size), z_position = 0.6)
			self.add_child(self.score_label1)
			self.score_label1.run_action(score_action)
		
			self.score_label2 = LabelNode("-"+str(self.white_count.text), font = ('Helvetica', 40), color = color2, position = (screen_w / 2, 100), size = (square_size, square_size), z_position = 0.6)
			self.add_child(self.score_label2)
			self.score_label2.run_action(score_action)
	
			self.score_label3 = LabelNode("-"+str(red_count), font = ('Helvetica', 40), color = color3, position = (screen_w / 2, 50), size = (square_size, square_size), z_position = 0.6)
			self.add_child(self.score_label3)
			self.score_label3.run_action(score_action)
		
			self.score_label_back = SpriteNode(color = color1, size = (4 * square_size, 4 * square_size), position = (screen_w / 2, 100), alpha = 0.8)
			self.score_label_back.z_position = 0.59
			self.add_child(self.score_label_back)
			self.score_label_back.run_action(score_action)
		
		total_score_change = num - int(self.white_count.text) - red_count
		if win:
			self.score.text = str(int(self.score.text) + total_score_change)
		else:
			total_score_change = -1 * int(self.score.text)
		
		if win:
			self.total_score_change_label = LabelNode("+"+str(total_score_change), font = ('Helvetica', 40), color = color4, position = self.score.position)
			if total_score_change < 0:
				self.total_score_change_label.text = str(total_score_change)
				self.total_score_change_label.color = color3
		elif not win:
			self.total_score_change_label = LabelNode(str(total_score_change), font = ('Helvetica', 40), color = color3, position = self.score.position)
		self.add_child(self.total_score_change_label)
		self.total_score_change_label.run_action(A.sequence(A.fade_to(1, 0.1), A.wait(1), A.move_to(screen_w / 2, 50, 2, TIMING_EASE_IN_OUT), A.remove()))
		self.score.run_action(A.sequence(A.fade_to(0, 0), A.wait(1.5),A.fade_to(1, 0.5)))


	def new_game(self, win):
		self.can_play = False
		self.win = False
		
		self.start.row = randint(1, rows)
		self.start.color = color4
		self.finish.row = randint(1, rows)
		self.finish.color = color4
		self.backdrop5.color = color4
		
		self.make_grid()
		
		self.move_counters()
		
		try:
			for item in (self.score_label1, self.score_label2, self.score_label3, self.score_label_back):
				item.run_action(A.remove())
		except:
			pass
		self.start.run_action(A.move_to(top_left[0] - square_size, top_left[1] - square_size * (self.start.row - 1)))
		self.finish.run_action(A.move_to(top_left[0] + square_size * cols, top_left[1] - square_size * (self.finish.row - 1)))
		
		self.backdrop3a.run_action(A.move_to(top_left[0] - square_size, top_left[1] - square_size * (self.start.row - 1)))
		
		self.backdrop3b.run_action(A.move_to(top_left[0] + square_size * cols, top_left[1] - square_size * (self.finish.row - 1)))
		
		self.restart_button.texture = Texture('iob:ios7_refresh_32')
		self.restart_button.scale = 1
		self.restart_button.remove_all_actions()
		
		if not win:
			self.score.text = "0"
		
		self.can_play = True
		self.no_whites = False
		
		sound.play_effect(new_game_sound)

	@ui.in_background
	def make_grid(self):
		for square in self.squares:
			square.state = choice((1, 2))
			if square.state == 1:
				square.color = color1
			elif square.state == 2:
				square.color = color2
			square.run_action(toggle_action)
			sleep(0.002)

	def move_counters(self):
		black_list = []
		white_list = []
		for square in self.squares:
			if square.state == 1:
				black_list.append(square)
			elif square.state == 2:
				white_list.append(square)
		try:
			b = choice(black_list)
			w = choice(white_list)
		except:
			self.black_count.text = str(len(black_list))
			self.white_count.text = str(len(white_list))
			if len(black_list) == 0:
				self.black_count.position = (-100, -100)
			elif len(white_list) == 0:
				self.white_count.position = (-100, -100)
				self.no_whites = True
			return
		self.black_count.position = b.position
		self.white_count.position = w.position
		self.black_count.text = str(len(black_list))
		self.white_count.text = str(len(white_list))


	def did_change_size(self):
		pass

	def update(self):
		pass
	
	def touch_began(self, touch):
		if touch.location in self.backdrop5.bbox and self.can_play:
			self.commit_button.run_action(pressed_action)
			self.backdrop4.run_action(pressed_action)
			self.backdrop5.run_action(pressed_action)
			self.commit()
			return
		elif touch.location in self.restart_button.bbox:
			self.restart_button.run_action(pressed_action)
			sound.play_effect(button_sound)
			self.new_game(self.win)
			return
		elif self.can_play:
			for square in self.squares:
				if touch.location in square.bbox and (square.state == 1 or square.state == 2):
					square.pressed()
					square.toggle_neighbours(self.squares)	
					self.move_counters()
					return

	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass


class Square (SpriteNode):
	def __init__(self, row, col, position, size, state, color):
		self.row = row
		self.col = col
		self.position = position
		self.size = size
		self.color = color
		self.z_position = 0.2
		self.state = state
		if self.state == 1:
			self.color = color1
		if self.state == 2:
			self.color = color2
	
	def white_neighbours(self, square_list):
		white_neighbours = []
		for s in square_list:
			if (((s.row == self.row - 1) and (s.col == self.col)) or ((s.row == self.row + 1) and (s.col == self.col)) or ((s.row == self.row) and (s.col == self.col - 1)) or ((s.row == self.row) and (s.col == self.col + 1))) and s.state == 2:
				white_neighbours.append(s)
		return white_neighbours
	
	def toggle_neighbours(self, squares):
		for square in squares:
			if square.row >= self.row - 1 and square.row <= self.row + 1 and square.col >= self.col - 1 and square.col <= self.col + 1 and not (square.row == self.row and square.col == self.col) and (square.state == 1 or square.state == 2):
				square.toggle()

	def pressed(self):
		if self.state == 0:
			return
		sound.play_effect(tap_sound)
		self.z_position = 0.3
		self.run_action(pressed_action)
		self.state = 0
		self.color = color3

	def toggle(self):
		if self.state == 0:
			return
		self.run_action(toggle_action)
		if self.state == 1:
			self.state = 2
			self.color = color2
		elif self.state == 2:
			self.state = 1
			self.color = color1
			

class StartFinish (SpriteNode):
	def __init__(self, row, type):
		if type == "start":
			self.anchor_point = (0.75, 0.5)
			self.position = (top_left[0] - square_size, top_left[1] - square_size * (row - 1))
		elif type == "finish":
			self.anchor_point = (0.25, 0.5)
			self.position = (top_left[0] + square_size * cols, top_left[1] - square_size * (row - 1))
		self.size = (2 * square_size, square_size)
		self.color = color4
		self.z_position = 0.2
		self.row = row


#---Run Game
if __name__ == '__main__':
	run(Game(), show_fps=False, orientation=PORTRAIT)