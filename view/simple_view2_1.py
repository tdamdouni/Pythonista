# Pythonista Forum - @Phuket2

# https://gist.github.com/Phuket2/42924cb9a311ae47084e7f0d05f362f4

import ui, editor

'''
a_path = os.path.expanduser('~/Documents/MyProjects/MyViews')
sys.path.append(a_path)
import class_walker as cw
'''

def add_labels_to_sv(parent):
	# just for debuging. add a label to each subview with the views name
	for v in parent.subviews:
		lb = ui.Label()
		lb.text = v.name
		lb.text_color = 'black'
		lb.size_to_fit()
		lb.center = v.bounds.center()
		lb.flex = 'lrtb'
		v.add_subview(lb)
		
def add_label(v):
	# just for debuging. add a label to each subview with the views name
	lb = ui.Label()
	lb.text = v.name
	lb.text_color = 'black'
	lb.size_to_fit()
	lb.center = v.bounds.center()
	lb.flex = 'lrtb'
	v.add_subview(lb)
	
def translate_number(wh, n):
	# i know can be done better... but thinking will expand this
	# wh is either width or height
	# n is a number that we translate
	if n == 0 or n > 1:
		return n
	elif n == -1:
		return wh
	elif n < 1.0:
		return wh * n
		
def apply_kwargs(kwargs, obj):
	for k, v in kwargs.items():
		if hasattr(obj, k):
			setattr(obj, k, v)
			
def create_content_view(parent, name='cv', margin=(0, 0), **kwargs):
	cv = ui.View(name=name, frame=ui.Rect(*parent.frame).inset(*margin))
	cv.flex = 'wh'
	apply_kwargs(kwargs, cv)
	return cv
	
def inset_into_view(view, v_list, bn='bn', vert=True,
                                        v_margin=(0, 0), **kwargs):
	r = ui.Rect(*view.bounds)
	
	def get_v():
		# return based on vertical or horizontal, maybe not good. But
		# i find this helpful to try to keep the code generic as i can
		return r.height if vert else r.width
		
	# translate the numbers in v_list to absolute numbers, except zero
	v_list = [translate_number(get_v(), x) if x else x for x in v_list]
	
	# var is the space left over in the view after the absolute heights
	# have been subtracted divided by the number if items that are
	# equal to 0
	zero_count = v_list.count(0)
	
	# aviod divide by zero error
	var = (get_v() - sum(v_list)) / zero_count if zero_count else\
	(get_v() - sum(v_list))
	
	# replaces 0 in v_list with var.
	v_list = [var if x == 0 else x for x in v_list]
	
	lst = []        # a list of the views created, we return this
	xy = 0          # keep track of width or height
	# go through v_list, create the views as subviews of cv, and apply
	# some attrs to the created views
	for i, num in enumerate(v_list):
		frame = ui.Rect(0, xy, r.width, num).inset(*v_margin) if vert\
		else ui.Rect(xy, 0, num, r.height).inset(*v_margin)
		
		v = ui.View(name=bn + str(i), frame=frame)
		v.flex = 'whlrtb'
		apply_kwargs(kwargs, v)
		view.add_subview(v)
		xy += num
		lst.append(v)
		
	return lst
	
def split_view_h(parent, view, v_list, h_gap=0):

	#split a view horizontally.
	
	r = ui.Rect(*view.frame)
	
	# reduce our width to allow for the h_gap param
	r.width -= h_gap * (len(v_list) - 1)
	
	# translate the numbers in v_list to absolute numbers
	v_list = [translate_number(r.width, x) if x else x for x in v_list]
	
	# var is the space left over in the view after the absolute heights
	# have been subtracted divided by the number if items that are
	# equal to 0
	zero_count = v_list.count(0)
	
	# aviod divide by zero error
	var = (r.width - sum(v_list)) / zero_count if zero_count else\
	(r.width - sum(v_list))
	
	# replaces 0 in v_list with var.
	v_list = [var if x == 0 else x for x in v_list]
	
	x = r.x
	y = r.y
	
	num_views = len(parent.subviews)
	
	for i, w in enumerate(v_list):
		frame = ui.Rect(x, y, w, r.height)
		if i is 0:
			# this is the frame we split.  we just resize it
			view.frame = frame
		else:
			frame.x += (h_gap * i)
			v = ui.View(name='h' + str(i + num_views), frame=frame)
			v.flex = 'whlrtb'
			v.border_width = view.border_width
			v.corner_radius = view.corner_radius
			parent.add_subview(v)
			
		x += w
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		# dont need this, just if you want an enclosing view,
		# can be handy.
		cv =create_content_view(self, margin=(5, 5),
		bg_color='pink', corner_radius=6)
		
		self.add_subview(cv)
		
		inset_into_view(cv, [44, 0,  60],
		bn ='root', vert=True, v_margin=(4, 4),
		border_color='maroon', corner_radius=6,
		border_width=.5)
		
		split_view_h(cv, cv['root1'], [.5, 0, 0], h_gap=5)
		
		inset_into_view(cv['root1'], [44, 0,  60],
		bn ='root', vert=True, v_margin=(4, 4),
		border_color='maroon', corner_radius=6,
		border_width=.5)
		
		inset_into_view(cv['root0'], [0, 0, 0, 0, 0],
		bn ='root', vert=False, v_margin=(4, 4),
		border_color='maroon', corner_radius=6,
		border_width=.5)
		
		inset_into_view(cv['h4'], [0, 0, 0],
		bn ='root', vert=True, v_margin=(4, 4),
		border_color='maroon', corner_radius=6,
		border_width=.5)
		
		
if __name__ == '__main__':
	_use_theme = False
	w, h = 600, 800
	f = (0, 0, w, h)
	style = ''
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)

