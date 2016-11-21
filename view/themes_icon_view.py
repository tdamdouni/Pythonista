# https://gist.github.com/Phuket2/06d09ee0f51214e91caa9fed5757418b

'''
        Pythonista Forum - @Phuket2
'''
import ui, editor, bz2, base64
#_pyui_file_name = 'booking.pyui'

__pyui_str__ ='''
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
'''

from collections import deque

class ViewWalker(object):
	# JonB
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
		
def pyui_decode(str):
	s = bz2.decompress(base64.b64decode(str))
	return s.decode('utf-8')
	
def WrapInstance(obj):
	class Wrapper(obj.__class__):
		def __new__(cls):
			return obj
	return Wrapper
	
	
class ThemeViewer(ui.View):
	def __init__(self, pyui_str , theme,  *args, **kwargs):
		#ui.load_view(_pyui_file_name,
		#bindings={'MyClass': WrapInstance(self), 'self': self})
		ui.load_view_str(pyui_str, bindings={'MyClass': WrapInstance(self), 'self': self})
		
		super().__init__(*args, **kwargs)
		
		self.tc = None
		self.set_tint_color_cheat(theme)
		self.theme = theme
		self.border_width=.5
		self.corner_radius = 6
		self.border_color='darkgray'
		self.update_view()
		
	def update_view(self):
	
		self['lb_theme'].border_color = 'darkgray'
		self['lb_theme'].text = self.theme
		
		# attempt to set all subviews border color to the correct
		# tint color.only shown on obects that have a border_width set
		for sv in ViewWalker(self).sub_view_objects():
			sv.border_color = self.tc
			
	def reset_theme(self, sender):
		#print('in, reset_theme')
		self.theme = sender.title
		self.set_tint_color_cheat(self.theme)
		editor.apply_ui_theme(self, theme_name = sender.title)
		self.update_view()
		
	def set_tint_color_cheat(self, theme):
		# maybe this is a screw up....
		#return
		btn = ui.Button()
		editor.apply_ui_theme(btn, theme_name = theme)
		self.tc = btn.tint_color
		
	def take_screenshot(self):
		# take a screenshot of the ui.View.bounds
		with ui.ImageContext(self.width, self.height) as ctx:
			self.draw_snapshot()
			return ctx.get_image()
			
if __name__ == '__main__':
	# initial theme
	theme = 'Cool Glow'
	
	# decode the pyui str
	pyui_str = pyui_decode(__pyui_str__)
	
	tv = ThemeViewer(theme = theme , pyui_str = pyui_str)
	
	editor.present_themed(tv, theme_name=theme, style='sheet', animated=False)
	
	# take a screen shot of the view, could be used to create thumbnail
	# images for example...
	img = tv.take_screenshot()
	
	# show the image in the console
	img.show()
	
	# write the snapshot to a png file
	bytes = img.to_png()
	with open(theme + '.png', 'wb') as file:
		file.write(bytes)

