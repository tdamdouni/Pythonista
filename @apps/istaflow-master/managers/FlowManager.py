# coding: utf-8
import json
import os
import time

class FlowManager (object):
	def __init__(self):
		self.dir = 'flows/'
		if not os.path.exists(self.dir):
			os.mkdir(self.dir)
		
	def get_flows(self):
		return os.listdir(self.dir)
	
	def save_flow(self, title, elements):
		names = []
		for ele in elements:
			names.append(ele.get_title())
		f = open(self.dir+title+'.flow','w')
		f.write(json.JSONEncoder().encode(names))
		f.close()
	
	def delete_flow(self, title):
		if os.path.exists(self.dir+title):
			os.remove(self.dir+title)
	
	def get_element_names_for_flow(self, flow):
		f = open(self.dir+flow,'r')
		fl = json.JSONDecoder().decode(f.read())
		f.close()
		return fl
	
	def run_flow(self, elements):
		output = None
		prevOutputType = None
		for element in elements:
			if element.get_input_type() == None:
				output = element.run()
			else:
				if prevOutputType == element.get_input_type():
					output = element.run(output)
				else:
					raise ValueError('Invalid input type provided to ' + element.get_title())
			prevOutputType = element.get_output_type()