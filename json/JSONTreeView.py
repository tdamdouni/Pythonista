# coding: utf-8

import json
import sys
PY3 = sys.version_info[0] >= 3
if PY3:
	basestring = str
def iteritems(d):
	if PY3:
		return d.items()
	else:
		return d.iteritems()
		
class JSONTreeNode (TreeNode):
	def __init__(self, json_path=None, node=None, key=None, level=0):
		TreeNode.__init__(self)
		if json_path is not None:
			with open(json_path, 'rb') as f:
				root_node = json.load(f)
				self.node = root_node
		else:
			self.node = node
		if isinstance(self.node, list):
			self.title = 'list (%i)' % (len(self.node),)
			self.leaf = False
			self.icon_name = 'iob:navicon_32'
		elif isinstance(self.node, dict):
			self.title = 'dict (%i)' % (len(self.node),)
			self.leaf = False
			self.icon_name = 'iob:ios7_folder_outline_32'
		elif isinstance(self.node, basestring):
			self.title = '"%s"' % (self.node,)
			self.leaf = True
			self.icon_name = 'iob:ios7_information_outline_32'
		else:
			self.title = str(self.node)
			self.leaf = True
			self.icon_name = 'iob:ios7_information_outline_32'
		self.level = level
		if key is not None:
			self.title = key + ' = ' + self.title
		elif json_path is not None:
			self.title = os.path.split(json_path)[1]
			
	def expand_children(self):
		if self.children is not None:
			self.expanded = True
			return
		if isinstance(self.node, list):
			self.children = [JSONTreeNode(node=n, level=self.level+1) for n in self.node]
		elif isinstance(self.node, dict):
			self.children = [JSONTreeNode(node=v, key=k, level=self.level+1) for k, v in iteritems(self.node)]
		self.expanded = True
		
# --------------------
#root_node = JSONTreeNode(os.path.expanduser('~/Documents/Examples/User Interface/Calculator.pyui'))
#tree_controller = TreeDialogController(root_node)
#tree_controller.view.present('sheet')
#tree_controller.view.wait_modal()
#--------------------

