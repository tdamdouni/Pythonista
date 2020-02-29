from __future__ import print_function


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
		
		
def parse_expr_to_tree(expr):
	stack = []
	operators = ['+', '-', '*', '/']
	expr_list = list(expr)
	expr_list = [x for x in expr_list if not x.isspace()]
	tree = BinaryTree('')
	current_node = tree
	stack.append(current_node)
	for char in expr_list:
		if char == '(':
			stack.append(current_node)
			current_node = current_node.insertLeft('')
			
		elif char.isdigit():
			current_node.setRootVal(char)
			current_node = stack.pop()
			
		elif char in operators:
			current_node.setRootVal(char)
			stack.append(current_node)
			current_node = current_node.insertRight('')
			
		elif char is ')':
			current_node = stack.pop()
			
	else:
		assert tree
		return tree
		
		
def eval_tree(tree):
	operator_map = {
	'+': '__add__',
	'-': '__sub__',
	'/': '__div__',
	'*': '__mul__'
	}
	
	operator = tree.getRootVal()
	left_op = tree.leftChild.getRootVal()
	right_op = tree.rightChild.getRootVal()
	
	if type(left_op) is int or left_op.isdigit():
		left_int = int(left_op)
	elif left_op in operator_map.keys():
		left_int = eval_tree(tree.leftChild)
		
	if type(right_op) is int or right_op.isdigit():
		right_int = int(right_op)
	elif right_op in operator_map.keys():
		right_int = eval_tree(tree.rightChild)
		
	total = getattr(left_int, operator_map[operator])(right_int)
	return total
	
print(eval_tree(parse_expr_to_tree('(3 + (4 * 5))')))

