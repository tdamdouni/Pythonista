# coding: utf-8

import ui

class MessagesController(object):
	def __init__(self):
		self.view = ui.load_view('view_messages.pyui')
		self.bt_set_mode(None)
		modesc = self.view['mode_segmentedcontrol']
		modesc.action = self.bt_set_mode
	
	def bt_set_mode(self,sender):
		modesc = self.view['mode_segmentedcontrol']
		idx = modesc.selected_index
		if idx > -1:
			self.mode = modesc.segments[idx]
		else:
			self.mode = None

if __name__ == '__main__':  # pragma: no cover
	my_app = MessagesController()
	my_app.view.present(hide_title_bar=True)
