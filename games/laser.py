# coding: utf-8

# https://gist.github.com/J-Behemoth/44834f5f6109d5fe4f19

# https://forum.omz-software.com/topic/2972/getting-a-game-to-scale-on-all-devices

# ALIEN LASERS
# By: Jackson Laumann

# WHAT MORE CAN YOU ASK FOR
from scene import *
from random import *
from sound import *
import pickle
class MyScene (Scene):
	def setup(self):
		global mobx, moby, speed, ded, score, highscore, star1, star2, star3, star4, star5, star6, star7, star8, star9, star10, gold, golden, menu, lazor, lazorx, lazory, boss, sheild, ship, ships
		self.x = self.size.w * 0.5
		self.y = self.size.h * 0.5
		moby = 1500
		mobx = randint(1,290)
		speed = 19
		ded = 0
		score = 0
		lazor = 0
		lazorx = -100
		lazory = 900
		try:
			with open('laserShips', 'r') as f:
					ships = pickle.load(f)
		except IOError:
					ships = 0
		try:
			with open('laserSheild', 'r') as f:
					sheild = pickle.load(f)
		except IOError:
					sheild = 0
		try:
			with open('laserShip', 'r') as f:
					ship = pickle.load(f)
		except IOError:
					ship = 0
		try:
			with open('laserHigh', 'r') as f:
					highscore = pickle.load(f)
		except IOError:
					highscore = 0
		try:
			with open('laserGold', 'r') as f:
					gold = pickle.load(f)
		except IOError:
					gold = 0
		if sheild == 1:
			ded = -1
		golden = randint(1,100)
		star1 = randint(1,290)
		star3 = randint(1,290)
		star5 = randint(1,290)
		star7 = randint(1,290)
		star9 = randint(1,290)
		star2 = randint(1,550)
		star4 = randint(1,550)
		star6 = randint(1,550)
		star8 = randint(1,550)
		star10 = randint(1,550)
		menu = 0
		boss = 0
	def draw(self):
		global mobx, moby, score, highscore, ded, star1, star2, star3, star4, star5, star6, star7, star8, star9, star10, gold, golden, menu, lazor, lazorx, lazory, boss, sheild, ship, ships
		try:
			with open('laserSheild', 'r') as f:
					sheild = pickle.load(f)
		except IOError:
					sheild = 0
		set_volume(0.5)
		background(.0, .0, .12)
		fill(1,1,1)
		tint(1,1,1)
		if menu == 1:
			g = gravity()
			self.x += g.x * 24
			self.y += g.y * 24
			self.x = min(self.size.w - 100, 	max(0, self.x))
			self.y = min(self.size.h - 90, 	max(0, self.y))
		def star():
			image('emj:Star_1', star1, star2, 20, 20)
			image('emj:Star_1', star3, star4, 20, 20)
			image('emj:Star_1', star5, star6, 20, 20)
			image('emj:Star_1', star7, star8, 20, 20)
			image('emj:Star_1', star9, star10, 20, 20)
		star()
		if menu == 0:
			global alienRect
			alienRect = Rect(self.x, self.y, 100, 100)
			image('iow:ios7_cart_outline_256',0, 0, 50, 50)
			image('spc:PlayerLife2Green',260, 10, 50, 50)
			if ship == 0:
				image('spc:PlayerShip2Green', 150, 250, 100, 100)
			if ship == 1:
				image('spc:PlayerShip2Orange', 150, 250, 100, 100)
				tint(1,1,1)
			if ship == 2:
				tint(random(),random(),random())
				image('spc:PlayerShip2Blue', 150, 250, 100, 100)
				tint(1,1,1)
			image('spc:Fire9',190, 210, 20,50)
			tint(1.0, 1.0, .47)
			text('Space','Papyrus',70,100,500,5)
			text('Lazors','Papyrus',70,150,400,5)
		elif menu == 1:
			if not ded > 270:
				if ship == 0:
					image('spc:PlayerShip2Green', self.x, self.y, 100, 100)
				if ship == 1:
					image('spc:PlayerShip2Orange', self.x, self.y, 100, 100)
				if ship == 2:
					tint(random(),random(),random())
					image('spc:PlayerShip2Blue', self.x, self.y, 100, 100)
					tint(1,1,1)
				image('spc:Fire9',self.x+40, self.y-40, 20,50)
				tint(1,1,1)
			stroke(0.00, 1.00, 0.00)
			stroke_weight(3)
			if golden > 3 or ded >= 3:
				image('spc:LaserRed6', mobx, moby, 30, 50)
			else:
				image('plf:Item_CoinGold', mobx, moby, 50, 50)
			alienRect = Rect(self.x, self.y, 100, 100)
			lazorRect = Rect(lazorx + 29, lazory + 60, 40, 70)
			mobRect = Rect(mobx-10, moby, 30, 30)
			global speed
			lazorRect
			moby = moby - speed
			if ded >= 3:
				lazory = 900
				self.x = 100
				self.y = 250
				tint(1,1,1)
				text('Your time has come.','Avenir-HeavyOblique', 30, 150, 400, 5)
				fill(.83, .3, .3)
				stroke(.65, .65, .65)
				rect(35,100,230,50)
				tint(0.70, 0.00, 0.00)
				text('tap to try again','Avenir-Roman',30, 150,125,5)
				tint(1,1,1)
				tint(.93, .93, .1)
				text('%s' %gold,'Papyrus',30, 170,60,5)
				tint(1,1,1)
				image('plf:Item_CoinGold', 110, 37,50,50)
				if score >= highscore:
					tint('#20ce20')
					highscore = score
					text('HIGHSCORE!', 'Papyrus', 30,150,500,5)
					with open('laserHigh', 'w+') as f:
						pickle.dump(highscore, f)
				text('%s' %score,'Avenir-Roman',70, 150, 460,5)
				tint(1,1,1)
				mobx = 150
				moby = moby - 2
				ded = ded + 1
				alienRect = Rect(self.x, self.y, 100, 100)
			if moby < -200:
				if ded < 3:
					if golden > 3:
						score = score + 1
					moby = 800
					mobx = randint(1,290)
					golden = randint(1,100)
					fill(1,1,1)
					mobRect
			if ded > 300:
				self.x += g.x * 24
				self.y += g.y * 24
				self.x = min(self.size.w - 5000, 	max(0, self.x))
				self.y = min(self.size.h - 5000, max(0, self.y))
				alienRect = Rect(self.x, 900, 100, 100)
			if mobRect.intersects(lazorRect):
				moby = 800
				mobx = randint(1,290)
				golden = randint(1,100)
				score = score + 1
			if alienRect.intersects(mobRect):
				if ded >= 3:
					ded = ded + 1
				elif golden > 3:
					play_effect('Hit_2')
					ded = ded + 1
				else:
					play_effect('arcade:Coin_2')
					gold = gold + 1
					with open('laserGold', 'w+') as f:
						pickle.dump(gold, f)
				moby = 800
				mobx = randint(1,290)
				golden = randint(1,100)
				if golden > 3 or ded >= 3:
					self.y = self.y - 10
			if ded > 270 and ded < 320:
				image('Explosion',0, 150, 300,300)
				moby = 900
				mobx = -100
			if ded == 271:
				play_effect('Explosion_4')
			if ded < 3:
				text('%s' %score,'Avenir-Roman',30, 20, 540,5)
				tint(.93, .93, .1)
				text('%s' %gold,'Papyrus',30, 130, 540,5)
				image('plf:Item_CoinGold', 60, 517, 50, 50)
				tint(1,1,1)
			if moby < 690 and moby > 670 and ded >= 3:
				ded = ded
			elif moby < 690 and moby > 670 and golden > 3:
				play_effect('arcade:Laser_1')
			elif moby < 690 and moby> 670 and ded < 3:
				play_effect('arcade:Coin_3')
			star2 = star2 - 10
			star4 = star4 - 10
			star6 = star6 - 10
			star8 = star8 - 10
			star10 = star10 - 10
			if star2 < -20:
				star1 = randint(1,290)
				star2 = randint(700,900)
			if star4 < -20:
				star3 = randint(1,290)
				star4 = randint(700,900)
			if star6 < -20:
				star5 = randint(1,290)
				star6 = randint(700,900)
			if star8 < -20:
				star7 = randint(1,290)
				star8 = randint(700,900)
			if star10 < -20:
				star9 = randint(1,290)
				star10 = randint(700,900)
			if ded <= -1:
				image('spc:ShieldBronze', 170,527,30,30)
			else:
				tint(.4,.4,.4)
				image('spc:ShieldBronze',170,527,30,30)
				tint(1,1,1)
			if ded <= 0:
				image('emj:Heart', 200,527,30,30)
			else:
				tint(.4,.4,.4)
				image('emj:Heart_Broken',	200,527,30,30)
				tint(1,1,1)
				if ded < 3:
					image('spc:PlayerShip2Damage1', self.x, self.y, 100, 100)
			if ded <= 1:
				image('emj:Heart', 230,527,30,30)
			else:
				tint(.4,.4,.4)
				image('emj:Heart_Broken', 230,527,30,30)
				tint(1,1,1)
				if ded < 3:
					image('spc:PlayerShip2Damage2', self.x, self.y, 100, 100)
			if ded <= 2:
				image('emj:Heart', 260,527,30,30)
			else:
				tint(.4,.4,.4)
				image('emj:Heart_Broken',260,527,30,30)
				tint(1,1,1)
			if ded <= 2:
				image('emj:Heart', 260,527,30,30)
			else:
				tint(.4,.4,.4)
				image('emj:Heart_Broken',260,527,30,30)
				tint(1,1,1)
			if ded <= 2:
					if lazor == 0:
						stroke_weight(3)
						stroke(.41, .41, .41)
						fill(.63,.63,.63)
						rect(260,0,60,40)
						stroke_weight(0)
						fill(.16, 1.0, .16)
						rect(263,3,54,34)
						fill(1,1,1)
					else:
						stroke_weight(3)
						stroke(.41, .41, .41)
						fill(.63,.63,.63)
						rect(260,0,60,40)
						stroke_weight(0)
						fill(.81, .0, .0)
						rect(263,3,lazory/17,34)
						fill(1,1,1)
			if ded >= 3:
				image('iow:ios7_cart_outline_256',0, 0, 50, 50)
				image('spc:PlayerLife2Green',260,10,50,50)
			if lazor >= 1 and lazory <= 1000:
				lazory = lazory + 12
				lazorRect
				image('spc:LaserGreen10', lazorx + 39, lazory + 70, 20, 50)
			if lazory >= 1000:
				lazor = 0
			if score == 10:
				boss = 1
		if menu == 3:
			tint(.93, .93, .1)
			text('%s' %gold,'Papyrus',30, 130, 540,5)
			image('plf:Item_CoinGold', 60, 517, 50, 50)
			tint(1,1,1)
			fill(.68, .68, .68)
			rect(0,0,600,50)
			fill(.33, .33, .33)
			ellipse(200,-170,200,200)
			image('iow:arrow_left_c_256',0,0,50,50)
			if ships == 2:
				tint(.28, .28, .28)
			tint (random(),random(),random())
			image('spc:PlayerShip2Blue',220,220,60,60)
			tint(1,1,1)
			if ships == 2:
				tint(.28, .28, .28)
			image('plf:Item_CoinGold',200,180,40,40)
			text('250','Papyrus',35,260,190,5)
			tint(1,1,1)
			if ships == 1:
				tint(.28, .28, .28)
			image('spc:PlayerShip2Orange',220,100,60,60)
			image('plf:Item_CoinGold',200,60,40,40)
			text('100','Papyrus',35,260,70,5)
			tint(1,1,1)
			if sheild == 1:
				tint(.28, .28, .28)
			image('spc:ShieldGold',120,100,60,60)
			image('plf:Item_CoinGold',110,60,40,40)
			text('60','Papyrus',35,160,70,5)
			tint(1,1,1)
		if menu == 4:
			image('iow:ios7_cart_outline_256',0, 0, 50, 50)
			if ship == 1:
				tint(.7, .7, .7)
			image('spc:PlayerShip2Green',50,400,100,100)
			tint(1,1,1)
			if ships == 1:
				if ship == 0:
					tint(.7, .7, .7)
				image('spc:PlayerShip2Orange',200,400,100,100)
				tint(1,1,1)
	def touch_began(self, touch):
		global ded, score, mobx, moby, star1, star2, star3, star4, star5, star6, star7, star8, star9, star10, lazorx, lazory, lazor, alienRect, menu, sheild, gold, ship, ships
		if menu == 1 and ded <=2 and lazor == 0:
			set_volume(1)
			play_effect('arcade:Laser_6')
			set_volume(0.5)
			lazor = 1
			lazory = alienRect.y
			lazorx = alienRect.x
		elif ded >= 3 and touch.location.x >= 35 and touch.location.x <= 265 and touch.location.y >= 100 and touch.location.y <= 150:
			play_effect('arcade:Powerup_1')
			ded = 0
			try:
				with open('laserSheild', 'r') as f:
					sheild = pickle.load(f)
			except IOError:
					sheild = 0
			if sheild == 1:
				ded = -1
			score = 0
			mobx = randint(1,290)
			moby = 1500
		elif touch.location.x < 51 and touch.location.y < 51 and menu == 3:
			menu = 0
			star1 = randint(1,290)
			star3 = randint(1,290)
			star5 = randint(1,290)
			star7 = randint(1,290)
			star9 = randint(1,290)
			star2 = randint(1,550)
			star4 = randint(1,550)
			star6 = randint(1,550)
			star8 = randint(1,550)
			star10 = randint(1,550)
		elif touch.location.x > 260 and touch.location.y < 51 and menu == 0:
			menu = 4
			star1 = randint(1,290)
			star3 = randint(1,290)
			star5 = randint(1,290)
			star7 = randint(1,290)
			star9 = randint(1,290)
			star2 = randint(1,550)
			star4 = randint(1,550)
			star6 = randint(1,550)
			star8 = randint(1,550)
			star10 = randint(1,550)
		elif touch.location.x > 260 and touch.location.y < 51 and ded >= 3 and not menu == 4:
			menu = 4
			star1 = randint(1,290)
			star3 = randint(1,290)
			star5 = randint(1,290)
			star7 = randint(1,290)
			star9 = randint(1,290)
			star2 = randint(1,550)
			star4 = randint(1,550)
			star6 = randint(1,550)
			star8 = randint(1,550)
			star10 = randint(1,550)
		elif menu == 3 and touch.location.x >=120 and touch.location.x <= 180 and touch.location.y >= 100 and touch.location.y <= 160:
			if sheild == 0:
				if gold >= 60:
					sheild = 1
					gold = gold - 60
					with open('laserSheild', 'w+') as f:
							pickle.dump(sheild, f)
					with open('laserGold', 'w+') as f:
							pickle.dump(gold, f)
		elif menu == 3 and touch.location.x >=220 and touch.location.x <= 280 and touch.location.y >= 100 and touch.location.y <= 160:
			if ships == 0:
				if gold >= 100:
					ship = 1
					ships = 1
					gold = gold - 100
					with open('laserShip', 'w+') as f:
							pickle.dump(ship, f)
					with open('laserShips', 'w+') as f:
							pickle.dump(ships, f)
					with open('laserGold', 'w+') as f:
							pickle.dump(gold, f)
		elif touch.location.x > 50 and touch.location.x < 150 and touch.location.y > 400 and touch.location.y < 500 and menu == 4:
			ship = 0
			with open('laserShip', 'w+') as f:
							pickle.dump(ship, f)
		elif touch.location.x > 200 and touch.location.x < 300 and touch.location.y > 400 and touch.location.y < 500 and menu == 4 and ships == 1:
			ship = 1
			with open('laserShip', 'w+') as f:
							pickle.dump(ship, f)
		elif touch.location.x < 51 and touch.location.y < 51 and not menu == 3 and not menu == 1:
			menu = 3
			star1 = randint(1,290)
			star3 = randint(1,290)
			star5 = randint(1,290)
			star7 = randint(1,290)
			star9 = randint(1,290)
			star2 = randint(1,550)
			star4 = randint(1,550)
			star6 = randint(1,550)
			star8 = randint(1,550)
			star10 = randint(1,550)
		elif menu == 0:
			menu = 1
			ded = 0
			if sheild == 1:
				ded = -1
		elif touch.location.x < 51 and touch.location.y < 51 and ded >= 3 and menu == 1:
			menu = 3
			star1 = randint(1,290)
			star3 = randint(1,290)
			star5 = randint(1,290)
			star7 = randint(1,290)
			star9 = randint(1,290)
			star2 = randint(1,550)
			star4 = randint(1,550)
			star6 = randint(1,550)
			star8 = randint(1,550)
			star10 = randint(1,550)
		
run(MyScene(),PORTRAIT)
