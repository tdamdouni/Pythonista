# coding: utf-8
from ElementBase import ElementBase

class {{title}}(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = {}
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		#return the input type as a string, return None if not required
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		#return the output type as a string, return None if not required
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = {}):
		self.params = params
		
	def get_description(self):
		#REQUIRED - return a description of the element as a string 
		pass
	
	def get_title(self):
		return '{{title}}'
		
	def get_icon(self):
		#REQUIRED - return element icon to display
		pass
		
	def get_category(self):
		#REQUIRED - return category as a string (case sensitive)
		pass
	
	def run(self, input=''):
		#where the magic happens, put element logic here input is only used if input type is not None, return something if output type is not None, NOTE: for future changes please set self.status to 'complete' if successful or 'error' if error required
		pass