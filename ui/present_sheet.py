#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/2544/wish-list-for-next-release/82

from __future__ import print_function
import ui

class SomeCustomClass(ui.View):
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
	def show(self, modal = True, factor = 1.0, *args, **kwargs):
		m_bar = 0
		
		if kwargs.get('hide_title_bar', None):
			if kwargs['hide_title_bar']:
				m_bar = 44
				
		if factor <= 1.0 and factor > 0:
			f = (0,0, ui.get_screen_size()[0] * factor , (ui.get_screen_size()[1]-m_bar) * factor)
			self.frame = f
		self.present(*args, **kwargs)
		
		if modal:
			self.wait_modal()
			
if __name__ == '__main__':
	scc = SomeCustomClass(bg_color = 'white')
	scc.show(modal = True , style = 'sheet', factor = .5)
	print('fell through...')

