# coding: utf-8

# https://gist.github.com/nitricware/468b31a1b5363c4474e1

import ui
import dialogs

def pressButton(sender):
	dialogs.hud_alert('okay2')
	# Setting the text of the label in the root view from the sub view. works fine.
	root['label1'].text = 'done'
	# Trying to call the method doSomething
	NavView.doSomething()
	
# Load the sub view thats loaded when the defined button in the Navigation View is pressed while the root view is loaded
subview = ui.load_view('SubView.pyui')
# This text will be displayed as the Navigatuion View's titlebar text
subview.name = 'Sub View'

# Load the default view that's placed inside the Navigation View.
# This root view has its own pyui file (here: RootView.pyui).
# That makes it easier to design the root view.
root = ui.load_view('RootView.pyui')

class NavView(ui.View):
	def __init__(self):
		# Specify the visible buttons in the navigation view titlebar when the root view is visible.
		root.right_button_items = [ui.ButtonItem(action=self.openSubView, image=ui.Image.named('ionicons-close-24'))]
		# Set the titlebar text of the Navigation View when the root view is loaded
		root.name = 'Root View'
		# Create the Navigation View with the root view preloaded
		self.v = ui.NavigationView(root)
		self.v.name = 'navview'
		self.v.width = 320
		self.v.height = 480
		self.v.present('sheet')
		
	def openSubView(self,sender):
		# Display the sub view insteaf of the root view
		self.v.push_view(subview)
		
	def doSomething(self):
		dialogs.hud_alert('okay3')
		# Trying to close the subview and go back to root view
		self.v.close()
		
# Call the class
NavView()

