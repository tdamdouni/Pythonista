# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/14

import ui

class CustomUIRect(object):
	# my_color = None
	def as_rect(self, x=0, y=0, w=0, h=0):
		r = ui.Rect(x, y, w, h)
		return r
		
	def __init__(self, color):
		print('in init')
		self.my_color = color
		
if __name__ == '__main__':
	r = CustomUIRect('blue').as_rect()
	print(dir(r))
	print(r.my_color)

