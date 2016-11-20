# https://forum.omz-software.com/topic/3206/ui-path-attributes-would-be-great-if-there-were-mor

def draw_shape(self, shape = 'rect', r = None,
                    stroke = False, fill = False):
	if not r:
		r = self.bounds
		
	if shape is 'rect':
		s = ui.Path.rect(*r)
	elif shape is 'oval':
		s = ui.Path.rect(*r)
	else:
		s = ui.Path.rounded_rect(*r, * self.corner_radius)
		
	if stroke:
		s.stroke()
		
	if fill:
		s.fill()
		
# --------------------

def make_circle(w):
	# standalone ui.Path
	r = ui.Rect(0, 0, w, w)
	s = ui.Path.oval(*r)
	s.line_width = .5                   #valid
	s.fill_color = 'silver'             #invalid
	s.stroke_color = 'black'            #invalid
	s.shadow = ('yellow', 1, 1, 8)      #invalid
	return s
	
# --------------------

