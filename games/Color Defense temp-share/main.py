# coding: utf-8

# https://forum.omz-software.com/topic/3261/instead-of-a-question-i-d-like-to-share-my-accomplishments/4

# https://drive.google.com/folderview?id=0B5-adIslOLy_QUZsUDRwREhOTkk&usp=sharing

from button import *
from color import *
from gameobjects import *


class MainMenu(scene.Scene):
	
	#Each scene has a similar variable. It simply holds the last button which was successfully pressed.
	pressedbutton = False

	def setup(self):

		self.buttonlist = []		#Keeps track of all scene buttons in one list for reference.
		
		
		#Each button is created. The node is added to the scene within the button module. Each button is appended to the list as well.
		self.start = Button(self, middlex, 300, 180, 50, text = "New Game", color = 'yellow', textcolor = 'cyan')
		self.buttonlist.append(self.start)
        
		self.resume = Button(self, middlex, 230, 180, 50, text = "Resume Game", color = 'red', textcolor = 'brown', altcolor = 'blue', alttextcolor = 'black')
		self.buttonlist.append(self.resume)

		self.prefs = Button(self, middlex, 160, 180, 50, text = "Preferences")
		self.buttonlist.append(self.prefs)

		self.quit = Button(self, middlex, 90, 180, 50, text = "Quit")
		self.buttonlist.append(self.quit)
	
    

	def touch_began(self, touch):
		self.get_button_touched(touch.location)		#Just calls the method which figures out what button was pressed.


	def touch_ended(self, touch):
		z = False		#Z has to have a state whether or not a button was pressed. True = button was pressed.
		
		#If any button has been stored in 'pressedbutton', check and see if it's still being touched now.
		if not MainMenu.pressedbutton == False:
			MainMenu.pressedbutton.press_done()
		
			temprect = scene.Rect()
			temprect = MainMenu.pressedbutton.node.frame
			z = temprect.contains_point(touch.location)
		
		#If it's still being touched, run the appropriate code for that button.
		if z == True:
 
			if MainMenu.pressedbutton == self.start:
			
				nextscene = GameScene()
				self.view.scene = nextscene
				nextscene.setup()
        
			elif MainMenu.pressedbutton == self.resume:
				pass
            
			elif MainMenu.pressedbutton == self.prefs:
				pass
            
			elif MainMenu.pressedbutton == self.quit:
				mainview.close()

		MainMenu.pressedbutton = False		#Clear the variable.


	def get_button_touched(self, loc):

		#Check every button in the list to see if it has been touched. If it has, store it in 'pressedbutton' and return.
		for i in range(len(self.buttonlist)):

			temprect = scene.Rect()
			temprect = self.buttonlist[i].node.frame
			z = temprect.contains_point(loc)

			if z == True:
				self.buttonlist[i].was_pressed(loc)
				MainMenu.pressedbutton = self.buttonlist[i]
				return




#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================




class GameScene(scene.Scene):

	pressedbutton = False
	buypanel = False		#Perhaps a better way to do this? It's there so that buypanel.node can be referenced outside of this class.
	selectedtower = (1,1,1)
	
	colornode = False

	def setup(self):

		self.buttonlist = []
		
		self.greypath = ui.Path.rect(0,0 , 670,380)
		self.greynode = scene.ShapeNode(self.greypath, color = (0.25,0.25,0.25), position = (2,4))
		self.greynode.anchor_point = (0,0)
		self.add_child(self.greynode)
		
		self.map = Map(self)
		self.add_child(self.map.node)
		self.buttonlist.append(self.map)
        
		self.panel = BuyPanel()
		self.panel.setup()
		
		self.path = ui.Path.rect(0, 0, size.x, 34)
		self.panelnode = scene.ShapeNode(self.path, fill_color = 'black', stroke_color = 'yellow', position = (middlex, size.y - 17))
		self.add_child(self.panelnode)


		self.mainmenu = Button(self, self.size.x - 29, 15, 59, 30, text = "Menu", rounded = False, color = 'cyan', bordercolor = 'blue')
		self.buttonlist.append(self.mainmenu)
    
		self.buypanel = Button(self, self.size.x - 31, self.size.y - 17, 58, 28, text = "Buy", rounded = False)
		GameScene.buypanel = self.buypanel
		self.buttonlist.append(self.buypanel)
	
		self.next = Button(self, 31, self.size.y - 17, 58, 28, text = "Next", rounded = False)
		self.buttonlist.append(self.next)
	
		self.colorpath = ui.Path.rect(0,0, 20, 20)
		self.colornode = scene.ShapeNode(self.colorpath, color = 'blue', position = (self.buypanel.node.position.x - 45, size.y - 17))
		GameScene.colornode = self.colornode
		self.add_child(self.colornode)
    

	def touch_began(self, touch):
	
		self.get_button_touched(touch.location)
	


	def touch_ended(self, touch):
		z = False
    
		if not GameScene.pressedbutton == False:
			GameScene.pressedbutton.press_done()
		
		
			temprect = scene.Rect()
			temprect = GameScene.pressedbutton.node.frame
		
			z = temprect.contains_point(touch.location)
		
		if z == True:
		
			if GameScene.pressedbutton == self.mainmenu:
				nextscene = MainMenu()
				self.view.scene = nextscene
				nextscene.setup()

			elif GameScene.pressedbutton == self.buypanel:
				self.panel.animate_in()
				self.present_modal_scene(self.panel)
				
			elif GameScene.pressedbutton == self.next:
				pass

		GameScene.pressedbutton = False




	def get_button_touched(self, loc):

		for i in range(len(self.buttonlist)):

			temprect = scene.Rect()
			temprect = self.buttonlist[i].node.frame
			z = temprect.contains_point(loc)

			if z == True:
				self.buttonlist[i].was_pressed(loc)
				GameScene.pressedbutton = self.buttonlist[i]



