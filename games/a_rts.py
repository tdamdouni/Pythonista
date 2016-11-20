# https://gist.github.com/anonymous/26a01b934ea7e522c497

from scene import *
from random import randint

#A simple function to return the ratio of two integers or floats
def ratios(item1,item2):
	if item1 > item2: 
		return float(item1)/item2 
	return float(item2)/item1

#Hit test function.  Tests a point to see if it's hitting a square.
#Used for controls.  Minimap uses a hittest when you click, for example.
def hit(loc1, loc2, size2):
	if loc1.x>loc2.x and loc1.x<loc2.x+size2.x:
		if loc1.y>loc2.y and loc1.y<loc2.y+size2.y:
			return True

#Draw map draws the grids
def draw_map(grid_size, grid_count, grid_pos):
		stroke_weight(0)
		fill(1,1,1)
		rect(grid_pos.x,grid_pos.y, grid_size*grid_count, grid_size*grid_count)
		stroke_weight(1)
		stroke(0,0,0)
		for lines in range(grid_count+1):
			line(lines*grid_size+grid_pos.x, grid_pos.y, 
			     lines*grid_size+grid_pos.x, grid_pos.y+grid_count*grid_size)
			line(grid_pos.x, lines*grid_size+grid_pos.y, 
			     grid_pos.x+grid_count*grid_size, lines*grid_size+grid_pos.y)
		return
	
	

class MyScene (Scene):
	def setup(self):
		self.grid_count = 30 #Number of columns and rows on the map.
		self.minimap_size = 200./self.grid_count #Size of each node on minimap
		self.minimap_position = Point(self.size.w-220,20)
		self.map_size = 20 #Size of each node on real map
		self.map_position = Point(10,10) #Current viewing position of map
		self.ratio = ratios(200,self.map_size*self.grid_count) #Finds the ratio to translate to minimap
		self.drag = False #Drag and drop
		self.circle_pos = Point(randint(0,self.map_size), randint(0,self.map_size)) #position of circle
		self.circle_vel = Point(randint(-10,10),randint(-10,10)) #velocity of circle
		
	def draw(self):
		background(1, 1, 1)
		draw_map(self.map_size, self.grid_count, self.map_position)
		draw_map(self.minimap_size, self.grid_count, self.minimap_position)
		fill(0,0,1,1)
		
		#Circle for demonstration and testing.  Just bounces around
		ellipse(self.circle_pos.x+self.map_position.x,self.circle_pos.y+self.map_position.y,10,10)
		ellipse(self.circle_pos.x/self.ratio+self.minimap_position.x,
		        self.circle_pos.y/self.ratio+self.minimap_position.y,3,3)
		self.circle_pos.x -= self.circle_vel.x
		self.circle_pos.y -= self.circle_vel.y
		if self.circle_pos.x < 0 or self.circle_pos.x > self.grid_count*self.map_size: 
			self.circle_vel.x = randint(-10,10)
			self.circle_pos.x = 0
		if self.circle_pos.y < 0 or self.circle_pos.y > self.grid_count*self.map_size: 
			self.circle_vel.y = randint(-10,10)
			self.circle_pos.y = 0
		self.circle_vel.y += .1
		self.circle_vel.x += .1
		
		if self.drag: #Drag and drop
			fill(1,1,1,.4)
			rect(self.drag[0].x, self.drag[0].y, self.drag[1].x, self.drag[1].y)
	
	def touch_began(self, touch):
		if not self.drag and not hit(touch.location, self.minimap_position, Point(200,200)):
			self.drag = [touch.location, Point(0,0)]
	
	def touch_moved(self, touch):
		if self.drag:
			self.drag[1] = Point(touch.location.x-self.drag[0].x, touch.location.y-self.drag[0].y)

	def touch_ended(self, touch):
		#When you touch the minimap, the screen moves.
		if self.drag:
			self.drag = False
			return
		if hit(touch.location, self.minimap_position, Point(200,200)):
			tempPoint=Point(self.minimap_position.x-touch.location.x,
			            self.minimap_position.y-touch.location.y)
			self.map_position = Point(tempPoint.x*self.ratio+self.size.w/2, 
			                          tempPoint.y*self.ratio+self.size.h/2)

run(MyScene())
