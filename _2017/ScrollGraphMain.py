# https://gist.github.com/rogerstedman/13a36a95cfee655b4ff88445a53e476d

#ScrollGraph is my first foray into Pythonista and GitHub
#I have written this a a generic UI component for the purpose writing a Mechanical Ventilator Simulator programme (coming soon!)
#I thought I would share as it has generalisable applications
#Think of it as a kind of rather sedate oscilloscope - or wave form on a mechanical ventilator or patient monitor...
#Please do use and or adapt - However if you do please acknowledege my authorship

#Written by Dr Roger Stedman - December 2017 - www.rogerstedmn.com

import ui
from scene import *
import math,random


#This class defines the generic shapenode that is the animated plot on the screen (a simple vertical line)
class PlotLine (ShapeNode):
	def __init__(self, **kwargs):
		ShapeNode.__init__(self, **kwargs)

#This class defines a simple label that is the title of the scrolling graph		
class Label (LabelNode):
	def __init__(self, **kwargs):
		LabelNode.__init__(self, **kwargs)
		
#This is the little icon in the top right corner that brings up the popover to adjust the scrolling graph attributes	
class Button (SpriteNode):
	def __init__(self,**kwargs):
		SpriteNode.__init__(self,'iow:navicon_24',**kwargs)

#As the name suggests this class draws the axes into an image context which is then passed to a spritenode to be displayed.  
#Setting this up as a separate node allows the axis to be removed and redrawn as required		
class Axis (SpriteNode):
	def __init__(self,width,height,label_range,x_position, **kwargs):
		with ui.ImageContext(width,height) as ctx:
			ui.set_color('white')
			x_axis_path = ui.Path.rect(0,height-x_position-2,width,2)
			x_axis_path.stroke()
			x_axis_path.fill()
			y_axis_path = ui.Path.rect(0,0,2,height)
			y_axis_path.stroke()
			y_axis_path.fill()
		
			for counter in range(label_range+1):
				x = counter*(int(width/label_range))
				x_axis_ticks_path = ui.Path.rect(x,height-x_position-8,2,8)
				x_axis_ticks_path.stroke()
				x_axis_ticks_path.fill()
				ui.draw_string(str(counter), rect=(x+5,(height - x_position)-15,15,15), color = 'white')
			img = Texture(ctx.get_image())
			SpriteNode.__init__(self, img, **kwargs)

#The Signal class is a model class that generates a signal for a ScrollGraph.  
#Each time an ScrollGraph is invoked a Signal must be invoked as well
#this is done by instantiating the signal class and passing it to the set_signal_type method in ScrollGraph 
#along with the name of the signal type you want displayed.  
#This particular Signal class has two signal types as examples a square wave generator and a sine wave generator.  
#You can (indeed you should) create your own Signal class and override the get_signal_value method - 
#which must return a vaue between 0 and 1.0 if it is to be displayed within the bounds of the ScrollGraph view.  
#Bear in mind the get_signal_value method gets called with each update of the ScrollGraph scene i.e. 60 times a second. 

class Signal:
	time_on_screen = 0
	time_since_last_update = 0
	time_in_cycle = 0
	hi_time = 1.0
	lo_time = 2.0
	hi_value = 0.8
	lo_value = 0.2
	is_hi = True
	signal_type = 'not set yet'
	
	def get_signal_value(self):
		if self.signal_type == 'sine':
			return (self.sine_wave_generator())
		elif self.signal_type == 'square':
			return (self.square_wave_generator())
		else:
			return random.uniform(-1,1)
		
	def square_wave_generator(self):
		self.time_in_cycle += self.time_since_last_update
		if self.is_hi:
			if self.time_in_cycle > self.hi_time:
				self.is_hi = False
				self.time_in_cycle = 0
				return self.lo_value
			else:
				return self.hi_value
		else:
			if self.time_in_cycle > self.lo_time:
				self.is_hi = True
				self.time_in_cycle = 0
				return self.hi_value
			else:
				return self.lo_value
			
	def sine_wave_generator(self):
		return(((math.sin(self.time_on_screen)+1)/2))
		
	def set_hi_time(self,time):
		self.hi_time = time
		
	def set_lo_time(self,time):
		self.lo_time = time
		
	def set_hi_value(self,value):
		self.hi_value = value
		
	def set_lo_value(self,value):
		self.lo_value = value
		
	def set_signal_type(self,wave):
		self.signal_type = wave
		
