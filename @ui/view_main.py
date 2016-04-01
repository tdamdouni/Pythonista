# coding: utf-8

import ui
from view_lock import *
from view_messages import *
from view_settings import *

def make_button_item(action, image_name):
    return ui.ButtonItem(action=action, image=ui.Image.named(image_name))


class NavController(ui.View):
	def __init__(self):
		self.vc = {}
		#
		self.vc['lock'] = LockController()
		self.vc['lock'].set_unlock_callback(self.unlock)
		#
		self.vc['messages'] = MessagesController()
		self.vc['messages'].view.right_button_items = [make_button_item(self.bt_settings, 'ionicons-gear-a-24')]
		#
		self.vc['settings'] = SettingsController()
		#
		self.nav_view = ui.NavigationView(self.vc['lock'].view)
		self.nav_view.present(hide_title_bar=True)
	
	def unlock(self):
		self.nav_view.push_view(self.vc['messages'].view)
	
	def bt_settings(self,sender):
		self.nav_view.push_view(self.vc['settings'].view)

NavController()

