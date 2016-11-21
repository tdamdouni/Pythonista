# coding: utf-8

# https://forum.omz-software.com/topic/3039/share-draw-text-in-a-circle-not-earth-shattering/2

import ui
# Pythonista Forum - @Phuket2
# for @ccc , should be pep8 ok and pyflakes :)

# No break through here. just expanded on the Pythonista help
# code for ui.ImageContext


# draw text in a circle, and return a ui.image
def text_in_circle(r,
                            text,
                            text_color = 'white',
                            circle_color = 'teal',
                            circle_alpha = 1.0,
                            font_name = 'Arial Rounded MT Bold',
                            inset_percent = 0):

	'''
	text_in_circle - * denotes a param
	==============
	*r-ui.Rect or tuple (0, 0, 0, 0) - the bounding rect for the circle.
	
	*text-text to draw in the circle
	
	*text_color-color of the text drawn inside the circle
	
	*circle_color-color of the circle
	
	*circle_alpha-alpha setting applied to circle color. Note, did this
	for a reason. easier to use string names for colors!
	
	*font_name-the font used to render the *text
	
	*inset_percent-reduces *r by a percentage for l,t,w,h for possible
	better placement of the text inside the circle. a.k.a margin
	
	RETURNS - a rendered uiImage
	
	'''
	
	# this inner function does not need to be here, was just to keep it
	# all together
	def get_max_fontsize(r, text, font_name, inset_rect = ui.Rect()):
		r1 = ui.Rect(*r).inset(*inset_rect)
		for i in xrange(5, 1000):
			w, h = ui.measure_string(text, max_width=0,
			font=(font_name, i), alignment=ui.ALIGN_LEFT,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
			
			if w > r1.width or h > r1.height:
				return (i - 1, ui.Rect(r1.x, r1.y, w, h))
				
	# tuple or Rect? tried issubclass but had problems
	if not type(r) is ui.Rect:
		r = ui.Rect(*r)
		
	inset_rect = ui.Rect(r.x * inset_percent, r.y * inset_percent,
	r.width * inset_percent, r.height * inset_percent)
	
	with ui.ImageContext(r.width, r.height) as ctx:
		oval = ui.Path.oval(r.x, r.y, r.width, r.height)
		c = ui.parse_color(circle_color)
		nc = (c[0], c[1], c[2], circle_alpha)       # color with alpha
		fs, dest_r = get_max_fontsize(r, text, font_name, inset_rect = inset_rect)
		dest_r.center(r.center())
		with ui.GState():
			ui.set_color(nc)
			oval.fill()
			ui.draw_string(text, rect=dest_r,
			font=(font_name, fs), color=text_color,
			alignment=ui.ALIGN_LEFT,
			line_break_mode=ui.LB_TRUNCATE_TAIL)
		return ctx.get_image()
		
		
if __name__ == '__main__':
	r = (0, 0, 200, 200)
	
	img = text_in_circle(r = r, text = 'EHF', circle_alpha = 1)
	# to the console, test
	img.show()
	
	v = ui.View(frame = (0, 0, img.size.width, img.size.height))
	img_v = ui.ImageView(frame = v.frame)
	img_v.image = img
	v.add_subview(img_v)
	v.present('sheet')
	
# --------------------

