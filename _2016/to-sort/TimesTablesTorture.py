from scene import *
from random import randint
import sound

BUTTONS = [['', '0', 'Delete'],
           ['7', '8', '9'],
           ['4', '5', '6'],
           ['1', '2', '3']]

BLOCKS = ['PC_Brown_Block', 'PC_Dirt_Block', 'PC_Grass_Block', 'PC_Plain_Block', 'PC_Stone_Block', 'PC_Wood_Block']

IMAGE_HEIGHT = 171.0
IMAGE_WIDTH = 101.0
BLOCK_WIDTH = IMAGE_WIDTH
BLOCK_HEIGHT = 40.0
BLOCK_DEPTH =  80.0
BLOCK_SELECTOR_OFFSET = BLOCK_HEIGHT + BLOCK_DEPTH
BLOCK_TEXT_X = BLOCK_WIDTH / 2
BLOCK_TEXT_Y_1 = BLOCK_HEIGHT + (BLOCK_DEPTH / 2)
BLOCK_TEXT_Y_2 = BLOCK_HEIGHT * 0.4

BLOCK_MATRIX_WIDTH = 10
BLOCK_MATRIX_HEIGHT = 10

VISIBLE_BLOCK_COLUMNS = 10
VISIBLE_BLOCK_ROWS = 3

GRAVITY = 1000
BLOCK_DROP = -2 * IMAGE_HEIGHT

BUTTON_WIDTH = 85
BUTTON_HEIGHT = 85
BUTTON_PAD = 15

MULT_TABLE_MAX = 11
MULT_TABLE_MIN = 1

GAME_WAITING = 0
GAME_PLAYING = 1
GAME_FINISHED = 2

GAME_TIME = 120

def shadow_text(s, font, font_size, x, y, col):
	tint(0.00, 0.00, 0.00)
	text(s, font, font_size, x + 2, y - 2)
	tint(*col)
	text(s, font, font_size, x, y)

class ProblemSquare(object):
	def __init__(self):
		self.a = randint(MULT_TABLE_MIN, MULT_TABLE_MAX)
		self.b = randint(MULT_TABLE_MIN, MULT_TABLE_MAX)
		self.answer_text = ""
		self.bounds = Rect(0, 0, 0, 0)
		self.selected = False
		self.answer = str(self.a * self.b)
		self.velocity = 0
		self.img = 0
		self.falling = False
		self.final_y = 0
		
	def draw(self):
		tint(1,1,1)
		image(BLOCKS[self.img], self.bounds.x, self.bounds.y)
		if self.selected:
			image('PC_Selector', self.bounds.x, self.bounds.y + BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_DEPTH, 0, 0, 0, BLOCK_SELECTOR_OFFSET)
			tint(0,0,0)
			text(str(self.a) + ' x ' + str(self.b), 'AppleSDGothicNeo-Bold', 28, self.bounds.x + BLOCK_TEXT_X, self.bounds.y + BLOCK_TEXT_Y_1)
		else:
			shadow_text(str(self.a) + ' x ' + str(self.b), 'AppleSDGothicNeo-Bold', 28, self.bounds.x + BLOCK_TEXT_X, self.bounds.y + BLOCK_TEXT_Y_1, (1.00, 1.00, 1.00))
		shadow_text(self.answer_text, 'AppleSDGothicNeo-Bold', 28, self.bounds.x + BLOCK_TEXT_X, self.bounds.y + BLOCK_TEXT_Y_2, (1.00, 1.00, 1.00))

class TTTButton(object):
	def __init__(self):
		self.bounds = Rect()
		self.is_selected = False
		self.is_enabled = True
		self.draw_border = True
		self.border_colour = (0.00, 0.50, 1.00)
		self.background_colour = (0.00, 0.25, 0.50)
		self.text_colour = (1.00, 1.00, 1.00)
		self.text = ""
	
	def draw(self):
		if self.is_enabled:
			if self.draw_border:
				stroke_weight(1)
				stroke(*self.border_colour)
			else:
				no_stroke()
			fill_colour = self.border_colour if self.is_selected else self.background_colour
			fill(*fill_colour)
			ellipse(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h)
			tint(*self.text_colour)
			if not self.is_selected:
				font_size = (self.bounds.h / 2) - (4 * len(self.text))
				text(self.text, 'AppleSDGothicNeo-Light', font_size, self.bounds.x + self.bounds.w/2, self.bounds.y + self.bounds.h/2)
			
