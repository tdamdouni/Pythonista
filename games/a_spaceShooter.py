# https://gist.github.com/anonymous/a03bfdab757c1d978061

from scene import *
from random import randint, uniform, choice
import sound
#sound.play_effect('Explosion_1')

statusY = 700
statusSizeY = 68

def outOfBounds(pos, sSize): #Position, Screen Size
	if pos.x > sSize.w+100 or pos.x < -100 or pos.y > sSize.h+100 or pos.y < -100:
		return True
	return False
	
#Hit test function used for bullets
def hit(loc1, loc2, size2):
	if loc1.x>loc2.x and loc1.x<loc2.x+size2.x:
		if loc1.y>loc2.y and loc1.y<loc2.y+size2.y:
			return True

#Returns the distance range between two objects based on x,y
def dif(loc1,loc2):
 if loc1.x>loc2.x: difx=loc1.x-loc2.x
 else: difx=loc2.x-loc1.x
 if loc1.y>loc2.y: dify=loc1.y-loc2.y
 else: dify=loc2.y-loc1.y
 return difx+dify
 
# Draws a healthbar
def healthBar(loc,health,shield):
	fill(1, 0, 0) #Damaged
	rect(loc.x-17.5,loc.y+25,33,5)
	if health>0:
		fill(0, 1, 0) #Health
		rect(loc.x-17.5,loc.y+25,health/3,5)
	if shield>0:
		fill(0, 0, 1) #Shield
		rect(loc.x-17.5,loc.y+25,shield/3,5)

# Draws status info
def status(self):
	fill(0,0,0)
	rect(0,statusY,1024,statusSizeY)
	#scene.text(txt, font_name='Helvetica', font_size=16.0, x=0.0, y=0.0, alignment=5)
	text('Wave: '+str(self.wave), 'Chalkduster', 16., 200, statusY+10,  3)
	if self.shield[1]<0: text('Shield: 0', 'Chalkduster', 16., 50, statusY+10,  3)
	else: text('Shield: '+str(int(self.shield[1])), 'Chalkduster', 16., 50, statusY+10,  3)
	if self.health<0:     text('Health: 0', 'Chalkduster', 16., 50, statusY+26,  3)
	else: text('Health: '+str(self.health), 'Chalkduster', 16., 50, statusY+26,  3)
	
# Just combines set_volume and play_effect
def playSound(name,volume):
	sound.set_volume(volume)
	sound.play_effect(name)
 
# Bullet class.
class bullet (object):
	def __init__(self, position, velocity, type):
		self.pos = position
		self.vel = velocity
		self.type = type
		self.special = 0 #Used for missiles

#Exploding bullet particles
class bulletParticle (object):
	def __init__(self, position, velocity):
		self.pos = position
		self.vel = velocity
		
#Exploding bullet effect
class bulletExplosion (object):
	def __init__(self, position, velocity,ship=False):
		self.ship = ship
		self.particles = set()
		self.alpha = 1
		if ship: 
			loop=15
			velocity.x*=-.1
		else: loop=2
		for i in range(loop):
			if ship: divide = (i+1)/3.
			else: divide = i+3
			self.particles.add(bulletParticle(Point(position.x, position.y), 
			                                  Point( (velocity.x+randint(-1,1)) / divide,
			                                         (velocity.y+randint(-1,4)) / divide ) ) )

class enemy (object):
	def __init__(self, position, velocity, type, shield=0):
		self.pos = position
		self.vel = velocity
		self.target = Point(position.x, position.y)
		self.type = type
		self.health = 100
		self.shield = [100,shield] #0 is 'max', 1 is 'current'.  Shield recharges.
		self.bulletLoop = 0

