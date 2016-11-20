# -*- coding: utf-8 -*-

# my first dev with pythonista. A short game for my children

from scene import *
import time
import random
import sound

# force cpu to play the right move whith 12 pawn left
takeaction = {
    12:3,
    11:2,
    10:1,
    8: 3,
    7: 2,
    6: 1,
    4: 3,
    3:2,
    2:1}

sText =''
img_size = 60
btnImg_size = 90
cols = 8
rows = 10

class MyRectangle(object):
	def __init__(self,x,y,w,h,touched=False):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.touched = touched
		
class Pawn(object):
	def __init__(self, image, x, y):
		self.offset = Point()
		self.selected = False
		self.image = image
		self.touched = False
		self.x, self.y = x, y
		
	def hit_test(self, touch):
		frame = Rect(self.x * img_size + self.offset.x,
		self.y * img_size + self.offset.y,
		img_size, img_size)
		return touch.location in frame
		
		
class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		self.nbpawn= random.randrange(15,41)
		self.LstImg = self.getImage(self.nbpawn)
		self.show_instructions = True
		self.game_running = False
		self.btnOk = MyRectangle(730,630,100,100)
		self.btnImg = Pawn('White_Square',8,7)
		self.textbtn = 'Suivant'
		self.nbpawnInGame=0
		self.bCpuIsPlaying = False
		self.nbPawnSelected = 0
		self.nbPawnSelectedByCpu = 0
		self.bPlayerTurn = True
		self.selectedP_cpu = 0
		self.bNext = False
		self.bPlayerok = False
		self.effects = Layer(self.bounds)
		
	#list of rectangle,
	#set number of image to show in parameter
	def getImage(self,nbImg):
		listImg = []
		iCount = 0
		x = 1
		y = 1
		for i in range(0,nbImg):
			if iCount == 8:
				iCount = 0
				y = y + 2
				x = 1
				
			listImg.append(Pawn('Baby_Chick_2',x,y))
			x = x + 2
			iCount = iCount+1
		return listImg
		
	# This will be called for every frame (typically 60 times per second).
	def draw(self):
		background(0, 0, 0)
		fill(1,0,1)
		image(self.btnImg.image,
		self.btnImg.x * btnImg_size + self.btnImg.offset.x,
		self.btnImg.y * btnImg_size + self.btnImg.offset.y,
		btnImg_size, btnImg_size)
		text(self.textbtn,'Futura', 19,self.btnOk.x+36,self.btnOk.y+50)#text for OK button
		if self.show_instructions:
			self.textIntro()
		else:
			if self.nbpawn>1:
				if self.bPlayerTurn:
					self.PlayerTurn()
				else:
					self.nbPawnSelectedByCpu= self.choosePawn(self.nbpawn)
					self.CpuTurn()
					tint(1,0,0)
				self.myText(str(self.nbPawnSelectedByCpu) + ' pions pris par le cpu',700)
				self.myText('il reste ' + str(self.nbpawn) + ' pions',680)
				tint(1,1,1)
			else:
				self.finPartie()
			for img in self.LstImg:
				image(img.image,
				img.x * img_size + img.offset.x,
				img.y * img_size + img.offset.y,
				img_size,img_size)
			tint(1,1,1)
			
	#when you touch the screen
	def touch_began(self, touch):
		myBtn = Rect(self.btnOk.x,self.btnOk.y,self.btnOk.w,self.btnOk.h)
		bselectedBeforeTouched = False
		self.bNext = False
		
		if touch.location in myBtn:
			self.btnImg.image = 'Black_Square'
			if self.show_instructions:
				self.show_instructions = False
			else:
				if self.bPlayerok:
					self.game_running = True
					self.bNext = True
					self.bPlayerTurn = True
			#self.play()
		else:
			for img in self.LstImg:
				if img.hit_test(touch):
					self.bPlayerok = True
					bselectedBeforeTouched = img.touched #etat avant toute modif
					img.touched = not(img.touched)
					if img.touched and self.nbPawnSelected >= 3:
						img.touched = False
					if img.touched:
						img.image = 'Baby_Chick_3'
					else: img.image = 'Baby_Chick_2'
					if self.nbPawnSelected < 3 and img.touched:
						self.nbPawnSelected = self.nbPawnSelected + 1
					else:
						img.touched = False
						if bselectedBeforeTouched:
							self.nbPawnSelected = self.nbPawnSelected -1
					break
					
	def touch_moved(self, touch):
		pass
		
	#when you stop touching the screen
	def touch_ended(self, touch):
		myBtn = Rect(self.btnOk.x,self.btnOk.y,self.btnOk.w,self.btnOk.h)
		if touch.location in myBtn:
			self.btnImg.image = 'White_Square'
			
	def myText(self,stext,pos):
		text(stext, 'Futura', 20,400, pos,5)
		
	def textIntro(self):
		tint(1,1,1)
		self.myText('Nous allons jouer à  un jeu amusant !!!',730)
		self.myText('Le jeu de NIM',710)
		self.myText('le principe est simple',690)
		self.myText('chacun notre tour nous allons prendre des poussins ^_^',670)
		self.myText('Tu peux prendre jusqu à 3 poussins d un coup.',650)
		self.myText('mais tu ne dois jamais prendre le dernier sinon c est toi le perdant',630)
		tint(1,0,0)
		self.myText('touche le bouton suivant pour jouer.',590)
		self.animatedText('test anime')
		tint(1,1,1)
		
	def CpuTurn(self):
		self.nbpawn = self.nbpawn - self.nbPawnSelectedByCpu
		self.LstImg = self.getImage(self.nbpawn)
		self.bNext = False
		self.bPlayerTurn = True
		
	def PlayerTurn(self):
		if self.bNext:
			self.nbpawn = self.nbpawn - self.nbPawnSelected
			self.LstImg = self.getImage(self.nbpawn)
			self.bNext = False
			self.nbPawnSelected = 0
			self.bPlayerTurn = False
			self.bPlayerok = False
			
	def choosePawn(self,nbP):
		resultAction = takeaction.get(nbP)
		if resultAction != None:
			return resultAction
		bimPair = False
		if bimPair :
			return 2
		elif nbP > 3:
			return random.randrange(1,4,2)
		else:
			return 1
			
	def isItImpair(self,nbP):
		if nbP > 12 :
			return (nbP % 2 != 0)
		elif nbP == 5:
			return True
		else:
			return False
			
	def play(self):
		tint(1,1,1)
		if self.game_running == False:
			if self.isItImpair(self.nbpawn):
				self.PlayerTurn()
			else:
				self.nbpawn = self.StartByCPU(self.nbpawn)
				self.bPlayerTurn = True
		else:
			if self.nbpawn > 1:
				if self.bPlayerTurn:
					self.PlayerTurn()
				if self.bCpuIsPlaying:
					self.nbpawn = self.StartByCPU(self.nbpawn)
					self.bPlayerTurn = True
					
					
	def finPartie(self):
		if self.bPlayerTurn:
			self.myText('Dommage tu as perdu !!! ',730)
		else:
			self.myText('Bravo, tu es le vainqueur !!! ',730)
			
	def StartByCPU(self,nb):
		self.bNext = False
		nbpawnInGame = nb
		self.nbPawnSelectedByCpu = self.choosePawn(nbpawnInGame)
		nbpawnInGame = nb - self.nbPawnSelectedByCpu
		self.CpuTurn()
		return nbpawnInGame
		
	def animatedText(self,text):
		#Show the added score as an animated text layer:
		score_layer = TextLayer(text,
		'GillSans-Bold', 20)
		score_layer.frame.center(self.bounds.center())
		#self.effects.add_layer(score_layer)
		overlay = Layer(self.bounds)
		overlay.background = Color(0, 0, 0, 0)
		overlay.add_layer(score_layer)
		self.add_layer(overlay)
		overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
		score_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
		score_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
		from_frame = MyRectangle(730,630,100,100)
		to_frame = Rect(from_frame.x, from_frame.y,
		from_frame.w, from_frame.h)
		score_layer.animate('frame', to_frame, duration=0.5)
		#score_layer.draw()
		score_layer.animate('alpha', 0.0, delay=0.3,
		completion=score_layer.remove_layer)
		
		
run(MyScene())

