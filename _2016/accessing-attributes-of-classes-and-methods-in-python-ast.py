# To count the attributes in a Class and Method

# https://forum.omz-software.com/topic/3866/accessing-attributes-of-classes-and-methods-in-python-ast/2

import ast


class ClassAttributes(object):
	def __init__(self, node):
		self.node = node
		self.loc_in_module = 0
		self.loc_in_class = 0
		
	def get_attribute_names(self):
		for cls in self.node.body:
		
			if isinstance(cls, ast.ClassDef):
				self.loc_in_class += 1
				print('Class {}'.format(self.loc_in_class))
				
				self.loc_in_method = 0
				if isinstance(cls, ast.Attribute) or isinstance(cls, ast.Assign):
				
					for target in target.targets:
						print('{} Atrribute: {}'.format(str(cls.lineno), target))
						
				for node in ast.walk(cls):
					if isinstance(node, ast.FunctionDef):
						self.loc_in_method += 1
						print('Method {}'.format(self.loc_in_method))
						if isinstance(node, ast.Attribute) or isinstance(node, ast.Assign):
						#if isinstance(node, (ast.Attribute, ast.Assign)):
	#pass
							for target in target.targets:
								print('{} Atrribute: {}'.format(str(node.lineno), target))
								
								
if __name__ == '__main__':
	filename = 'test.py'
	
	with open(filename, 'r') as pyfile:
		data = pyfile.read()
		pyfile.close()
		tree = ast.parse(data)
		
		
	v = ClassAttributes(tree)
	v.get_class_attribute_names()
