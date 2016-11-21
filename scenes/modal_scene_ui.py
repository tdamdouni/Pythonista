# https://gist.github.com/glitchassassin/b280d3c5cc06aaf82df3602eb9af843e

# https://forum.omz-software.com/topic/3528/ui-elements-in-modal-scene

import scene, ui

class MainMenu(ui.View):
	def __init__(self):
		ui.View.__init__(self)
		self.scene_view = scene.SceneView()
		self.scene_view.scene = MainMenuScene()
		self.present(hide_title_bar=True)
		self.scene_view.frame = self.bounds
		self.add_subview(self.scene_view)
	def set_login_scene(self):
		loading_scene = LoadingScene(self._login_complete)
		self.scene_view.scene.present_modal_scene(loading_scene)
		#loading_scene.showUiElements()
	def _login_complete(self, username, password):
		self.controller.set_credentials(username, password)
		self.scene_view.scene.dismiss_modal_scene()
		
class MainMenuScene(scene.Scene):
	def __init__(self):
		scene.Scene.__init__(self)
		self.background_color = 'midnightblue'
		self.add_child(scene.Node()) # Dummy node as a bugfix
		pass
		
class LoadingScene (scene.Scene):
	def __init__(self, callback):
		scene.Scene.__init__(self)
		self.callback = callback
		# More setup stuff here
		
	def setup(self):
		self.background_color = "#101020"
		# More setup stuff here
		self.setupUiElements()
		
	def setupUiElements(self):
		self.login_view = ui.load_view('login')
		self.login_view.background_color = 'clear'
		self.login_view.center = self.size/2
		self.login_view.set_callback(self.complete_callback)
		self.presenting_scene.view.add_subview(self.login_view)
		
class LoginView (ui.View): # Actual view is defined in UI Designer File
	def set_callback(self, callback):
		self.callback = callback
	def did_load(self):
		self['connect_button'].action = self.do_callback
	def do_callback(self, sender):
		username = self['txtUsername'].text
		password = self['txtPassword'].text
		if username != "" and password != "":
			self.callback(username, password)
	def keyboard_frame_will_change(self, frame):
		if not self.superview:
			return
		if sum(frame) == 0:
			# Keyboard disappeared
			self.center = (self.superview.width/2, self.superview.height/2)
		else:
			# Keyboard opened
			self.center = (self.superview.width/2, min(self.superview.height/2, frame[1]-100))
			
MainMenu()

