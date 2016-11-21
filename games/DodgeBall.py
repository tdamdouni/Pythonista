#A simple game for Pythonista

from scene import *
import console
import random
import sound
from time import time


class Enemy:
	position=None
	direction=None 
	alive=False
	hitBox= None
	
	def __init__(self,Scene):
		position=Point(0,0)
		direction=Point(-1,0)
		alive=False
		hitBox=Rect(position.x+50,position.y+50,100,100)
		
	def spawn(self,Scene):
		wall=random.randint(1,4)
		#1=left 2=top 3=right 4=bottom
		if wall==1:
			self.position=Point(0,random.randint(1,Scene.size.h))
			self.direction=Point(1,0.1*random.randint(1,9))
		if wall==2:
			self.position=Point(random.randint(1,Scene.size.w),Scene.size.h)
			self.direction=Point(0.1*random.randint(1,9),-1)
		if wall==3:
			self.position=Point(Scene.size.w,random.randint(1,Scene.size.h))
			self.direction=Point(-1,0.1*random.randint(1,9))
		if wall==4:
			self.position=Point(random.randint(1,Scene.size.w),0)
			self.direction=Point(0.1*random.randint(1,9),1)
			
		self.alive=True
		return self
	
	
	def update(self):
		self.position.x=self.position.x+10*self.direction.x
		self.position.y=self.position.y+10*self.direction.y
		


class MyScene (Scene):
	score=0
	multiplier=0
	level=1
	State="Menu"
	lives=5
	player_pos=None
	enemies=[]
	temp=Enemy
	flash_anim=False
	EnemyTimer=None
	StartTime=None
	EnemySpawnTime=0.7
	
	def setup(self):
		pass
		
	def StartGame(self):
		MyScene.EnemyTimer=time()
		MyScene.StartTime=time()
		MyScene.score=0
		MyScene.lives=5
		MyScene.level=1
		MyScene.enemies[:]=[]
		self.player_pos=Point(self.size.w/2,self.size.h/2)
		
	def UpdateGame(self):
		#update score and multipler
		MyScene.multiplier=1
		MyScene.score=MyScene.score+MyScene.multiplier
		
		#update level and difficulty
		if time()-MyScene.StartTime > MyScene.level*5:
			MyScene.level=MyScene.level+1
		
		#spawn enemies
		if time()-MyScene.EnemyTimer >= MyScene.EnemySpawnTime:
			for spawn in range(0,MyScene.level):
				self.enemies.append(Enemy(self).spawn(self))
			MyScene.EnemyTimer=time()
		
		#update dem enemies and do collision
		for enemy in self.enemies:
			enemy.update()
			#for touch in self.touches.values():
			if(self.player_pos.distance(enemy.position)<=100):
				sound.play_effect('Drums_10')
				enemy.alive=False
				MyScene.lives=MyScene.lives-1
				self.enemies.remove(enemy)
				flash_anim=True
			#clear enemies that are long gone
			if (enemy.position.x>self.size.w+100 or enemy.position.x<-100 \
			or enemy.position.y>self.size.h+100 or enemy.position.y<-100):
				enemy.alive=False
				self.enemies.remove(enemy)
			
			
		if(MyScene.lives<=0):
			MyScene.State="GameOver"			
			
			
		
	def drawText(self):
		tint(0,0,0)
		text("Score: "+str(MyScene.score)+"     Level: "+str(MyScene.level)+"     Lives: "+str(MyScene.lives), font_name="Helvetica",x=275,y=self.size.h-50,font_size=24)
			
	def drawEnemies(self):
		fill(1,0,0)
		for enemy in self.enemies:
			fill(1,1,1)
			ellipse(enemy.position.x-55,enemy.position.y-55,110,110)
			fill(1,0,0)		
			ellipse(enemy.position.x-50,enemy.position.y-50,100,100)
			
	
	def drawPlayer(self):
		fill(0, 1, 0)
		for touch in self.touches.values():
			if(self.player_pos.distance(touch.location)<=100 and len(self.touches)!=0):
				self.player_pos=touch.location
		image('_player3',self.player_pos.x - 50, self.player_pos.y - 50, 100, 100)
	
	def drawGame(self):
		#called every frame, about 60fps
		background(0,0,0)
		tint(1,1,1)
		image('_db_bkg',0,0,self.size.w,self.size.h)
		self.UpdateGame()
		self.drawEnemies()
		self.drawPlayer()
		self.drawText()
	
	def drawGameOver(self):
		background(0,0,0)
		tint(1,1,1)
		#image('_db_bkg',0,0,self.size.w,self.size.h)
		tint(1,0,0)
		text("YOU LOSE!",font_name='Helvetica',x=self.size.w/2,y=3*self.size.h/4,font_size=128,alignment=5)
		text("SCORE: "+str(MyScene.score),font_name="Helvetica",x=self.size.w/2,y=2*self.size.h/4,font_size=64,alignment=5)
		fill(0,0,0)
		rect(self.size.w/2-200,2*self.size.h/4-200,400,100)
		tint(1,0,0)
		text("Main Menu",font_name="Helvetica",x=self.size.w/2,y=2*self.size.h/4-150,font_size=64,alignment=5)
		
	def drawMenu(self):
		background(0,0,0)
		tint(1,1,1)
		image('_db_bkg',0,0,self.size.w,self.size.h)
		fill(0,0,0)
		#rect(self.size.w/2-100,3*(self.size.h/4)-450,200,100)
		tint(0,0,0)
		text("DODGE BALL!",font_name='Helvetica',x=self.size.w/2,y=3*self.size.h/4,font_size=64,alignment=5)
		tint(0,0,0)
		text("Start!",font_name='Helvetica',x=self.size.w/2,y=3*(self.size.h/4)-400,font_size=64,alignment=5)
		
	def drawError(self):
		background(1,0,0)
		tint(1,1,1)
		text("FATAL DRAW ERROR! OH NO!",font_name='Helvetica',x=self.size.w/2,y=self.size.h/2, font_size=32,alignment=5)
		
	
	def draw(self):
		if MyScene.State=="Game":
			MyScene.drawGame(self)
		elif MyScene.State=="GameOver":
			MyScene.drawGameOver(self)
		elif MyScene.State=="Menu":
			MyScene.drawMenu(self)
		else:
			MyScene.drawError(self)
		
	
	def Menu_touch_began(self, touch):
		fill(1,0,0)
		touched=Rect(touch.location.x,touch.location.y,1,1)
		startButton=Rect((self.size.w/2)-100,3*(self.size.h/4)-450,200,100)
		if(touched.intersects(startButton)):
			MyScene.StartGame(self)
			MyScene.State="Game"
			
	def GameOver_touch_began(self, touch):
		touched=Rect(touch.location.x,touch.location.y,1,1)
		menuButton=Rect(self.size.w/2-200,2*self.size.h/4-200,400,100)
		if(touched.intersects(menuButton)):
			MyScene.State="Menu"
			
	def touch_began(self, touch):
		if MyScene.State=="Menu":
			MyScene.Menu_touch_began(self,touch)
		
		elif MyScene.State=="GameOver":
			MyScene.GameOver_touch_began(self,touch)
			
		else:
			pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass
		
	def end_level(self,touch):
		background(1,0,0)

run(MyScene())
