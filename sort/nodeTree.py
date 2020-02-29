from __future__ import print_function
# https://gist.github.com/jefflovejapan/7607589

#import pudb


class BinaryTree(object):
	"""docstring for BinaryTree"""
	def __init__(self, arg):
		self.key = arg
		self.leftChild = None
		self.rightChild = None
		
	def insertLeft(self, node):
		if not self.leftChild:
			self.leftChild = BinaryTree(node)
		else:
			tmp = BinaryTree(node)
			tmp.leftChild = self.leftChild
			self.leftChild = tmp
		return self.leftChild
		
	def insertRight(self, node):
		if not self.rightChild:
			self.rightChild = BinaryTree(node)
		else:
			tmp = BinaryTree(node)
			tmp.rightChild = self.rightChild
			self.rightChild = tmp
		return self.rightChild
		
	def getRootVal(self):
		return self.key
		
	def setRootVal(self, newval):
		self.key = newval
		
operators = ['+', '-', '*', '/']


def parse_expr_to_tree(expr, tree=None, parent=None):
	expr_list = list(expr)
	expr_list = [x for x in expr_list if not x.isspace()]
	
	if len(expr) == 0:
		return tree
		
	if not tree:
		tree = BinaryTree('')
		
	if expr[0] == '(':
		print('creating left')
		new_tree = BinaryTree('')
		tree.insertLeft(parse_expr_to_tree(expr[1:], new_tree, tree))
		
	elif expr[0] == ')':
		print('found )')
		return parent
	elif expr[0] in operators:
		print('found operator')
		tree.setRootVal(expr[0])
		new_tree = BinaryTree('')
		tree.insertRight(parse_expr_to_tree(expr[1:], new_tree, tree))
		
	else:
		print('found number')
		# ch is number
		tree.setRootVal(expr[0])
		return parent
		
# pudb.set_trace()
t = parse_expr_to_tree('(3 + 2)')

print(t.leftChild.key)