# Class ScrollGraph is the main constructor class 
#an animated scene which is passed to a ui.Scene to be displayed as a custom ui component.  
#Each plot value creates a SpriteNode in the form of a vertical line to the height of the plot value (in fact a narrow rectangle) 
#which is placed at one end of the ScrollGraph Scene - this is animated horizontally.  
#A new plot line is added with each refresh of the scene (60fps).  
#Attributes that can be set are: speed (i.e the time it takes for a plot line to transit the screen), direction (left to right or right to left), 
#Colour (background and plot), axis position etc.

class ScrollGraph (Scene):
	
	timeOnScreen = 10							#Horizontal transit time in seconds i.e. speed
	hasNegativeYValues = False		#Does the plot value go below the base line?
	yOffSet = 0										#Height position of the X-Axis
	title = 'Untitled'						#The title of the particular scroll graph
	isRightToLeft = True					#Horizontal direction of the scrolling
	plotColor = 'red'							#Default plot Colour
	popup = ui.View()							#The popover view called when the menu button is tapped

		
	def setup(self):
		self.x,self.y,self.width, self.height = self.bounds		#Gets the size of the view (as set at instantiation)
		self.set_plotValue(50)																#initialise plot value
		label = Label(parent=self)														#intatiate a Label Node
		label.text = (self.title)															#give it the value passed at instantiation
		lx,ly = label.size																		#get the label size so we can position it
		label.position = (self.width/2,self.height-ly/2)			#put it in the middle at the top of the view
		label.z_position = (1.0)															#put it in front of everything else
		self.add_child(label)																	#place the label into the UI
		button = Button(parent=self)													#instantiate a button Node
		button.position = (self.width-10,self.height-10)			#put it in the top right corner
		button.z_position = (1.0)															#make sure it can always be seen
		self.add_child(button)																#place the button into the UI
		if self.hasNegativeYValues :													#find out if our graph drops below baseline
			self.yOffSet=self.height/2													#If it does put the x-Axis in the middle
		self.draw_axis_node()																	#call the method that draws the axis

	def action_button_pressed(self,sender):						#This is the method that handles the buttons
		if sender.title == 'Black':														#in the popover
			self.set_backgroundColor('black')
		elif sender.title == 'Blue':
			self.set_backgroundColor('midnightblue')
		elif sender.title == 'Grey':
			self.set_backgroundColor('darkgray')
		elif sender.title == 'Red':
			self.set_plotColor('red')
		elif sender.title == 'Green':
			self.set_plotColor('lightgreen')
		elif sender.title == 'Yellow':
			self.set_plotColor('yellow')
		elif sender.title == 'Fast':
			self.set_timeOnScreen(5)
			self.axis.remove_from_parent()
			self.setup()
		elif sender.title == 'Medium':
			self.set_timeOnScreen(10)
			self.axis.remove_from_parent()
			self.setup()
		elif sender.title == 'Slow':
			self.set_timeOnScreen(20)
			self.axis.remove_from_parent()
			self.setup()
		elif sender.title == 'Left to Right':
			self.isRightToLeft = False
		elif sender.title == 'Right to Left':
			self.isRightToLeft = True
		elif sender.title == 'Bottom X Axis':
			self.axis.remove_from_parent()
			self.hasNegativeYValues = False
			self.yOffSet = 0
			self.setup()
		elif sender.title == 'Middle X Axis':
			self.axis.remove_from_parent()
			self.hasNegativeYValues = True
			self.yOffSet = self.height/2
			self.setup()
		elif sender.title == 'Exit':
			self.popup.close()
						
	def touch_began(self, touch):														#This method detects a touch of the 'menu' button
		x, y = touch.location
		if x>(self.width-30) and y>(self.height-30):
			self.call_popup()
		
	def touch_moved(self, touch):														#If you touch the graph and move your finger
		x, y = touch.location																	#the plot will follow your finger
		self.plotValue = y
		
	def touch_ended(self, touch):
		pass

	def call_popup(self):																		#This method instantiates the popover window
		self.popup = ui.load_view('ScrollGraphPopUp')					#which has been created in the UI designer
		self.popup.name = (self.title+" Graph Attributes")
		self.popup.present('Sheet')
	
	def set_scrollDirection(self, direction):								#Method to change the direction of scrolling
		self.isRightToLeft = direction

	def set_timeOnScreen(self,speed):												#Method to change speed
		self.timeOnScreen = speed
		
	def set_backgroundColor(self,color):										#Method to change background colour
		self.background_color = color
		
	def set_plotColor(self,color):													#Method to change plot colour
		self.plotColor = color
		
	def set_plotValue(self,value):													#Method to change the plot value
		self.signal.time_since_last_update = self.dt
		self.signal.time_on_screen = self.t
		self.signal.set_signal_type(self.signal_type)
		if self.hasNegativeYValues:
			self.plotValue = self.signal.get_signal_value()*(self.height/2) + (self.height/2)
		else:
			self.plotValue = self.signal.get_signal_value()*self.height
		
	def set_signal_type(self,signal,signal_type):
		self.signal = signal
		self.signal_type = signal_type
		self.signal.set_signal_type(signal_type)
				
	def get_time(self):
		return (self.t,self.dt)
		
	def draw_axis_node(self):																#Intiatiates an axis Node
		self.axis = Axis(self.width, self.height,self.timeOnScreen,self.yOffSet)
		self.axis.anchor_point = (0,0)												#positions it
		self.axis.position = (0,0)
		self.axis.z_position = (1.0)													#makes sure it can always be seen
		self.add_child(self.axis)															#adds it to the view