class MyScene (Scene):
	
	def create_problem_matrix(self):
		self.problems = []
		starting_x = self.block_area_x
		starting_y = self.block_area_y
		for y in range(BLOCK_MATRIX_HEIGHT):
			row = []
			img = y % len(BLOCKS)
			for x in range(BLOCK_MATRIX_WIDTH):
				problem = ProblemSquare()
				problem.bounds = Rect(starting_x + (x * BLOCK_WIDTH), starting_y + (y * BLOCK_DEPTH),  IMAGE_WIDTH, IMAGE_HEIGHT)
				problem.img = img
				row.append(problem)
			self.problems.append(row)
			
	def create_button_keypad(self):
		self.buttons = []
		starting_x = (self.bounds.w - (3 * BUTTON_WIDTH) - (2 * BUTTON_PAD)) / 2
		starting_y = (self.block_area_y - (4 * BUTTON_HEIGHT) - (3 * BUTTON_PAD)) / 2
		for y in range(len(BUTTONS)):
			for x in range(len(BUTTONS[y])):				
				button = TTTButton()
				button.text = BUTTONS[y][x]
				button.bounds = Rect(starting_x + (x * (BUTTON_WIDTH + BUTTON_PAD)), starting_y + (y * (BUTTON_HEIGHT + BUTTON_PAD)), BUTTON_WIDTH, BUTTON_HEIGHT)
				if button.text == 'Delete':
					button.draw_border = False
				elif button.text == '':
					button.is_enabled = False
				self.buttons.append(button)
		
	def setup_graphics(self):
		self.block_area_x = (self.bounds.w - (VISIBLE_BLOCK_COLUMNS * BLOCK_WIDTH)) / 2
		self.block_area_y = self.bounds.top() - (VISIBLE_BLOCK_ROWS * BLOCK_DEPTH) - BLOCK_HEIGHT
		self.button_area_x = (self.bounds.w - ((BUTTON_WIDTH * 3) + (BUTTON_PAD * 2)) / 2)
		self.button_area_y = (self.block_area_y - ((BUTTON_HEIGHT * 4) + (BUTTON_PAD * 3))) / 2
		
	def setup_game(self):
		self.create_problem_matrix()
		self.demo_block = 0
		self.demo_drop_time = self.t
		self.problems[0][0].selected = True
		self.game_state = GAME_WAITING
	
	def draw_problems(self):
		for row in reversed(self.problems):
			for problem in row:
				if problem.bounds.y < self.bounds.h and problem.bounds.top() > 0:
					problem.draw()
		
	def draw_buttons(self):
		for button in self.buttons:
			button.draw()
		
	def run_gravity(self):
		for row in self.problems:
			for problem in row:
				if problem.falling:
					problem.velocity += GRAVITY * self.dt
					problem.bounds.y -= problem.velocity * self.dt
					if problem.bounds.y < problem.final_y:
						problem.bounds.y = problem.final_y
						problem.falling = False
						problem.velocity = 0
						
	def drop_block(self, x, y):
		problem = self.problems[y][x]
		problem.falling = True
		problem.final_y = BLOCK_DROP
		for y2 in range(y + 1, BLOCK_MATRIX_HEIGHT):
			problem = self.problems[y2][x]
			problem.falling = True
			problem.final_y = problem.bounds.y - BLOCK_DEPTH
			
	def correct_answer(self, x, y):
		index = (y * BLOCK_MATRIX_WIDTH + x)
		problem = self.problems[y][x]
		self.drop_block(x, y)
		sound.play_effect('Coin_2')
		self.score += 1
		finished = self.select_next_block(x, y)
		if finished:
			self.game_finished()
			
	def draw_score(self):
			shadow_text('Score : ' + str(self.score), 'AvenirNext-Heavy', 72, self.bounds.w / 2, self.bounds.h * 0.65, (0.80, 0.40, 1.00))
			shadow_text('Time : ' + str(int(self.play_time)), 'AvenirNext-Heavy', 72, self.bounds.w / 2, self.bounds.h * 0.5, (0.80, 0.40, 1.00))
			shadow_text('{:.2f}s / Answer'.format(self.avg_prob_time), 'AvenirNext-Heavy', 72, self.bounds.w / 2, self.bounds.h * 0.35, (0.80, 0.40, 1.00))
		
	def draw_text(self):
		if self.game_state == GAME_WAITING:
			if(int(self.t) % 2):
				shadow_text('Touch to Start!', 'AvenirNext-Heavy', 72, self.bounds.w / 2, self.bounds.h / 2, (0.80, 0.40, 1.00))
		if self.game_state == GAME_FINISHED:
			self.draw_score()
			
	def check_time(self):
		if self.game_state == GAME_PLAYING:
			if self.t - self.start_time > GAME_TIME:
				self.game_finished()
				
	def get_selected_block(self):
		for y in range(len(self.problems)):
			for x in range(len(self.problems[y])):
				p = self.problems[y][x]
				if p.selected:
					return (x, y)
		return (-1, -1)
		
	def select_next_block(self, x, y):
		problem = self.problems[y][x]
		problem.selected = False
		index = (y * BLOCK_MATRIX_WIDTH) + x + 1
		if index == BLOCK_MATRIX_WIDTH * BLOCK_MATRIX_HEIGHT:
			return True
		else:
			self.problems[index / BLOCK_MATRIX_WIDTH][index % BLOCK_MATRIX_WIDTH].selected = True
		return False
					
	def run_demo(self):
		if(self.t > (self.demo_drop_time + 0.1)):
			x, y = self.get_selected_block()
			problem = self.problems[y][x]
			problem.answer_text = problem.answer
			self.drop_block(x, y)
			self.demo_drop_time = self.t
			finished = self.select_next_block(x, y)
			if finished:
				self.setup_game()

	def game_loop(self):
		self.run_gravity()
		if self.game_state == GAME_WAITING:
			self.run_demo()
		elif self.game_state == GAME_PLAYING:
			self.check_time()
			
	def draw_game(self):
		background(0.00, 0.25, 0.50)
		self.draw_problems()
		self.draw_buttons()
		self.draw_text()

	def start_game(self):
		self.setup_game()
		self.game_state = GAME_PLAYING
		self.start_time = self.t
		self.problems[0][0].selected = True
		self.clock_index = 0
		self.score = 0
		self.best = 0
	
	def game_finished(self):
		self.game_state = GAME_FINISHED
		sound.play_effect('Powerup_2')
		self.finish_time = self.t
		self.play_time = self.finish_time - self.start_time
		self.avg_prob_time = self.play_time / self.score

	def button_pushed(self, button):
		if self.game_state == GAME_PLAYING:
			x, y = self.get_selected_block()
			problem = self.problems[y][x]
			sound.play_effect('Click_1')
			if button.text == 'Delete':
				l = len(problem.answer_text)
				if l > 0:
					problem.answer_text = problem.answer_text[0:l-1]
			else:
				problem.answer_text += button.text
				if len(problem.answer_text) >= len(problem.answer):
					if(problem.answer_text == problem.answer):
						self.correct_answer(x, y)
					else:
						sound.play_effect('Error')
						problem.answer_text = ''
	
	def setup(self):
		self.setup_graphics()
		self.create_button_keypad()
		self.setup_game()
		
	def draw(self):
		self.game_loop()
		self.draw_game()
		
	def touch_began(self, touch):
		if self.game_state == GAME_PLAYING:
			for button in self.buttons:
				if touch.location in button.bounds:
					button.is_selected = True
				else:
					button.is_selected = False
	
	def touch_ended(self, touch):
		if self.game_state == GAME_WAITING:
			self.start_game()
		elif self.game_state == GAME_PLAYING:
			for button in self.buttons:
				if button.is_selected and (touch.location in button.bounds):
					self.button_pushed(button)
				button.is_selected = False
		elif self.game_state == GAME_FINISHED:
			if (self.t - self.finish_time > 2):
				self.setup_game()

run(MyScene(), LANDSCAPE)
