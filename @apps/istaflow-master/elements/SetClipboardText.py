# coding: utf-8
from ElementBase import ElementBase
import clipboard

class SetClipboardText(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None
	
	def get_status(self):
		return self.status
	
	def get_input_type(self):
		return 'string'
	
	def get_output(self):
		return self.output
	
	def get_output_type(self):
		return None
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This sets the system clipboard with input provided."
	
	def get_title(self):
		return 'Set Clipboard Text'
		
	def get_icon(self):
		return 'iob:ios7_copy_32'
		
	def get_category(self):
		return 'Utility'
		
	def run(self, input):
		clipboard.set(input)
		self.status = 'complete'