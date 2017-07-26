# coding : utf-8

# https://forum.omz-software.com/topic/3479/why-does-is-there-an-error-ocurring-in-my-script

from scene import *
from random import *
#from game_menu import ButtonNode
import sound
import random
#This module is not preset, its just the one I'm working on, if you ask what is this.
import _scene_Physics
A = Action

class Powerup(SpriteNode):

	def __init__(self, **kwargs):
		SpriteNode.__init__(self, "plf:Item_Star", **kwargs)
		
class Main(Scene):

	def shoot(self, type):
		if type == "up":
			self.laser_target_y = get_screen_size()[1]
		if type == "down":
			self.laser_target_y = -768
		if self.powerupActivated == True:
			self.laser_target_y = 768 if type == "up" else -768
		self.la = SpriteNode('spc:LaserGreen12', parent=self)
		self.la.position = self.al.position + (0, 30)
		self.la.z_position = 1
		self.lasersOnScreen.insert(1, self.la)
		actions = [A.move_by(0, self.laser_target_y), A.remove()]
		self.la.run_action(A.sequence(actions))
		self.lasersOnScreen.insert(1, self.la)
		sound.play_effect('digital:Laser4')
		
	def setup(self):
		_scene_Physics.Gravity.initGravity({"power" : 10})
		self.powerupActivated = False
		self.playerLevel = 1
		self.bricksOnScreen = []
		self.lasersOnScreen = []
		self.levelLabel = LabelNode("Level %s" % (self.playerLevel), ("Futura", 20), position=(40, 710), z_position = 1.0, parent=self)
		self.la = None
		self.bgimage = SpriteNode("spc:BackgroundPurple", position=(get_screen_size()[0]/2, get_screen_size()[1]/2), size=(get_screen_size()[0], get_screen_size()[1]), parent=self)
		self.al = SpriteNode("plf:AlienGreen_front", position=(512, 400), parent=self)
		self.shoot_button = ButtonNode("Shoot", parent=self)
		self.shoot_button.position = (924, 40)
		self.obstacleSpawnButton = ButtonNode("Spawn a brick", parent=self)
		self.upgradeStr = "Upgrade(Cost:100pts)"
		self.upgradeToNextLevelButton = ButtonNode(self.upgradeStr, parent=self)
		self.shootDownButton = ButtonNode("Shoot Down", parent=self)
		self.shootDownButton.position = (924, 100)
		self.upgradeToNextLevelButton.position = (512, 40)
		self.obstacleSpawnButton.position = (100, 40)
		self.score = 0
		self.scoreLabel = LabelNode(str(self.score), ("Futura", 20), parent=self)
		self.scoreLabel.position = (40, 740)
		self.scoreLabel.z_position = 1.0
		self.shootWith2 = False
		self.upgradeCost = 100
		
	def touch_ended(self, touch):
		touch_loc = self.point_from_scene(touch.location)
		if touch_loc in self.shoot_button.frame:
			self.shoot(type = "up")
		if touch_loc in self.obstacleSpawnButton.frame:
			o = self.spawn_random_brick()
			self.bricksOnScreen.insert(1, o)
			del o
		if touch_loc in self.upgradeToNextLevelButton.frame:
			if self.score >= self.upgradeCost or self.score == self.upgradeCost:
				self.score -= self.upgradeCost
				self.scoreLabel.text = str(self.score)
				self.playerLevel += 1
		if touch_loc in self.shootDownButton.frame:
			self.shoot(type = "down")
			
	def check_collisions(self):
		if self.lasersOnScreen:
			for brickOnScreen in self.bricksOnScreen:
				for laserOnScreen in self.lasersOnScreen:
					if laserOnScreen.position in brickOnScreen.frame:
						brickOnScreen.run_action(A.remove())
						sound.play_effect(random.choice(["Explosion_1", "Explosion_2", "Explosion_3"]))
						if brickOnScreen in self.bricksOnScreen:
							self.bricksOnScreen.remove(brickOnScreen)
						if random.randint(1, 5) == 4 and self.powerupActivated == False:
							self.pup = Powerup(parent=self)
							self.pup.position = brickOnScreen.position
							actions = [A.move_to(100, 10), A.call(self.powerupActive), A.wait(18), A.call(self.powerupDesactive), A.remove()]
							self.pup.run_action(A.sequence(actions))
						self.score += random.randint(1, 10)
						self.scoreLabel.text = str(self.score)
						if not self.la == None:
							if self.la in self.lasersOnScreen and self.powerupActivated == False:
								self.lasersOnScreen.remove(self.la)
								self.la.run_action(A.remove())
								
	def touch_moved(self, touch):
		touch_loc = self.point_from_scene(touch.location)
		if touch_loc in self.al.frame:
			self.al.position = touch_loc
			
	def spawn_random_brick(self):
		obstacles = ["pzl:Blue8", "pzl:Purple8", "pzl:Yellow4"]
		obstacleName = random.choice(obstacles)
		brick = SpriteNode(obstacleName, position=(random.randint(1, get_screen_size()[0]), random.randint(1, get_screen_size()[1])), parent=self)
		_scene_Physics.Gravity.gravity(_scene_Physics.Gravity(), brick)
		return brick
		
	def update(self):
		self.check_collisions()
		self.levelLabel.text = "Level %s" % (self.playerLevel)
		
	def powerupActive(self):
		self.powerupActivated = True
		
	def powerupDesactive(self):
		self.powerupActivated = False
		
if __name__ == "__main__":
	run(Main(), LANDSCAPE, show_fps=True)
# --------------------

	"""def update(self):
	self.check_collisions()
	self.levelLabel.text = "Level %s" % (self.playerLevel)"""
# --------------------
#_scene_Physics.Gravity.initGravity({"power" : 10})
# --------------------

