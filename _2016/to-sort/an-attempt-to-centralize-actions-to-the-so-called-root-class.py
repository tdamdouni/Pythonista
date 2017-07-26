# https://forum.omz-software.com/topic/3412/share-an-attempt-to-centralize-actions-to-the-so-called-root-class

import ui

def get_root(v):
	# get the root view of the view
	sv = v
	while sv.superview:
		sv= sv.superview
		
	return sv
	
class ViewBase(ui.View):
	def __init__(self, w, h, *args, **kwargs):
		super().__init__( *args, **kwargs)
		
		self.w = w
		self.h = h
		
		self.cc = ui.View(frame = self.bounds)
		self.cc.flex = 'wh'
		self.add_subview(self.cc)
		
	def layout(self):
		if not self.superview:
			return
			
		sv = self.superview
		
		if self.w <= 1:
			self.width = sv.bounds.width * self.w
		else:
			self.width = self.w
			
		if self.h <= 1:
			self.height = sv.bounds.height * self.h
		else:
			self.height = self.h
			
		if hasattr(self, 'Userlayout'):
			self.Userlayout()
			
	# an attempt to rationalise action flow. well in this case, directing
	# all actions to single method in the root class , if the root class
	# has exposed the method.
	def dispatch_action(self, sender):
		root = get_root(sender)
		if hasattr(root, 'actions'):
			root.actions(sender)
			
class SearchView(ViewBase):
	def __init__(self, w=1, h=1 , *args, **kwargs):
		super().__init__(w, h, *args, **kwargs)
		self.fld_search = None
		
		self.make_view()
		
	def make_view(self):
		self.bg_color = 'darkgray'
		r = ui.Rect(*self.bounds).inset(6, 8)
		sf = ui.TextField(frame = r, name = 'SearchTextField')
		# here, a test to attempt to pass actions through to the root view
		sf.action = self.dispatch_action
		sf.placeholder = 'Search'
		sf.flex = 'wh'
		
		self.fld_search = sf
		self.add_subview(sf)
		
	def Userlayout(self):
		# we want to base class to do some inital work in Layout.
		#if this method exists in the child class its called.
		pass
		
class NavigationView(ViewBase):
	def __init__(self, w=1, h=1, *args, **kwargs):
		super().__init__( w, h,  *args, **kwargs)
		self.bg_color = 'lightyellow'
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	# attempt to centralise action handling without explicitly setting
	# the action chain.  this method needs to of course examine each
	# sender to take the appropriate action.
	def actions(self, sender):
		print('sender' , sender, sender.name)
		if isinstance(sender, ui.TextField):
			print(sender.text)
			
if __name__ == '__main__':
	w, h = 600, 800
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white')
	nv = NavigationView(w = 1, h = 44)
	sv = SearchView(.5, 1)
	nv.add_subview(sv)
	mc.add_subview(nv)
	mc.present('sheet')
# --------------------

