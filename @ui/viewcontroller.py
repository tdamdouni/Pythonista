import ui
import shelve

class ViewController(object):
	"""Defines a base class for use in controlling multiple subviews in Pythonista.
	Inherit from this and override the appropriate methods."""
	def __init__(self, view_names, shelf_name=None):
		"""Parameters:
		view_names: LIST of names of views to be controlled by this class. The primary view should come first.
		shelf_name: [optional] STRING name of the shelf object to be opened. Default None--no persistance.
		"""
		self.views = {}
		for view_name in view_names:
			self.views[view_name] = ui.load_view(view_name)
		if shelf_name is None:
			self.will_persist = False
		else:
			self.will_persist = True
			self.shelf_closed = True
			self.shelf_name = shelf_name
			self.shelf = self.open_shelf()
		return

	def bind_actions(self, view_name, actions):
		"""Binds view actions (button presses, etc) to methods of the derived class.
		Parameters:
		view_name: STRING which subview to bind actions in
		actions: DICTIONARY mapping ui element name to call-back functions. Eg:
		{'big_red_button':'blow_up_world', 'cancel_button':'cancel_action'}.
		The keys must EXACTLY match the names defined in the ui designer.
		The values (actions) must be strings that match the name of methods (with parameters self and sender)
		defined in the derived class.
		"""
		view = self.views[view_name]
		for element, action in actions.items():
			view[element].action = action
		return
		
	def open_shelf(self):
		if self.shelf_closed:
			self.shelf_closed = False
			return shelve.open(self.shelf_name)
		else:
			return self.shelf

	def save(self, shelf_key, obj):
		if self.will_persist:
			self.shelf = self.open_shelf()
			self.shelf[shelf_key] = obj
		else:
			raise ValueError('Saving not enabled for this controller')
		return

	def load(self, shelf_key):
		if self.will_persist:
			self.shelf = self.open_shelf()
			value = self.shelf.get(shelf_key, None)
		else:
			raise ValueError('Loading not enabled for this controller')
		return value

	def present(self, view_name, style=None):
		if style is None:
			self.views[view_name].present()
		else:
			self.views[view_name].present(style)
		return

	def close(self, view_name):
		self.views[view_name].close()
		return

	def update_element_text(self, view_name, element_name, new_text):
		view = self.views[view_name]
		view[element_name].text = new_text
		return
		
	def on_exit(self, sender):
		if self.will_persist:
			self.shelf.close()
		for name in self.views.keys():
			self.close(name)
		return
		
	def close_shelf(self):
		if not self.shelf_closed:
			self.shelf.close()
			self.shelf_closed = True
		return
