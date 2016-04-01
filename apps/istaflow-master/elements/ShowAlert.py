# coding: utf-8
import console
from ElementBase import ElementBase

class ShowAlert(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None
		
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'string'
		
	def get_output(self):
		self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return None
		
	def set_params(self):
		return None
		
	def get_description(self):
		return "This show an alert from the string that is in the input parameter"
	
	def get_title(self):
		return 'Show Alert'
		
	def get_icon(self):
		return 'iob:alert_circled_32'
		
	def get_category(self):
		return 'Utility'
		
	def run(self, input):
		self.status = 'complete'
		console.alert(title='Message',message=input,button1='Ok',hide_cancel_button=True)
		