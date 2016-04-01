# coding: utf-8

# https://github.com/shaun-h/istaflow

from views import ElementListView, FlowCreationView, FlowsView
from managers import ElementManager, FlowManager
import ui
import collections
import console
import os

class ista(object):
	def __init__(self):
		self.elements_view = None
		self.flow_creation_view = None
		self.navigation_view = None
		self.flow_view = None
		self.element_manager = None
		self.flow_manager = None
		self.elements = None
		self.selectedElements = []
		self.flows = []
		self.selectedFlow = None
		self.setup_elementsmanager()
		self.setup_flowsmanager()		
		self.get_valid_elements()
		self.get_flows()
		self.setup_elementsview()
		self.setup_flowsview()
		self.setup_flowcreationview()
		self.setup_navigationview(self.flow_view)
	
	def get_valid_elements(self):
		if self.element_manager == None:
			raise ValueError("element_manager hasnt been initialised")
		else:	
			elements_to_sort = self.element_manager.get_all_elements(type='valid')
			for element in elements_to_sort:
				if self.elements == None:
					self.elements = {}
				try:
					ele_value = self.elements[element.get_category()]
					ele_value.append(element)
					ele_value.sort(key=lambda x:x.get_title())
					self.elements[element.get_category()] = ele_value
				except KeyError:
					self.elements[element.get_category()]=[element]
		self.elements = collections.OrderedDict(sorted(self.elements.items(), key=lambda t:t[0] ))
	
	def get_flows(self):
		self.flows = self.flow_manager.get_flows()
		
	def show_flowcreationview(self, sender):
		self.validate_navigationview()
		self.selectedElements = []
		if not self.selectedFlow == None:
			elementNames = self.flow_manager.get_element_names_for_flow(self.selectedFlow)
			for name in elementNames:
				self.selectedElements.append(self.element_manager.get_element_with_title(name))
			
			self.flow_creation_view.data_source.title = os.path.splitext(self.selectedFlow)[0]
			self.selectedFlow = None
		else:
			self.flow_creation_view.data_source.title = ''
		self.flow_creation_view.data_source.elements = self.selectedElements
		self.flow_creation_view.reload_data()
		
		if self.flow_creation_view == None:
			raise ValueError("flow_creation_view hasnt been initialised")
		else:	
			self.flow_creation_view.editing = False
			self.navigation_view.push_view(self.flow_creation_view)
			
	
	def setup_navigationview(self, initview):           
		initview.right_button_items = [ui.ButtonItem(title='Add Flow', action=self.show_flowcreationview)]
		initview.left_button_items = [ui.ButtonItem(title='Create Element', action=self.create_element)]
		self.navigation_view = ui.NavigationView(initview)
	
	def setup_flowsmanager(self):
		self.flow_manager = FlowManager.FlowManager()
		
	def setup_elementsmanager(self):
		self.element_manager = ElementManager.ElementManager()
				
	def setup_elementsview(self):
		self.elements_view = ElementListView.get_view(self.elements, self.elementselectedcb)
	
	def setup_flowsview(self):
		self.flow_view = FlowsView.get_view(self.flows, self.flowselectedcb, self.deleteflow)
		
	def setup_flowcreationview(self):
		self.flow_creation_view = FlowCreationView.get_view(self.selectedElements, self.savecb)
		self.flow_creation_view.right_button_items = [ui.ButtonItem(title='+', action=self.show_elementsview), ui.ButtonItem(title='Save', action=self.saveflow)]
		self.flow_creation_view.left_button_items = [ui.ButtonItem(title='Play',action=self.runflow)]
		
	def deleteflow(self, flowtitle):
		self.flow_manager.delete_flow(flowtitle)
	
	@ui.in_background
	def saveflow(self,sender):
		if self.flow_creation_view.data_source.title == '':
			console.alert(title='Error',message='Please enter a title',button1='Ok',hide_cancel_button=True)
		else:
			self.flow_manager.save_flow(self.flow_creation_view.data_source.title, self.selectedElements)
			console.alert(title='Success',message='Flow has been saved',button1='Ok',hide_cancel_button=True)
			self.get_flows()
			self.flow_view.data_source.flows = self.flows
			self.flow_view.reload_data()
		
	def validate_navigationview(self):
		if self.navigation_view == None:
			raise ValueError("navigation_view hasn't been initialised")
			
	def show_elementsview(self, sender):
		self.validate_navigationview()
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.navigation_view.push_view(self.elements_view)
			
	def close_elementsview(self):
		if self.elements_view == None:
			raise ValueError("elements_view hasnt been initialised")
		else:	
			self.navigation_view.pop_view(self.elements_view)
	
	def close_flowcreationview(self):
		if self.flow_creation_view == None:
			raise ValueError("flow_creation_view hasnt been initialised")
		else:	
			self.navigation_view.pop_view(self.flow_creation_view)
	
	def show_mainview(self):
		self.validate_navigationview()
		self.navigation_view.present()
		
	def elementselectedcb(self, element):
		self.selectedElements.append(element)
		self.flow_creation_view.data_source.elements=self.selectedElements
		self.flow_creation_view.reload_data()
		self.close_elementsview()
		
	def savecb(self, saveElements):
		self.selectedElements = saveElements
		self.close_flowcreationview()
		
	def flowselectedcb(self, flow):
		self.selectedFlow = flow
		self.show_flowcreationview(None)
	
	@ui.in_background
	def create_element(self, sender):
		title = console.input_alert(title='Enter Element title', message='Title cannot have spaces and will be replaced. If element with file exists it will be overwritten without warning.')
		self.element_manager.create_element(title=title)
		console.hud_alert('Element created')
		
	@ui.in_background
	def runflow(self,sender):
		try:
			self.flow_manager.run_flow(self.selectedElements)
		except ValueError, e:
			console.alert(str(e))

def main():
	m = ista()
	m.show_mainview()
	
if __name__ == '__main__':
	main()