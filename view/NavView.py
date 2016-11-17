# coding: utf-8

# https://forum.omz-software.com/topic/1880/navigationview-questions/18

import ui

class NavView(ui.View):
	def __init__(self):
		# Load the default view that's placed inside the Navigation View.
		# This root view has its own pyui file (here: RootView.pyui).
		# That makes it easier to design the root view.
		root = ui.load_view('RootView.pyui')
		# Set the titlebar text of the Navigation View when the root view is loaded
		root.name = 'Root View'
		# Specify the visible buttons in the navigation view titlebar when the root view is visible.
		root.right_button_items = [ui.ButtonItem(action=self.openSubView, image=ui.Image.named('ionicons-close-24'))]
		# Create the Navigation View with the root view preloaded
		self.v = ui.NavigationView(root)
		self.v.present('sheet')
		
	def openSubView(self,sender):
		# Load the sub view thats loaded when the defined button in the Navigation View is pressed while the root view is loaded
		sub = ui.load_view('SubView.pyui')
		# This text will be displayed as the Navigation View's titlebar text
		sub.name = 'Sub View'
		# Display the sub view instead of the root view
		self.v.push_view(sub)
		
# Call the class
#NavView()

