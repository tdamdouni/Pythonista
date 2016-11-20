# https://forum.omz-software.com/topic/3208/ui-path-append_path-other_path-diff-line_width-values

def make_shape(self):
	with ui.GState():
		r = ui.Rect(*self.bounds).inset(ln_width / 2, ln_width /2)
		s = ui.Path.oval(*r)
		s.line_width = 20
		
	with ui.GState():
		s2 = ui.Path.rect(*s.bounds)
		s2.line_width = .5
		s.append_path(s2)
		s.close()
		s.stroke()
		
# --------------------

