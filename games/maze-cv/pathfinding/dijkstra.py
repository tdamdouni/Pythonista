from __future__ import print_function
#By Luke Taylor
class Node:
	def __init__(self, name='Node'):
		self.graph = None #parent graph
		self.neighbors = {} #adjacent nodes
		self.distance = float('inf') # distance from node is infinity
		self.prev_node = None
		self.id = name
	def __float__(self):
		return float(self.distance)
	def __str__(self):
		return str(self.id)

class Graph:
	def __init__(self, nodes):
		self.neighbors = dict(zip(nodes, [{} for _ in nodes]))
		
	def __iter__(self):
		return iter(self.neighbors.keys())

	def add_connection(self, a, b, cost=1):
		self.neighbors[a][b] = cost
		self.neighbors[b][a] = cost
		a.neighbors = self.neighbors[a]
		b.neighbors = self.neighbors[b]

def Dijkstra(graph, start, end):
	if start not in graph or end not in graph:
		raise ValueError('Both the start and nodes must be in the provided graph')
	visited = set()
	unvisited = set(graph)
	
	start.distance = 0
	while end.distance == float('inf'): # change to while
		current = min(unvisited, key=lambda x: x.distance)
		unvisited.remove(current)
		visited.add(current)
		adjs = current.neighbors.keys()
		for a in adjs:
			tentativeDistance = current.distance+current.neighbors[a]
			if tentativeDistance < a.distance:
				a.distance = tentativeDistance
				a.prev_node = current
	path = [end]
	#Trace path back to beginning
	while 1:
		current = path[-1]
		if current.prev_node:
			path.append(current.prev_node)
		elif current == start:
			break
	path.reverse()
	return path


if __name__ == '__main__':
	alpha = 'abcdefghijklmnopqrstuvwxyz'
	#3x3 grid
	nodes = [Node(alpha[x]) for x in range(9)]
	graph = Graph(nodes)
	
	graph.add_connection(nodes[0], nodes[1])
	graph.add_connection(nodes[1], nodes[2])
	graph.add_connection(nodes[2], nodes[3])
	graph.add_connection(nodes[3], nodes[4])
	graph.add_connection(nodes[4], nodes[5])
	graph.add_connection(nodes[5], nodes[6])
	graph.add_connection(nodes[6], nodes[7])
	graph.add_connection(nodes[7], nodes[8])
	
	graph.add_connection(nodes[0], nodes[3])
	graph.add_connection(nodes[1], nodes[4])
	graph.add_connection(nodes[2], nodes[5])
	graph.add_connection(nodes[3], nodes[6])
	graph.add_connection(nodes[4], nodes[7])
	graph.add_connection(nodes[5], nodes[8])
	
	graph.add_connection(nodes[0], nodes[4], 1.5)
	graph.add_connection(nodes[1], nodes[3], 1.5)
	graph.add_connection(nodes[1], nodes[5], 1.5)
	graph.add_connection(nodes[2], nodes[4], 1.5)
	graph.add_connection(nodes[3], nodes[7], 1.5)
	graph.add_connection(nodes[4], nodes[6], 1.5)
	graph.add_connection(nodes[4], nodes[8], 1.5)
	graph.add_connection(nodes[5], nodes[7], 1.5)
	
	path = Dijkstra(graph,nodes[0],nodes[8])
	print([str(x) for x in path], 'is the shortest path, with a distance of', end=' ')
	print(path[0].neighbors[path[1]]+path[1].neighbors[path[2]])
	