class MyScene (Scene):
	#def should_rotate(self,orientation):
	#	return False
	def setup(self):
		self.wave = 0 # The more waves, the harder the game becomes.
		self.speed = 20 # How quickly player moves
		self.vel = Point(0, 0) # Velocity
		self.pos = Point(100, 384) # Position
		self.target = Point(self.pos.x, self.pos.y) #Touch target
		self.health = 100
		self.shield = [100,50] # 0 is 'max', 1 is 'current'
		self.bullets = set() # A set containing all active bullets. 
		self.bulletLoop = 0  # Used to determine when to shoot bullets
		self.bulletSpeed = 7 # The rate bullets are fired.
		self.bulletSpecial = 0 # When the player gets a bonus, this is used as a timer
		self.bulletType = 0#randint(0,2) # 0=normal.  1=missile.  2=cluster bullet
		self.bulletExplosions = set() # Exploding bullets.  Purely aesthetic.
		self.bonus = set() # Bonuses the player can collect to change bulletType and bulletSpecial
		self.enemies = set() # A set containing all active enemies
		self.stun = 0 #This timer is also aesthetic and makes the scene look strange when hit
		self.mute = False # Used for muting sound.  May increase performance?
		self.screen = 1 # If screen=0, play scene.  Otherwise, draw screens.
	
	def draw(self):
		
		#Stun is the background.  To create the stun effect, simply don't draw a full
		#background. Leave some parts transparent so it only overlaps the last draw()
		if self.stun<0:
			fill(0,0,0,self.stun+1) #Replace with background for trippy effects
			rect(0,0,1024,768)
			self.stun+=.005
		else:
			background(0, 0, 0)
		
		#Start with screens.
		if self.screen:
			if self.screen==1:
				text('eliskan space shooter v1.0\n   \"They shoot, you die.\"', 'Chalkduster', 25., 512, 384,  2)
			elif self.screen==2:
				text('That had to hurt! Ouch...\n     Click to restart.', 'Chalkduster', 25., 512, 384,  2)
			return
			
		# bulletSpecial is turned on by hitting 'bonus' items.	
		if self.bulletSpecial >= 0:
			self.bulletSpecial -= 1
			if self.bulletSpecial < 0:
				self.bulletType = 0
				self.bulletSpecial = 0
				self.bulletSpeed = 7
				
		# Move towards touch
		if self.pos.y < self.target.y - 1 or self.pos.y > self.target.y + 1:
			self.pos.y = ((self.pos.y*self.speed) + self.target.y) / (self.speed + 1)
		# Draw a blue box for player
		fill(0, 0, 1)
		rect(self.pos.x-20, self.pos.y-20, 40, 40)
		
		#Handle shield and health bar
		if self.shield[1]<self.shield[0]:
			healthBar(self.pos, self.health, self.shield[1])
			self.shield[1] += .1
		
		# SHOOT BULLETS
		self.bulletLoop += 1
		if self.bulletLoop > self.bulletSpeed:
			self.bulletLoop = 0
			newBullet = bullet(Point(self.pos.x,self.pos.y), Point(8,0),self.bulletType)#randint(0,2))
			self.bullets.add(newBullet)
			
		# NEW WAVE
		if len(self.enemies) == 0:
			self.bullets = set()
			self.bulletExplosions = set()
			self.wave += 1
			for i in range(self.wave+20):
				newEnemy = enemy(Point(self.size.w,randint(0,self.size.h-statusSizeY)),Point(4,4),0,100)
				newEnemy.target.x = randint(300,600)
				self.enemies.add(newEnemy)
			
		#BULLETS
		deadBullets = set()
		newBullets = set()
		deadEnemies = set()
		bulletHit = False #Used for sound
		bulletHitPlayer = False #Used for sound
		for bull in self.bullets:
			smallestDif = 300
			if bull.type < 10: #If bullet is used by player
				if bull.type == 0: fill(0, 0, 1)  #Bullet color = blue: 'bullet'
				elif bull.type == 1: fill(0, 1, 0)#Bullet color = green: 'missile'
				else: fill(0.40, 1.00, 0.80)    #Bullet color = spindrift: 'cluster bomb'
				for enemies in self.enemies:
					if bull.type == 1:
						difference = dif(enemies.pos, bull.pos)
						if difference < smallestDif:
							smallestDif = difference
							target = enemies
							
					#Hit enemies
					if hit(bull.pos,Point(enemies.pos.x-10,enemies.pos.y-10),Point(20,20)): 
						if bull.type == 2: #Cluster bombs spawn missiles when they hit enemy
							for i in range(10):
								#tempInt=randint(0,2)
								newBullet=bullet(Point(bull.pos.x-20,bull.pos.y),
								                      Point((bull.vel.x+uniform(-2., 2.))*-1,
								                            (bull.vel.y+uniform(-2., 2.))*-1), 1)
								newBullets.add(newBullet)
						bulletHit = True
						deadBullets.add(bull)
						self.bulletExplosions.add(bulletExplosion(bull.pos,bull.vel))
						if enemies.health > 0:
							if enemies.shield[1] > 0: enemies.shield[1] -= 20
							else: enemies.health -= 20
						else: 
							deadEnemies.add(enemies)
							self.bulletExplosions.add(bulletExplosion(enemies.pos,enemies.vel,True))
							if randint(1,3)==1: #Random chance to drop a bonus.
								self.bonus.add(Point(enemies.pos.x-10,enemies.pos.y-10))
			else: #Bullet is used by enemy
				if bull.type == 11:
					fill(1, 0, 0) #Enemy bullet = red: 'missile'
					difference=dif(self.pos,bull.pos)
					if difference<smallestDif:
							smallestDif=difference
							target = self
				else: 
					fill(1, 1, 0) #Enemy bullet = yellow: 'bullet'
					smallestDif = 300
				
				# Damaging the player
				if hit(bull.pos, Point(self.pos.x-20,self.pos.y-20), Point(40,40)):
					bulletHitPlayer = True
					if self.shield[1] > 0: self.shield[1] -= 20
					else: 
						self.health -= 10
						self.stun = -1
					deadBullets.add(bull)
					self.bulletExplosions.add(bulletExplosion(bull.pos,bull.vel))
					if self.health <= 0:
						self.screen = 2
					
			if bull.type == 1 or bull.type == 11: #Missiles
				if smallestDif != 300:
					if bull.type == 1: fill (0.00, 0.70, 0.10)	# Bullet color = clover: 'missile activated'
					else: fill(1, 0, 1) #Enemy bullet = purple: 'missile activated'
					if bull.special < 125:
						bull.special += 1
					else: 
						deadBullets.add(bull)
						self.bulletExplosions.add(bulletExplosion(bull.pos,bull.vel))
					mod = 20
					bull.vel.x+=(target.pos.x-bull.pos.x)/(difference)
					bull.vel.y+=(target.pos.y-bull.pos.y)/(difference)
					if bull.vel.x>10 or bull.vel.x<-10: bull.vel.x/=1.1
					if bull.vel.y>10 or bull.vel.y<-10: bull.vel.y/=1.1
			bull.pos.x += bull.vel.x
			bull.pos.y += bull.vel.y
			if outOfBounds(bull.pos,self.size): deadBullets.add(bull)
			ellipse(bull.pos.x-2, bull.pos.y-2, 4, 4)
		self.bullets -= deadBullets
		for newBullet in newBullets:
			if len(self.bullets)<50-self.wave: self.bullets.add(newBullet)
		self.enemies -= deadEnemies
						
		# ENEMIES
		enemiesShoot = False #Used for sound
		for enemies in self.enemies:
			if enemies.pos.y > self.size.h-statusSizeY or enemies.pos.y < 0:
				enemies.vel.y *= -1
			if enemies.pos.x > enemies.target.x:
				enemies.pos.x = ((enemies.pos.x*800) + enemies.target.x) / 801
			if enemies.bulletLoop > 200:
				enemies.bulletLoop = 0
				enemiesShoot = True
				newBullet=bullet(Point(enemies.pos.x, enemies.pos.y),
				                 Point(-8,0), randint(11,12))
				self.bullets.add(newBullet)
			else: enemies.bulletLoop += 1
			enemies.pos.y += enemies.vel.y
			fill(1, 0, 0)
			ellipse(enemies.pos.x-10, enemies.pos.y-10, 20, 20)
			if enemies.shield[1] < enemies.shield[0]:
				enemies.shield[1] += .1
				healthBar(enemies.pos, enemies.health, enemies.shield[1])
		
		# EXPLOSIONS
		deadExplosions=set()
		for explosion in self.bulletExplosions:
			explosion.alpha -= .01
			if explosion.alpha > 0:
				for particle in explosion.particles:
					particle.pos.x += particle.vel.x
					particle.pos.y += particle.vel.y
					if explosion.ship==True: 
						fill(1, 0, 0, explosion.alpha)
						ellipse(particle.pos.x-(explosion.alpha*5), particle.pos.y-(explosion.alpha*5),
						         (explosion.alpha*10),  (explosion.alpha*10))
					else: 
						fill(1, 1, 1, explosion.alpha)
						#ellipse(particle.pos.x-1, particle.pos.y-1, 2, 2)
						rect(particle.pos.x-1, particle.pos.y-1, 2, 2)
			else: deadExplosions.add(explosion)
		self.bulletExplosions -= deadExplosions
		
		# BONUSES
		deadBonus = set()
		bonusSound = False
		for bonus in self.bonus:
			fill(0,0,1,1)
			ellipse(bonus.x, bonus.y, 20, 20)
			bonus.x -= 4
			if bonus.x < 0: deadBonus.add(bonus)
			elif hit(bonus, Point(self.pos.x-20,self.pos.y-20), Point(40,40)):
				bonusSound = True
				deadBonus.add(bonus)
				randBullet = randint(1,5)
				if randBullet == 1:
					self.bulletType = 1
					self.bulletSpecial = 800
					self.bulletSpeed = 5
				elif randBullet == 2:
					self.bulletType = 2
					self.bulletSpecial = 1000
					self.bulletSpeed = 20
				elif randBullet == 3:
					self.bulletType = 2
					self.bulletSpecial = 150
					self.bulletSpeed = 5
				elif randBullet == 4:
					self.bulletType = 1
					self.bulletSpecial = 400
					self.bulletSpeed = 2
				elif randBullet == 5:
					self.bulletType = 0
					self.bulletSpecial = 600
					self.bulletSpeed = 1
		self.bonus -= deadBonus
		
		#Sounds
		if not self.mute:
			if deadEnemies:
				playSound('Hit_2', 0.1)
			elif bonusSound:
				playSound('Jump_3',0.1)
			elif enemiesShoot:
				playSound('Laser_4', 0.1)
			elif bulletHitPlayer:
				playSound('Powerup_3', 0.1)
			elif self.bulletLoop==0:
				playSound('Laser_6', 0.05)
			elif bulletHit:
				playSound('Hit_1', 0.1)
		
		#Status
		status(self)
	
	def touch_began(self, touch):
		self.target = touch.location
	def touch_moved(self, touch):
		self.target = touch.location
	def touch_ended(self, touch):
		if self.screen:
			#if self.screen == 1:
			if self.screen == 2:
				self.bonus = set()
				self.bullets = set()
				self.enemies = set()
				self.bulletExplosions = set()
				self.wave = 0
				self.shield = [100,100]
				self.health = 100
			self.screen = 0
		self.target = touch.location

run(MyScene(), LANDSCAPE, 2)
