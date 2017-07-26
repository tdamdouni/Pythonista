# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2835/pythonista-games-patterned-after-godot

# @TutorialDoctor

# P.S. I would like it if nodes could have names, so I might have to write my own class. Also, I would need a function to traverse the node tree. I love the get_node() function of Godot, but I would like to get any node no matter how deep it is in the hierarchy.
# I don't really know anything about Godot, but you can easily assign names to nodes. some_node.name = 'foo' will work in Python, even though name is not a standard attribute of the Node class.

# Writing a helper function to find nodes in a tree is also pretty easy. Here's a little example:

from __future__ import print_function
from scene import Scene, SpriteNode, run

# A simple scene that contains a background,
# which contains a player, which contains a key...
# Just to have a nested node hierarchy for testing.

class MyScene (Scene):
	def __init__(self):
		a = SpriteNode('plf:BG_Colored_grass', parent=self)
		a.name = 'background'
		b = SpriteNode('plf:AlienBeige_swim2', parent=a)
		b.name = 'player'
		c = SpriteNode('plf:HudKey_yellow', parent=b)
		c.name = 'key'
		
def find_node(root, name):
	if hasattr(root, 'name') and root.name == name:
		return root
	for child in root.children:
		n = find_node(child, name)
		if n:
			return n
			
# Some tests for the find_node function:
s = MyScene()
print('Player:', find_node(s, 'player'))
print('Background:', find_node(s, 'background'))
print('Key:', find_node(s, 'key'))
print('Non-existing node:', find_node(s, 'foobar'))

