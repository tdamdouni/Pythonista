'''Functions for generating and solving graph structures from images'''
from __future__ import print_function
from PIL import Image
from dijkstra import *

def find(color, im):
	'''Find all instances of a certain color in an image'''
	load = im.load()
	locations = []
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			if load[x, y] == color:
				locations.append( (x, y) )
	return locations

def markPath(path, image):
	'''Draw in blue the provided path onto the provided image'''
	i = image.copy()
	l = i.load()
	path.pop(0)# Remove the start square
	path.pop(-1) # Remove the finish square
	for x, y in path:
		l[x, y] = (0,0,255)
	return i

def GraphFromImage(im):
	'''Create a graph from an image where black pixels are walls,
	and white are paths.'''
	path = find((255,255,255), im)+find((0,255,0), im)+find((255,0,0), im)
	pathNodes = [Node(p) for p in path]
	graph = Graph(pathNodes)
	#Add connections by finding all neighboring pixels and checking if they exist in the image
	for x, y in path:
		neighbors = [(x+1,y), (x-1, y), (x, y+1), (x, y-1)]
		node = pathNodes[path.index((x,y))]
		for n in neighbors:
			if n in path:
				node2 = pathNodes[path.index(n)]
				graph.add_connection(node, node2)
	return graph

def PathFromImage(im):
	graph = GraphFromImage(im)
	startpos = find((0,255,0),im)[0]
	for node in graph:
		if node.id == startpos:
			startNode = node
			break
	goalpos = find((255,0,0),im)[0]
	for node in graph:
		if node.id == goalpos:
			goalNode = node
			break
	return [x.id for x in Dijkstra(graph, startNode, goalNode)]


	
if __name__ == '__main__':
	import time, ImagePlus
	for name in ['maze1.png','maze2.png','maze3.png']:
		i = Image.open('../Test Images/'+name)
		
		t1 = time.time()
		path=PathFromImage(i)
		resultstr='Solved maze: \''+name+'\' in',time.time()-t1,'seconds.'
		
		ImagePlus.sidebyside((i.resize((256,256)), markPath(path, i).resize((256,256)))).show()
		print(resultstr)