# coding: utf-8

# https://forum.omz-software.com/topic/3880/number-bonds-good-for-kids

from scene import *
import sound
import random
import math
import console
import speech
A = Action

happy_faces = (Texture('emj:Grinning'),Texture('emj:Kissing_2'),Texture('emj:Monkey_Face'),Texture('emj:Smiling_1'),Texture('emj:Smiling_2'),Texture('emj:Smiling_4'),Texture('emj:Smiling_6'),Texture('emj:Stuck-Out_Tongue_2'),Texture('emj:Winking'))

speech.say('welcome to number bonds... what is your name please?')
name = console.input_alert('WELCOME TO NUMBER BONDSðŸ¤”','Name',hide_cancel_button=True)
thank_you = 'thank you %s' % name
speech.say(thank_you)

class rand_color(object):
	def get(self):
		return float(random.randrange(0,10)) / 10
		
class MyScene (Scene):
	def setup(self):
	
								#setup background and number        key-pad#
		rect = ui.Path.rounded_rect(0,0,self.size.x-10,160,15)
		panel = ShapeNode(rect,parent=self)
		panel.position = (self.size.x/2,150)
		panel.color = '#ffffc9'
		panel.line_width = 10
		panel.stroke_color = '#ffff28'
		
		col = rand_color()
		self.background_color = '#86aeff'
		self.number_list = []
		self.total = 0
		x = 30
		y = 200
		num = 0
		while num < 11:
			a = col.get()
			b = col.get()
			c = col.get()
			number =    LabelNode(str(num),parent=self)
			number.position = (x,y)
			number.scale = 3
			number.color = (a,b,c)
			self.number_list.append(number)
			x += 50
			num += 1
			if x > 300:
				x = 30
				y -= 100
				
			#set up number bonds#
		x2, y2 = self.size / 2
		circ_shape = ui.Path.oval(0,0,80,80)
		
		circle1 = ShapeNode(circ_shape,parent=self)
		circle1.position = (x2,y2+230)
		circle1.line_width = 10
		circle1.stroke_color = '#ff6b6b'
		
		circle2 = ShapeNode(circ_shape,parent=self)
		circle2.position = (circle1.position.x/2,y2+160)
		circle2.line_width = 10
		circle2.stroke_color = '#6b6bff'
		
		circle3 = ShapeNode(circ_shape,parent=self)
		circle3.position = (circle1.position.x/2*3,y2+160)
		circle3.line_width = 10
		circle3.stroke_color = '#6b6bff'
		
		self.check = ShapeNode(rect,parent=self)
		self.check.position = (x2,y2+50)
		self.check.line_width = 10
		self.check.stroke_color = '#000000'
		self.check.scale = 0.5
		check_label = LabelNode('CHECK',parent=self)
		check_label.position = self.check.position
		check_label.color = 'black'
		check_label.scale = 2
		
		self.master = random.randrange(30,100)
		self.num1 = random.randrange(1,self.master-10)
		self.answer = self.master - self.num1
		self.guess = 0
		
		self.master_label = LabelNode(str(self.master),parent=self)
		self.master_label.position = circle1.position
		self.master_label.color = 'black'
		self.master_label.scale = 2
		
		self.num1_label = LabelNode(str(self.num1),parent=self)
		self.num1_label.position = circle2.position
		self.num1_label.color = 'black'
		self.num1_label.scale = 2
		
		self.guess_label = LabelNode(str(self.guess),parent=self)
		self.guess_label.position = circle3.position
		self.guess_label.color = 'black'
		self.guess_label.scale = 2
		
		self.tries = 0
		self.correct = 0
		
		self.correct_messages = ['well done','excellent','your the best','fandabidozee','boom ting','bang on','bet you do this in your sleep']
		
	def reset(self):
		self.master = random.randrange(30,100)
		self.num1 = random.randrange(1,self.master-10)
		self.answer = self.master - self.num1
		self.guess = 0
		
		self.master_label.text = str(self.master)
		self.num1_label.text = str(self.num1)
		self.guess_label.text = str(self.guess)
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		global name
		
		x, y = touch.location
		
		for number in self.number_list:
			x1, y1, x2, y2 = number.frame
			if x1 < x < (x1 + x2) and y1 < y < (y1 + y2):
				num = int(number.text)
				self.guess += num
				self.guess_label.text = str(self.guess)
				if num == 0:
					self.guess = 0
					self.guess_label.text = str(self.guess)
					
		x1, y1, x2, y2 = self.check.frame
		if x1 < x < x1+x2 and y1 < y < y1+y2:
			if self.answer == self.guess:
				# IF ANSWER'S CORRECT
				speech.say(name)
				speech.say(self.correct_messages[random.randrange(0,len(self.correct_messages))])
				self.tries += 1
				self.correct += 1
				sound.play_effect('game:Ding_3')
				animation = A.group(A.move_by(self.size.x+30,0,3),A.rotate_by(-5,3))
				happy = SpriteNode(happy_faces[random.randrange(0,len(happy_faces))],parent=self)
				happy.position = (0,260)
				happy.run_action(animation)
				
			else:
				#IF ANSWER'S WRONG
				self.tries += 1
				sound.play_effect('game:Error')
			self.reset()
		appraisal = self.tries % 5
		if appraisal == 0 and self.tries > 0:
			message = '%d out of %d' % (self.correct, self.tries)
			console.hud_alert(message)
			
if __name__ == '__main__':
	run(MyScene(),PORTRAIT, show_fps=False)

