# https://forum.omz-software.com/topic/3381/re-share-ui-view-walker/2

# from @JonB

import ui
from collections import deque

class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._breadth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def __next__(self):
		'''required for iterator objects.  raise stopiteration once the queue is empty.  '''
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
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		# just add some btns to the view as a test
		for i in range(1, 11):
			btn = ui.Button(name = 'btn{}'.format(i))
			self.add_subview(btn)
			lb = ui.Label(name = 'lbl{}'.format(i))
			btn.add_subview(lb)
			
			
mc = MyClass(name = 'CustomView')
print('depthfirst:', [s.name for s in ViewWalker(mc)])
print('\n')
print ('breadthfirst:', [s.name for s in ViewWalker(mc,True )])
# --------------------
# from @JonB

import ui
from collections import deque

class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._breadth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def __next__(self):
		'''required for iterator objects.  raise stopiteration once the queue is empty.  '''
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
		
	def sub_view_objects(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s for s in self]
		
	def sub_view_names(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s.name for s in self]
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		# just add some btns to the view as a test
		for i in range(1, 11):
			btn = ui.Button(name = 'btn{}'.format(i))
			self.add_subview(btn)
			lb = ui.Label(name = 'lbl{}'.format(i))
			btn.add_subview(lb)
			
			
mc = MyClass(name = 'CustomView')
print('breadthfirst', ViewWalker(mc, True).sub_view_objects())
print('\n')
print('depthfirst', ViewWalker(mc).sub_view_objects())
print('\n')
print('breadthfirst', ViewWalker(mc, True).sub_view_names())
print('\n')
print('depthfirst', ViewWalker(mc).sub_view_names())
print('\n')
print('breadthfirst', [s.name for s in ViewWalker(mc, True)])
print('\n')
for v in ViewWalker(mc, False):
	print(v)
# --------------------
# from @JonB

import ui
from collections import deque

class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._breadth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def __next__(self):
		'''required for iterator objects.  raise stopiteration once the queue is empty.  '''
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
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		# just add some btns to the view as a test
		for i in range(1, 11):
			btn = ui.Button(name = 'btn{}'.format(i))
			self.add_subview(btn)
			lb = ui.Label(name = 'lbl{}'.format(i))
			btn.add_subview(lb)
			
			
mc = MyClass(name = 'CustomView')
print('depthfirst:', [s.name for s in ViewWalker(mc)])
print('\n')
print ('breadthfirst:', [s.name for s in ViewWalker(mc,True )])
# --------------------
# from @JonB

import ui
from collections import deque

class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._breadth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def __next__(self):
		'''required for iterator objects.  raise stopiteration once the queue is empty.  '''
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
		
	def sub_view_objects(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s for s in self]
		
	def sub_view_names(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s.name for s in self]
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		# just add some btns to the view as a test
		for i in range(1, 11):
			btn = ui.Button(name = 'btn{}'.format(i))
			self.add_subview(btn)
			lb = ui.Label(name = 'lbl{}'.format(i))
			btn.add_subview(lb)
			
			
mc = MyClass(name = 'CustomView')
print('breadthfirst', ViewWalker(mc, True).sub_view_objects())
print('\n')
print('depthfirst', ViewWalker(mc).sub_view_objects())
print('\n')
print('breadthfirst', ViewWalker(mc, True).sub_view_names())
print('\n')
print('depthfirst', ViewWalker(mc).sub_view_names())
print('\n')
print('breadthfirst', [s.name for s in ViewWalker(mc, True)])
print('\n')
for v in ViewWalker(mc, False):
	print(v)
# --------------------
def sub_views_mapping(self, breadthfirst = False):
	self._breadth=breadthfirst
	return {s.name : s for s in self}
# --------------------
# from @JonB

import ui
from collections import deque, namedtuple

class ViewWalker(object):
	'''simple iterator for ui.View objects, capable of depth or breadth first traversal'''
	def __init__(self,v,breadthfirst=False):
		self._dq=deque([v])
		self._breadth=breadthfirst
		
	def __iter__(self):
		'''required for iterator objects'''
		return self
		
	def __next__(self):
		'''required for iterator objects.  raise stopiteration once the queue is empty.  '''
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
		
	def sub_view_objects(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s for s in self]
		
	def sub_view_names(self, breadthfirst = False):
		self._breadth=breadthfirst
		return [s.name for s in self]
		
	def as_dict(self, breadthfirst = False):
		# returns a dict
		self._breadth=breadthfirst
		return {s.name : s for s in self}
		
	def as_namedtuple(self, breadthfirst = False):
		# returns a namedtuple
		self._breadth=breadthfirst
		d = self.as_dict(breadthfirst)
		return namedtuple('ViewObjects', d.keys())(**d)
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.make_view()
		
	def make_view(self):
		# just add some btns to the view as a test
		for i in range(1, 11):
			btn = ui.Button(name = 'btn{}'.format(i))
			self.add_subview(btn)
			lb = ui.Label(name = 'lbl{}'.format(i))
			btn.add_subview(lb)
			
			
mc = MyClass(name = 'CustomView')
for sv in ViewWalker(mc, False):
	print(sv)
	
# get a dict, string subscripts :(
d = ViewWalker(mc).as_dict()
print(d['btn1'].name)
print(d['btn1'])

# get a nampledtuple, now can use field names
vo = ViewWalker(mc).as_namedtuple()
print(vo.btn1.name)
print(vo.btn1)
# --------------------
dis# --------------------
timeit# --------------------
apply_kwargs()# --------------------
dis.dis()# --------------------
timeit.timeit()# --------------------
import dis, timeit

def apply_kwargs_0(obj, **kwargs):
	for k, v in kwargs.items():
		if hasattr(obj, k):
			setattr(obj, k, v)
			
print(dis.dis(apply_kwargs_0))

print('=====')

def apply_kwargs_1(obj, **kwargs):
	for key in set(vars(obj)) & set(kwargs):
		setattr(obj, key, kwargs[key])
		
print(dis.dis(apply_kwargs_1))

class MyClass(object):
	def __init__(self, a=0, b=1, c=2):
		self.a = a
		self.b = b
		self.c = c
		
obj = MyClass()
print(vars(obj))  # {'c': 2, 'b': 1, 'a': 0}
apply_kwargs_0(obj, b=7, c=8, d=9)
print(vars(obj))  # {'c': 8, 'b': 7, 'a': 0}

obj = MyClass()
print(vars(obj))  # {'c': 2, 'b': 1, 'a': 0}
apply_kwargs_1(obj, b=7, c=8, d=9)
print(vars(obj))  # {'c': 8, 'b': 7, 'a': 0}

print(timeit.timeit('apply_kwargs_0(obj, b=7, c=8, d=9)',
                    globals=globals(), setup='obj = MyClass()'))

print(timeit.timeit('apply_kwargs_1(obj, b=7, c=8, d=9)',
                    globals=globals(), setup='obj = MyClass()'))

# --------------------

