'''This view will compute the shortest path and then display it in a pretty format'''
import ui
import photos

import sys; sys.path.append('..')

from pathfinding import imageInput, dijkstra

class SolutionView(ui.View):
	def __init__(self, image, start, goal):
		self.image = image.convert('RGB')
		self.load = self.image.load()
		self.start=start
		self.goal=goal
		
		sx, sy=start
		gx, gy=goal
		self.load[sx,sy]=(0,255,0)
		self.load[gx,gy]=(255,0,0)
	def pathCalc(self):
		#Create graph from image
		graph = imageInput.GraphFromImage(self.image)
		#Locate nodes in graph that correspond to start and finish
		for node in graph:
			if node.id == self.start:
				startNode = node
			if node.id == self.goal:
				goalNode = node
		#Calculate path	
		return [x.id for x in dijkstra.Dijkstra(graph, startNode, goalNode)]
	
	def Djk2UI(self, path):
		'''Convert a path of (x,y) coordinates to a pretty ui path'''
		
		buttonsize=self.buttonsize
		#Center offset, used so that path is centered on tiles
		cenoff=0.5*buttonsize
		#Convert path to coordinates of the bigger window
		path = [(cenoff+self.startx+x*buttonsize,cenoff+y*buttonsize) for x,y in path]
		
		p=ui.Path()
		p.move_to(*path[0])
		for point in path:
			p.line_to(*point)
		p.line_join_style=ui.LINE_JOIN_ROUND
		p.line_cap_style=ui.LINE_CAP_ROUND
		p.line_width=buttonsize/4
		return p
		
	def draw(self):
		self.buttonsize = int(self.height/16)
		self.startx=int((self.width/2-self.height/2))
		
		buttonsize=self.buttonsize
		for x in range(16):
			for y in range(16):
				frame=(self.startx+x*buttonsize,y*buttonsize,buttonsize,buttonsize)
				p=ui.Path.rect(*frame)
				ui.set_color(self.load[x,y])
				p.fill()
		
		path=self.Djk2UI(self.pathCalc())
		
		ui.set_color((0,0,1))
		ui.set_shadow((0,0,0),2,2,5)
		path.stroke()
		
		
if __name__ == '__main__':	
	SolutionView(photos.pick_image(), (1,0), (12,14)).present(hide_title_bar=1)