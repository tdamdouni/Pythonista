# https://forum.omz-software.com/topic/3547/tip-ui-rect-if-you-are-not-using-it-for-ui-you-should/3

# Pythonista Forum - @Phuket2
import ui, editor

def make_view_rects(view, v_list, vert=True,
                        abs_size=True, margin=(0, 0)):

	# return a list of ui.Rects
	r = ui.Rect(*view.bounds)
	
	def translate_number(wh, n):
		if n == 0 or n > 1: return n
		return wh if n == -1 else wh * n
		
	# adjust v_list to account for margins, if we want positive numbers
	# to remain a fixed size, i.e if you pass 44, and a margin, it will
	# remain 44
	if abs_size:
		extra = margin[0] * 2 if vert else margin[1] * 2
		v_list = [x if x == 0 else (x + extra) for x in v_list]
		
	# translate the numbers in v_list to absolute numbers, except zero
	v_list = [translate_number((r.height if vert else r.width), x)
	if x else x for x in v_list]
	
	zero_count = v_list.count(0)
	
	# aviod divide by zero error
	var = ((r.height if vert else r.width) - sum(v_list)) / zero_count\
	if zero_count else ((r.height if vert else r.width) - sum(v_list))
	
	# replaces 0 in v_list with var.
	v_list = [var if x == 0 else x for x in v_list]
	
	lst = []  # a list of the rects created, we return this
	xy = 0    # keep track of width or height
	for num in v_list:
		lst.append(ui.Rect(0, xy, r.width, num).inset(*margin) if vert
		else ui.Rect(xy, 0, num, r.height).inset(*margin))
		xy += num
		
	return lst
	
	
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.question_panel = None
		self.responses_panel = None
		self.toolbar_panel = None
		
		self.make_view()
		
	def make_view(self):
		inset_w = 10
		inset_h = 10
		v_rects = make_view_rects(self, [60, 0, 0, 0, 60],
		abs_size=True,
		vert=True,
		margin=(inset_h, inset_w))
		for r in v_rects:
			v = ui.View(frame=r, bg_color='cornflowerblue')
			v.border_width = .5
			v.corner_radius = 6
			v.flex = 'tlwhbr'
			self.add_subview(v)
			
if __name__ == '__main__':
	_use_theme = True
	w, h = 600, 800
	w, h = 375, 667
	
	f = (0, 0, w, h)
	style = 'sheet'
	
	mc = MyClass(frame=f, bg_color='white')
	
	if not _use_theme:
		mc.present(style=style, animated=False)
	else:
		editor.present_themed(mc, theme_name='Oceanic', style=style, animated=False)

