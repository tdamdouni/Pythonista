from __future__ import print_function
from scene import *

# Wraps input text to a width size	
def textWrap(text, width):
	words = text.split()
	lines = ""
	length = 0
	wordNum = 0
	for i in words:
		if len(i) > width:
			if wordNum > 0:
				lines += "\n"
			length = 0
			num = int(len(i)/width) + 1
			for j in range(num-1):
				lines += i[j*width-(j):j*width+(width-1)] + "-\n"
			left = i[(num-1)*width-1:len(i)]
			if length + len(left) < width and wordNum < len(words)-1:
					left += " "
			lines += left
			length += len(left)
		else: 
			if length + len(i) <= width:
				if length + len(i) < width and wordNum < len(words)-1:
					i += " "
				lines += i
				length += len(i)
			else: 
				lines += "\n"
				length = 0
				if length + len(i) < width and wordNum < len(words)-1:
					i += " "
				lines += i
				length += len(i)
			wordNum += 1
	return lines


class Actor (object):
	def __init__(self, name, color):
		self.name = name
		
		# Set the Actor's graphics variables
		rbg = color.split(",")
		self.color = [float(rbg[0]), float(rbg[1]), float(rbg[2])]
		self.visible = True
		self.costume = ""
		
		self.x = 160
		self.y = 300


class Scene (Scene):
	def setup(self):
		# Read actor file and get actors
		actorFile = open("Oppy_Actors.txt", "r")
		actorScript = actorFile.read()
		actorFile.close()

		self.actors = []
		actorStarters = actorScript.split(";")

		for actor in actorStarters:
			state = 0
			tok = ""
			isActor = False
			characters = list(actor)
	
			for char in characters:
				tok += char
		
				if tok == "\n":
					tok = ""
				if tok == "_":
					tok = ""
				if char == ":":
					isActor = True
					name = tok[0:len(tok)-1]
					tok = ""
				if tok == "(":
					tok = ""
				if char == ")":
					color = tok[0:len(tok)-1]
					tok = ""
			if isActor == True:
				newActor = Actor(name, color)
				self.actors.append(newActor)
			

		# Read the event file and get script
		eventFile = open("Ideal_Script.txt", "r")
		eventScript = eventFile.read()
		eventFile.close()

		self.events = eventScript.split(";")
		self.currentEvent = 0
		
		self.background = ""
		
		self.actor = ""
		self.action = ""
		self.details = ""
		
		self.speech = ""
		self.finalSpeech = ""
		self.char = 0
		self.textSpeed = 0.9
		
		self.lex(self.events[0])
		
	def nextEvent(self):
		self.currentEvent += 1
		self.char = 0
		
		print(self.currentEvent)
		print(len(self.events))
		self.lex(self.events[self.currentEvent])
	
	def lex(self, line):
		state = 0
		tok = ""
		characters = list(line)
	
		for char in characters:
			tok += char
		
			if state == 1 and char == '"':
				self.details = tok[0:len(tok)-1]
				state = 0
				tok = ""
			if state == 1 and char == ")":
				self.details = tok[0:len(tok)-1]
				state = 0
				tok = ""
				
			if state == 0:
				if tok == "\n":
					tok = ""
				if tok == " ":
					tok = ""
				if char == ".":
					for actor in self.actors:
						if tok[0:len(tok)-1] == actor.name:
							self.actor = actor
					tok = ""
				if char == ":":
					self.action = tok[0:len(tok)-1]
					tok = ""
				if tok == '"':
					state = 1
					tok = ""	
				if tok == "(":
					state = 1
					tok = ""
					
		print(self.actor.name + " will " + self.action + ": (" + self.details + ")")
		
		self.parse()
		
	def parse(self):
		if self.action == "say":
			self.speech = textWrap(self.details, 37)
		if self.action == "change":
			if self.actor.name == "[BG]":
				self.background = self.details
			else: 
				self.actor.costume = self.details
			self.nextEvent()
			
		self.draw()
			
	def render(self):
		tint(1, 1, 1)
		image(self.background, 0, 308, 320, 240)
		
		for actor in self.actors:
			if actor.visible == True:
				tint(1, 1, 1)
				#image(actor.costume, actor.x, actor.y, 150, 200)
	
		# Render a white cutoff box
		fill(1.00, 1.00, 1.00)
		rect(0, 0, 320, 308)
		
		if self.action == "say":
			tint(self.actor.color[0], self.actor.color[1], self.actor.color[2])
			text(self.actor.name + ":\n" + self.finalSpeech, "Avenir-Book", 18, 160, 160)
		
	def draw(self):
		background(1, 1, 1)
		
		self.t += 1.00
			
		if self.t >= 100.00:
			self.t = 0.00
			if self.currentEvent < len(self.events)-2:
				self.nextEvent()
			
		# Add a character at a time to the final text
		self.finalSpeech = self.speech[0:int(self.char)]
			
		if self.char < len(self.speech):
			self.char += self.textSpeed
			
		self.render()
			
			
run(Scene())
		
		
