# https://gist.github.com/jsbain/30e03172edec4bfa70fb05358165a399

import ui
class Screen(ui.View):
	def __init__(self,view):
		scale=(min(ui.get_screen_size())-64)/1024.
		self.view=view
		self.add_subview(view)
		self.transform=ui.Transform.scale(scale,scale)
		rb=[]
		for b in ['ipad','ipad_land','iphone','iphone_land']:
			btn=ui.ButtonItem()
			btn.title=b
			btn.action=self._action
			rb.append(btn)
		self.right_button_items=rb
		self._action(self.right_button_items[0])
	def _action(self,sender):
		if sender.title=='ipad':
			self.view.frame=(0,0,768,1024)
		if sender.title=='ipad_land':
			self.view.frame=(0,0,1024,768)
		if sender.title=='iphone':
			self.view.frame=(0,0,320,576)
		if sender.title=='iphone_land':
			self.view.frame=(0,0,576,320)
			
v=ui.View()
v.border_color=(1,0,0)
v.border_width=8
Screen(v).present()

