# coding: utf-8

# https://forum.omz-software.com/topic/1787/recursively-getting-all-objects-from-all-subviews/12

def all_sub_views(v):
	for view in v.subviews:
		print view, view.name
		for item in view.subviews:
			if type(item)==ui.View:
				print 'called this'
				all_sub_views(item)
			else:
				pass
	print 'exiting...'
	
	
--------------------

# coding: utf-8

import ui
my_objects =[]

def treat_button(btn):
	btn.border_width = 1
	btn.background_color = 'gray'
	btn.tint_color = 'white'
	
def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		for item in view.subviews:
			if type(item)==ui.View:
				all_sub_views(item)
			else:
				pass
				
if __name__ =='__main__':
	v = ui.load_view()
	all_sub_views(v)
	for item in my_objects:
		if type(item)== ui.Button:
			treat_button(item)
	v.present('sheet')
	
--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		try:
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
				else:
					pass
		except:
			#this is an error, but a work around'
			pass
			
--------------------
>>> import ui
>>> s=ui.SegmentedControl()
>>> s.subviews
Traceback (most recent call last):
	File "<string>", line 1, in <module>
SystemError: /Users/ole/Development/xcode/Pythonista/python/Objects/tupleobject.c:54: bad argument to internal function
--------------------
add_subview--------------------
subviews--------------------
hasattr--------------------
# coding: utf-8
import ui
from collections import deque
def depthfirst(v):
	'''recursivdly walk tree'''
	if hasattr(v,'subviews'):
		for sv in v.subviews:
			yield sv
			for n in depthfirst(sv):
				yield n
				
--------------------
StopException--------------------
class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._bredth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def next(self):
	"""required for iterator objects.  raise stopiteration once the queue is empty.  """
		if not self._dq:
			raise StopIteration
		#pop next view...
		if self._breadth:
			v=self._dq.popleft()# oldest entry (FIFO)
		else:
			v=self._dq.pop() # newest entry (stack)
		#then push its subviews
		if hasattr(v,'subviews'):
			self._dq.extend(v.subviews)
		return v
		
v=ui.load_view('test')
print 'depthfirst:', [s.name for s in ViewWalker(v)]
print 'breadthfirst:', [s.name for s in ViewWalker(v,True )]

--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		if hasattr(view, 'subviews'):
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
--------------------
isinstance(x, y)--------------------
type(x) == y--------------------
import ui
class MyView(ui.View):               # MyView is a subclass of ui.View
	pass
my_view = MyView()
print(type(my_view) == ui.View)      # prints False because MyView != ui.View
print(isinstance(my_view, ui.View))  # prints True  because MyView is a ui.View
--------------------
my_objects--------------------
list--------------------
my_objects=list(depthfirst(v))
--------------------

def all_sub_views(v):
	for view in v.subviews:
		print view, view.name
		for item in view.subviews:
			if type(item)==ui.View:
				print 'called this'
				all_sub_views(item)
			else:
				pass
	print 'exiting...'
	
	
--------------------

# coding: utf-8

import ui
my_objects =[]

def treat_button(btn):
	btn.border_width = 1
	btn.background_color = 'gray'
	btn.tint_color = 'white'
	
def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		for item in view.subviews:
			if type(item)==ui.View:
				all_sub_views(item)
			else:
				pass
				
if __name__ =='__main__':
	v = ui.load_view()
	all_sub_views(v)
	for item in my_objects:
		if type(item)== ui.Button:
			treat_button(item)
	v.present('sheet')
	
--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		try:
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
				else:
					pass
		except:
			#this is an error, but a work around'
			pass
			
--------------------
>>> import ui
>>> s=ui.SegmentedControl()
>>> s.subviews
Traceback (most recent call last):
	File "<string>", line 1, in <module>
SystemError: /Users/ole/Development/xcode/Pythonista/python/Objects/tupleobject.c:54: bad argument to internal function
--------------------
# coding: utf-8
import ui
from collections import deque
def depthfirst(v):
	'''recursivdly walk tree'''
	if hasattr(v,'subviews'):
		for sv in v.subviews:
			yield sv
			for n in depthfirst(sv):
				yield n
				