#====================================================================================================================================================================================
#====================================================================================================================================================================================
#====================================================================================================================================================================================



class BuyPanel(scene.Scene):

	pressedbutton = False

	def __init__(self):

		self.buttonlist = []
		
		#Stuff for the 'create' button animation
		self.target = 1
		self.r = 1
		self.g = 0
		self.b = 0
		self.s = 0.005
		self.br = 0
		self.bg = 1
		self.bb = 1
		
		#A black rectangle used to "fade" the background when the buypanel comes up
		self.path2 = ui.Path.rect(0, 0, size.x, size.y)
		self.greynode = scene.ShapeNode(self.path2, fill_color = 'black', position = (middlex, middley))
		self.greynode.alpha = 0.5
		self.add_child(self.greynode)
		
		# Color spectrum backing
		self.path3 = ui.Path.rect(0,0, 375, 75)
		self.bgnode2 = scene.ShapeNode(self.path3, color = 'black', stroke_color = 'yellow', position = (- 377, 0))
		self.bgnode2.anchor_point = (0,0)
		self.bgnode2.line_width = 1.5
		
		self.spectrum = scene.SpriteNode('Assets/SpectrumBar.png')
		self.spectrum.anchor_point = 0,0
		self.spectrum.position = 5,7
		self.bgnode2.add_child(self.spectrum)
		
		self.slidepath = ui.Path.rect(0,0,5,20)
		self.slidenode = scene.ShapeNode(self.slidepath, color = 'white', position = (3,self.spectrum.size.y - 7))
		self.spectrum.add_child(self.slidenode)

		#The panel backing
		self.path = ui.Path.rect(0, 0, 60, 430)
		self.bgnode = scene.ShapeNode(self.path, fill_color = 'black', stroke_color = 'yellow', position = (size.x-61, 0))
		self.bgnode.anchor_point = 0,0
		self.bgnode.line_width = 1.5
		self.add_child(self.bgnode)
		
		
		self.bgnode.add_child(self.bgnode2)

		
		#Buttons

		self.done = Button(self, 30, size.y - 15, 58, 30, text = "Done", rounded = False, color = 'brown', bordercolor = 'yellow')
		self.buttonlist.append(self.done)
		self.bgnode.add_child(self.done.node)
		
    
		self.default1 = Button(self, 31,	self.done.node.frame.y - 32, 48, 48, text = "", rounded = False, color = (1,0,0), bordercolor = (1,0.5,0.5),
																																				altcolor = (0,0.65,0.45), altbordercolor = (0,1,1))
		self.buttonlist.append(self.default1)
		self.bgnode.add_child(self.default1.node)
	
		self.default2 = Button(self, 31, self.default1.node.frame.y - 29, 48, 48, text = "", rounded = False, color = (1,1,0), bordercolor = (1,1,0.5),
																																				altcolor = (0,0,0.45), altbordercolor = (0,0,1))
		self.buttonlist.append(self.default2)
		self.bgnode.add_child(self.default2.node)
	
		self.default3 = Button(self, 31, self.default2.node.frame.y - 29, 48, 48, text = "", rounded = False, color = (0,1,0), bordercolor = (0.5,1,0.5),
																																				altcolor = (0.45,0,0.45), altbordercolor = (1,0,1))
		self.buttonlist.append(self.default3)
		self.bgnode.add_child(self.default3.node)
	
		self.default4 = Button(self, 31, self.default3.node.frame.y - 29, 48, 48, text = "", rounded = False, color = (0,1,1), bordercolor = (0.5,1,1),
																																				altcolor = (0.45,0,0), altbordercolor = (1,0,0))
		self.buttonlist.append(self.default4)
		self.bgnode.add_child(self.default4.node)
	
		self.default5 = Button(self, 31, self.default4.node.frame.y - 29, 48, 48, text = "", rounded = False, color = (0,0,1), bordercolor = (0.5,0.5,1),
																																				altcolor = (0.45,0.45,0), altbordercolor = (1,1,0))
		self.buttonlist.append(self.default5)
		self.bgnode.add_child(self.default5.node)
		
		self.default6 = Button(self, 31, self.default5.node.frame.y - 29, 48, 48, text = "", rounded = False, color = (1,0,1), bordercolor = (1,0.5,1),
																																				altcolor = (0,0.45,0), altbordercolor = (0,1,0))
		self.buttonlist.append(self.default6)
		self.bgnode.add_child(self.default6.node)
	
		self.create = Button(self, 31, 30, 40, 40, text = "", rounded = False, color = 'white', bordercolor = 'brown', altcolor = 'black', altbordercolor = 'white')
		self.create.node.line_width = 2.5
		self.buttonlist.append(self.create)
		self.bgnode.add_child(self.create.node)
	
	
	def draw(self):
		
		#Only run the animation if it's not being pressed.
		if not BuyPanel.pressedbutton == self.create:
			self.animate_create_button()
		
		
	def animate_create_button(self):
	
		#1,0,0
		
		if self.target == 1:
			self.g += self.s
			if self.g >= 1:
				self.target = 2
				self.g = 1
	
		#1,1,0
		
		if self.target == 2:
			self.r -= self.s
			if self.r <= 0:
				self.target = 3
				self.r = 0
		
		#0,1,0
		
		if self.target == 3:
			self.b += self.s
			if self.b >= 1:
				self.target = 4
				self.b = 1

		#0,1,1
		
		if self.target == 4:
			self.g -= self.s
			if self.g <= 0:
				self.target = 5
				self.g = 0
				
		#0,0,1
		
		if self.target == 5:
			self.r += self.s
			if self.r >= 1:
				self.target = 6
				self.r = 1
				
		#1,0,1
		
		if self.target == 6:
			self.b -= self.s
			if self.b <= 0:
				self.target = 1
				self.b = 0
				
		#1,0,0
		
		self.br = (1 - self.r)
		self.bg = (1 - self.g)
		self.bb = (1 - self.b)
		
		self.create.color = (self.r,self.g,self.b)
		self.create.node.fill_color = (self.r,self.g,self.b)
		self.create.node.stroke_color = (self.br,self.bg,self.bb)


	def touch_began(self, touch):
		
		self.get_button_touched(touch.location)



	def touch_ended(self, touch):
		z = False
	
		if not BuyPanel.pressedbutton == False:
			BuyPanel.pressedbutton.press_done()
		
		
			temprect = scene.Rect()
			temprect = BuyPanel.pressedbutton.node.frame
            
			temprect.x += self.bgnode.frame.x
			temprect.y += self.bgnode.frame.y
		
			z = temprect.contains_point(touch.location)
		
		if z == True:
			if BuyPanel.pressedbutton == self.done:
				#if self.bgnode.position.x == size.x - 60:
				#	self.animate_out()
				pass
        
			elif BuyPanel.pressedbutton == self.default1:
				GameScene.selectedtower = self.default1.color
				
			elif BuyPanel.pressedbutton == self.default2:
				GameScene.selectedtower = self.default2.color
				
			elif BuyPanel.pressedbutton == self.default3:
				GameScene.selectedtower = self.default3.color
				
			elif BuyPanel.pressedbutton == self.default4:
				GameScene.selectedtower = self.default4.color
				
			elif BuyPanel.pressedbutton == self.default5:
				GameScene.selectedtower = self.default5.color
				
			elif BuyPanel.pressedbutton == self.default6:
				GameScene.selectedtower = self.default6.color
				
			elif BuyPanel.pressedbutton == self.create:
				GameScene.selectedtower = self.create.color

			if self.bgnode.position.x == size.x - 60:
				self.animate_out()
				
			GameScene.colornode.color = GameScene.selectedtower
	
		BuyPanel.pressedbutton = False


	def get_button_touched(self, loc):

		for i in range(len(self.buttonlist)):

			temprect = scene.Rect()
			temprect = self.buttonlist[i].node.frame
            
			temprect.x += self.bgnode.frame.x
			temprect.y += self.bgnode.frame.y
            
			z = temprect.contains_point(loc)

			if z == True:
				self.buttonlist[i].was_pressed(loc)
				BuyPanel.pressedbutton = self.buttonlist[i]
				return


	def animate_in(self):
		A = scene.Action
		self.bgnode.position = size.x+380, -1
		self.greynode.alpha = 0
		
		self.bgnode.run_action(A.move_to(size.x-60, -1, 1.2, scene.TIMING_SINODIAL))
		self.greynode.run_action(A.fade_to(0.4, 1, scene.TIMING_SINODIAL))

	def animate_out(self):
		A = scene.Action
		self.bgnode.run_action(A.sequence(A.move_to(size.x+380, -1, 1.2, scene.TIMING_SINODIAL), A.call(self.dismiss_modal_scene)))
		self.greynode.run_action(A.fade_to(0, 1, scene.TIMING_SINODIAL))






random.seed()
size = scene.get_screen_size()
middlex = size.x/2
middley = size.y/2


Menu = MainMenu()

mainview = ui.View()
mainview.multitouch_enabled = False

sceneview = scene.SceneView(frame=mainview.bounds, flex='WH')
sceneview.multitouch_enabled = False

mainview.add_subview(sceneview)
sceneview.scene = Menu
mainview.present(hide_title_bar = True, animated = False)
