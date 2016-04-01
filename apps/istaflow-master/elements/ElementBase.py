# coding: utf-8
class ElementBase (object):
	
	def get_status(self):
		raise NotImplementedError("Class %s doesn't implement get_status()" % (self.__class__.__name__))
		
	def get_input(self):
		raise NotImplementedError("Class %s doesn't implement get_input()" % (self.__class__.__name__))

	def get_output(self):
		raise NotImplementedError("Class %s doesn't implement get_output()" % (self.__class__.__name__))

	def get_input_type(self):
		raise NotImplementedError("Class %s doesn't implement get_input_type()" % (self.__class__.__name__))

	def get_output_type(self):
		raise NotImplementedError("Class %s doesn't implement get_output_type()" % (self.__class__.__name__))

	def get_params(self):
		raise NotImplementedError("Class %s doesn't implement get_params()" % (self.__class__.__name__))
		
	def set_params(self):
		raise NotImplementedError("Class %s doesn't implement set_params()" % (self.__class__.__name__))
			
	def get_description(self):
		raise NotImplementedError("Class %s doesn't implement get_description()" % (self.__class__.__name__))
		
	def get_title(self):
		raise NotImplementedError("Class %s doesn't implement get_title()" % (self.__class__.__name__))
	
	def get_icon(self):
		raise NotImplementedError("Class %s doesn't implement get_icon()" % (self.__class__.__name__))
	
	def get_category(self):
		raise NotImplementedError("Class %s doesn't implement get_category()" % (self.__class__.__name__))
	
	def run(self):
		raise NotImplementedError("Class %s doesn't implement run()" % (self.__class__.__name__))