--------------------
class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._bredth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def next(self):
	"""required for iterator objects.  raise stopiteration once the queue is empty.  """
		if not self._dq:
			raise StopIteration
		#pop next view...
		if self._breadth:
			v=self._dq.popleft()# oldest entry (FIFO)
		else:
			v=self._dq.pop() # newest entry (stack)
		#then push its subviews
		if hasattr(v,'subviews'):
			self._dq.extend(v.subviews)
		return v
		
v=ui.load_view('test')
print 'depthfirst:', [s.name for s in ViewWalker(v)]
print 'breadthfirst:', [s.name for s in ViewWalker(v,True )]
--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		if hasattr(view, 'subviews'):
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
--------------------
import ui
class MyView(ui.View):               # MyView is a subclass of ui.View
	pass
my_view = MyView()
print(type(my_view) == ui.View)      # prints False because MyView != ui.View
print(isinstance(my_view, ui.View))  # prints True  because MyView is a ui.View
--------------------

def all_sub_views(v):
	for view in v.subviews:
		print view, view.name
		for item in view.subviews:
			if type(item)==ui.View:
				print 'called this'
				all_sub_views(item)
			else:
				pass
	print 'exiting...'
	
	
--------------------

# coding: utf-8

import ui
my_objects =[]

def treat_button(btn):
	btn.border_width = 1
	btn.background_color = 'gray'
	btn.tint_color = 'white'
	
def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		for item in view.subviews:
			if type(item)==ui.View:
				all_sub_views(item)
			else:
				pass
				
if __name__ =='__main__':
	v = ui.load_view()
	all_sub_views(v)
	for item in my_objects:
		if type(item)== ui.Button:
			treat_button(item)
	v.present('sheet')
	
--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		try:
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
				else:
					pass
		except:
			#this is an error, but a work around'
			pass
			
--------------------
>>> import ui
>>> s=ui.SegmentedControl()
>>> s.subviews
Traceback (most recent call last):
	File "<string>", line 1, in <module>
SystemError: /Users/ole/Development/xcode/Pythonista/python/Objects/tupleobject.c:54: bad argument to internal function
--------------------
add_subview--------------------
subviews--------------------
hasattr--------------------
# coding: utf-8
import ui
from collections import deque
def depthfirst(v):
	'''recursivdly walk tree'''
	if hasattr(v,'subviews'):
		for sv in v.subviews:
			yield sv
			for n in depthfirst(sv):
				yield n
				
--------------------
StopException--------------------
class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._bredth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def next(self):
	"""required for iterator objects.  raise stopiteration once the queue is empty.  """
		if not self._dq:
			raise StopIteration
		#pop next view...
		if self._breadth:
			v=self._dq.popleft()# oldest entry (FIFO)
		else:
			v=self._dq.pop() # newest entry (stack)
		#then push its subviews
		if hasattr(v,'subviews'):
			self._dq.extend(v.subviews)
		return v
		
v=ui.load_view('test')
print 'depthfirst:', [s.name for s in ViewWalker(v)]
print 'breadthfirst:', [s.name for s in ViewWalker(v,True )]
--------------------

def all_sub_views(v):
	for view in v.subviews:
		my_objects.append(view)
		if hasattr(view, 'subviews'):
			for item in view.subviews:
				if type(item)==ui.View:
					all_sub_views(item)
--------------------
isinstance(x, y)--------------------
type(x) == y--------------------
import ui
class MyView(ui.View):               # MyView is a subclass of ui.View
	pass
my_view = MyView()
print(type(my_view) == ui.View)      # prints False because MyView != ui.View
print(isinstance(my_view, ui.View))  # prints True  because MyView is a ui.View
--------------------
my_objects--------------------
list--------------------
my_objects=list(depthfirst(v))
--------------------

