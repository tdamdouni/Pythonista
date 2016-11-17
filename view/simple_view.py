# Pythonista Forum - @Phuket2

# https://gist.github.com/Phuket2/5fc3c45aa19e52e26df4903421a8fa66

import ui, editor

def add_labels_to_sv(parent):
	# just for debuging. add a label to each subview with the views name
	for v in parent.subviews:
		lb = ui.Label()
		lb.text = v.name
		lb.size_to_fit()
		lb.center = v.bounds.center()
		lb.flex = 'lrtb'
		v.add_subview(lb)
		
def split_view_h(parent, view, v_list, h_gap=0):
	'''
	split a view horizontally.
	'''
	r = ui.Rect(*view.frame)
	
	# reduce our width to allow for the h_gap param
	r.width -= h_gap * (len(v_list) - 1)
	
	def translate_width(pw, w):
		# i know can be done better... but thinking will expand this
		if w == 0 or w > 1:
			return w
		elif w == -1:
			return ph
		elif w < 1.0:
			return pw * w
			
	# translate the numbers in v_list to absolute numbers
	v_list = [translate_width(r.width, x) if x else x for x in v_list]
	
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
		
		
def simple_vert_view(parent, v_list, cv_margin=(0, 0),
                                        v_margin=(0,0), *args, **kwargs):
	'''
	simple_h_view:
	Description - creates a number of ui.Views vertically. A root ui.View
	named 'cv' is created first. The vertical views are subviews of 'cv'
	params -
	1. parent = the parent view that this view will be a subview of
	2. v_list = a list of numbers. each number represents the height
	of the view. as follows
	0  = fill the free space, if more than one, its divided
	<1 = is a percentage if the overall height avail
	>1 = is a abs points value
	3. cv_margin, is used when creating the rect fir the 'cv' view.
	the 'cv' is equal to the parent.bounds.inset(*cv_margin).
	4. v_margin = is called on the ui.rect that is used to create
	the view. The view is already sized as per the v_list.
	so this will change the dimensions of the view. not trying to
	go the other way, meaning adusting the abs values in the v_list,
	would not be hard to do, but this way makes more sense i think.
	5. **kwargs = kwargs are evaluated for every view, including the
	'cv' view.  just a choice.
	
	returns:
	a ui.View. The view returned is named 'cv', contains the views
	created from v_list as subviews. each subview is named p0..pn
	'''
	r = ui.Rect(*parent.bounds).inset(*cv_margin)
	cv = ui.View(name='cv', frame=r)
	cv.bg_color = 'pink'
	cv.flex = 'wh'
	
	def translate_height(ph, h):
		# i know can be done better... but thinking will expand this
		if h == 0 or h > 1:
			return h
		elif h == -1:
			return ph
		elif h < 1.0:
			return ph * h
			
	def apply_kwargs(kwargs, obj):
		for k, v in kwargs.items():
			if hasattr(obj, k):
				setattr(obj, k, v)
				
	# translate the numbers in v_list to absolute numbers
	v_list = [translate_height(r.height, x) if x else x for x in v_list]
	
	# var is the space left over in the view after the absolute heights
	# have been subtracted divided by the number if items that are
	# equal to 0
	zero_count = v_list.count(0)
	
	# aviod divide by zero error
	var = (r.height - sum(v_list)) / zero_count if zero_count else\
	(r.height - sum(v_list))
	
	# replaces 0 in v_list with var.
	v_list = [var if x == 0 else x for x in v_list]
	
	y = 0           # keep track of the height
	# go through v_list, create the views as subviews of cv, and apply
	# some attrs to the created views
	for i, h in enumerate(v_list):
		frame = ui.Rect(0, y, r.width, h).inset(*v_margin)
		v = ui.View(name='p' + str(i), frame=frame)
		v.flex = 'whlrtb'
		apply_kwargs(kwargs, v)
		cv.add_subview(v)
		y += h
		
	# hmmm, to do or not do?
	apply_kwargs(kwargs, cv)
	return cv
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		self.make_view()
		
	def make_view(self):
		#v_list = [44, 0, 0, 0, 44, .5, 60]
		#v_list = [44, 0, 60]
		#v_list = [.5, .4, 0, 0]
		#v_list = [44, .2, 0, 60]
		#v_list = [.5, .5]
		#v_list = [48, .4, 0, 64]
		v_list = [44, 0, 60]
		
		v = simple_vert_view(self, v_list, cv_margin=(2, 2),
		v_margin=(5, 5), corner_radius=5, border_width=.5)
		self.add_subview(v)
		
		#v_list = [.3333, .3333, .3333]
		#v_list = [.5, .5]
		v_list = [.8, 20, 44, 0]
		p = self['cv']
		
		v_to_split = p['p1']
		v_list = [.8, 20, 44, 0]
		split_view_h(p, v_to_split, v_list, h_gap=5)
		
		v_to_split = p['p2']
		v_list = [.5, .5]
		split_view_h(p, v_to_split, v_list, h_gap=10)
		
		
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)
		
	# accessing a view, different ways
	mc['cv']['p0'].bg_color = 'crimson'
	cv = mc['cv']
	cv.subviews[len(cv.subviews)-1].bg_color = 'cornflowerblue'
	add_labels_to_sv(cv)

