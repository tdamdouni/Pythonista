# coding: utf-8
from os import listdir
from os.path import isfile, join, splitext
from importlib import import_module
import sys
sys.path.append('elements')

class ElementManager (object):
	elementsFolder = 'elements'
	elementExclusionList = ('ElementBase.py','__init__.py','Template.py')
	requiredElementInstanceMethods = ('get_status','get_input','get_output','get_input_type','get_output_type','get_params','set_params','get_description','get_title','get_category','get_icon','run')
	
	def get_all_elements(self, type=''):
		elements = [splitext(f) for f in listdir(self.elementsFolder) if isfile(join(self.elementsFolder, f)) and not f in self.elementExclusionList]
		validElements = []
		invalidElements = []
		for i in elements:
			mod = import_module(i[0])
			reload(mod)
			cla = getattr(mod,i[0])
			try:
				for method in self.requiredElementInstanceMethods:
					getattr(cla(), method)
				validElements.append(cla())
			except (NotImplementedError, AttributeError):
				invalidElements.append(cla())

		if type == '':
			return {'valid':validElements, 'invalid':invalidElements}
		elif type == 'valid':
			return validElements
		elif type == 'invalid':
			return inValidElements
		else:
			return []	
		
	def get_element_class(self, element):
		return type(element).__name__
	
	def get_element_with_title(self, title):
		elements = self.get_all_elements('valid')
		for element in elements:
			if element.get_title() == title:
				return element
		return None
	
	def create_element(self, title):
		titleValidated = title.replace(" ","")
		templatePath = self.elementsFolder + '/Template.py'
		f = open(templatePath, 'r')
		tem = f.read()
		print tem
		tem = tem.replace("{{title}}",titleValidated)
		f.close()
		f = open(self.elementsFolder+'/'+titleValidated+'.py','w')
		f.write(tem)
		f.close()