# https://forum.omz-software.com/topic/3409/share-yet-another-way-to-create-a-std-view

'''
    Pythonista Forum - @Phuket2
'''
import ui, editor

# hide_title_bar
_htb = False

# nothing now. but seems like the base. classes like NavigationBar,
# ToolBar, could inherit functionality fromma class like frame
class Frame(ui.View):
	def __init__(self,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		
class NavigationBar(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.flex = 'w'
		self.height = 44
		if _htb:
			self.height += 36
			
		self.bg_color = 'purple'
		
	def layout(self):
		if self.superview:
			sv = self.superview
			self.width = sv.frame.width
			
class ToolBar(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.flex = 'w'
		self.height = 60
		self.bg_color = 'orange'
		
	def layout(self):
		if self.superview:
			sv = self.superview
			self.width = sv.frame.width
			self.y = sv.frame.height - self.height
			
class ContentView(ui.View):
	def __init__(self, ctl_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.flex = 'wh'
		self.ctl_list = ctl_list
		self.bg_color = 'red'
		self.bring_to_front()
		
	def layout(self):
		if self.superview:
			sv = self.superview
			self.width = sv.bounds.width
			h = sv.bounds.height
			if self.ctl_list[0]:
				self.y = self.ctl_list[0].bounds.max_y
				h-= self.ctl_list[0].bounds.height
				
			if self.ctl_list[1]:
				h-= self.ctl_list[1].bounds.height
				
			self.height = h
			
class BaseViewClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.flex = 'wh'
		self.cc = None      # container class
		self.nv = None      # Navigation Bar class
		self.tb = None      # Toolbar class
		self.cv = None      # ContentView class
		
		self.make_view()
		
	def make_view(self):
		self.cc = ui.View(frame = self.bounds)
		self.cc.flex = 'wh'
		
		self.nv = NavigationBar()
		self.tb = ToolBar()
		self.cv = ContentView([self.nv, self.tb])
		
		self.cc.add_subview(self.nv)
		self.cc.add_subview(self.cv)
		self.cc.add_subview(self.tb)
		
		self.add_subview(self.cc)
		
# in a way, ignore the above. just subclass BaseViewClass..
# can be a lot better, just a idea
# ios has some well defined views, to composite a interface.
class StdClass(BaseViewClass):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.cv.bg_color = 'deeppink'
		
if __name__ == '__main__':
	# some switches here, for testing
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	style  = 'sheet'
	style  = 'panel'
	style  = 'full_screen'
	
	# hide_title_bar
	_htb = False
	
	mc = StdClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style = style, animated=False, hide_title_bar = _htb)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False, hide_title_bar = _htb)
# --------------------