#The update method is the meat of the class - this gets called 60 times a second.  
#This finds out which direction we are scrolling as that determies which end to draw the plot line.  
#It then finds out if we are plotting positive values only in which case baseline is bottom of the view or 
#if we are plotting positive and negative values in which case middle of the view.
							
	def update(self):
		self.set_plotValue(self.t)
		if self.isRightToLeft:
			if self.plotValue - self.yOffSet >= 0:
				line = ui.Path.rect(self.width,self.yOffSet,4,self.plotValue-self.yOffSet) 	#The plot line path
				plotLine = PlotLine(parent=self)																					#Instantiate a ShapeNode
				plotLine.path = line																											#give it the path
				plotLine.anchor_point = (0,0)																							#don't use centre for pos
				plotLine.fill_color=self.plotColor																				#draw it and fill it
				plotLine.stroke_colour=self.plotColor
				plotLine.position=(self.width,self.yOffSet)																#position it
			else:
				line = ui.Path.rect(self.width,self.plotValue,4,self.yOffSet-self.plotValue)		
				plotLine = PlotLine(parent=self)
				plotLine.path = line
				plotLine.anchor_point = (0,0)
				plotLine.fill_color = self.plotColor
				plotLine.stroke_colour = self.plotColor
				plotLine.position=(self.width,self.plotValue)
			actions = [Action.move_by(-self.width,0,self.timeOnScreen),Action.remove()]	#put it in the scene
			plotLine.run_action(Action.sequence(actions))																#and animate it
		else:
			if self.plotValue - self.yOffSet >= 0:
				line = ui.Path.rect(0,self.yOffSet,4,self.plotValue-self.yOffSet)
				plotLine = PlotLine(parent=self)
				plotLine.path = line
				plotLine.anchor_point = (0,0)
				plotLine.fill_color=self.plotColor
				plotLine.stroke_colour=self.plotColor
				plotLine.position=(0,self.yOffSet)
			else:
				line = ui.Path.rect(0,self.plotValue,4,self.yOffSet-self.plotValue)		
				plotLine = PlotLine(parent=self)
				plotLine.path = line
				plotLine.anchor_point = (0,0)
				plotLine.fill_color = self.plotColor
				plotLine.stroke_colour= self.plotColor
				plotLine.position=(0,self.plotValue)
			actions = [Action.move_by(self.width,0,self.timeOnScreen),Action.remove()]
			plotLine.run_action(Action.sequence(actions))		

#From here on is just to demo the scroll graph.  
#v is a simple sheet view to which I have added three instances of scoll graph with three signal types.  
#You can of course send any value (signal) you like to set_plotValue  
#If you don't want touches to interfere with the plot then remove lines 120 & 121 in method 'touch_moved' and replace with 'pass'
###### ENJOY! ##### 

def __main__():
	
	v = ui.View(background_colour = 'lightgray')
	v.background_color='lightgray'
	s = Signal()
		
	sv=SceneView(frame=(5,20,500,200))
	sv.scene=ScrollGraph()
	sv.scene.set_signal_type(s,'sine')
	sv.scene.background_color = 'black'
	sv.scene.title='Sine'
	sv.scene.isRightToLeft = False
	v.add_subview(sv)
			
	sv2=SceneView(frame=(5,230,500,200))
	sv2.scene=ScrollGraph()
	sv2.scene.set_signal_type(s,'square')
	sv2.scene.set_plotColor('yellow')
	sv2.scene.background_color = 'midnightblue'
	sv2.scene.title='Square'
	sv2.scene.set_timeOnScreen(5)
	v.add_subview(sv2)
			
	sv3=SceneView(frame=(5,440,500,200))
	sv3.scene=ScrollGraph()
	sv3.scene.set_signal_type(s,'random')
	sv3.scene.hasNegativeYValues = True
	sv3.scene.background_color = 'darkgray'
	sv3.scene.set_plotColor ('lightgreen')
	sv3.scene.title='Random'
	v.add_subview(sv3)
			
	v.present()

__main__()
