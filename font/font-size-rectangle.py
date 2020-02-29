#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/3009/font-size-for-a-rect

from __future__ import print_function
import ui

# only for testing...
_inset = 0.0
_font_name = 'Avenir Next Condensed'
_frame = ui.Rect(0,0, 320,480)

def font_size_for_rect(rect, text, font_name,
                            inset_factor = 0.0):
	fs_size = 0
	
	# inset the rect, by a factor for width and height
	# the inset can be very helpful
	inset_rect = ui.Rect(rect.width * inset_factor,
	rect.height * inset_factor  )
	
	r = ui.Rect(*rect).inset(*inset_rect)
	
	for fs in xrange(0 , 1000):
		fw, fh = ui.measure_string(text, max_width=0, font=(font_name, fs), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_TRUNCATE_TAIL)
		
		if fw > r.width or fh > r.height:
			fs_size = fs -1
			break
	return fs_size
	
if __name__ == '__main__':
	_frame = ui.Rect(0,0, 320, 480)
	v = ui.View(frame = _frame )
	btn = ui.Button(frame = _frame)
	btn.title = '99'
	btn.bg_color = 'purple'
	
	fs = font_size_for_rect(_frame, '99', _font_name,
	inset_factor = _inset)
	
	print('Calculated Font Size = ' ,  fs)
	btn.font = (_font_name, fs)
	v.add_subview(btn)
	v.present('sheet')

