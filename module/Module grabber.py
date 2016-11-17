#coding: utf-8

__name__ = "FileGrabber"
__version__ = "1.5"
__author__ = "671620616" # github username – strangerdanger! :p

__doc__ = '''This script is designed to grab a module file.
It puts a "{modulename}_copy.py" file in the same directory as itself.
I'm kinda a newb at retrieving files from other directories – I'm sure this can be improved alot.
Feel free to do so but please let me know so I can get a copy of the better file!'''

#set to 0 to search for file in sys.path
#set to 1 to use `inspect` module
mode = 0

if mode == 0:
	#search for file in sys.path
	
	import sys
	import os
	import console
	
	#Please Note:
	#    This only works with single-file non-builtin modules!
	#    Given a library, it will either have an error OR clone the {module}.__init__.{suffix} file.
	
	suffixs = (".py", ".pyc", ".pyo") # search for files with these suffixs
	
	def can_exec(path):
		try:
			execfile(path)
		except IOError:
			return False
		finally:
			return True
			
	def try_with_path(p):
		if can_exec(p):
			with open(p,'r') as fr:
				t = fr.read()
			return t
		else:
			raise IOError('File not found')
			
	class getter (object):
		def __init__(self):
			self.raw_path = start
			self.cur_path = path
			self.cur_suffix = suffixs[0]
			self.attempts = attempts
			self.finding = name
			self.file = None
			self.tried_paths = []
			
		def getpath(self):
			if self.cur_path[-1] == "/":
				return self.raw_path + self.finding + self.cur_suffix
			else:
				return self.raw_path + "/" + self.finding + self.cur_suffix
				
		def upd_suf(self,stage):
			self.cur_suffix = suffixs[stage % len(suffixs)]
			return self.cur_suffix
			
		def inc_path(self):
			ind = sys.path.index(self.raw_path) + 1
			self.raw_path = sys.path[ind]
			return self.cur_path
			
		def find(self):
			found = False
			stage = 0
			subcount = 0
			while (not found):
				self.attempts += 1
				self.upd_suf(stage)
				trying = self.getpath()
				self.tried_paths.append(trying)
				try:
					self.file = try_with_path(trying)
				except IOError:
					subcount += 1
					self.attempts += 1
					if subcount >= len(sys.path):
						if (stage >= len(suffixs)):
							break
						else:
							subcount = 0
							stage += 1
				finally:
					if self.file is not None:
						found = True
						break
					if self.attempts >= len(sys.path) * len(suffixs):
						break
					self.inc_path()
					
	def main():
		try:
			exec "import {}".format(name)
			exec "del {}".format(name) # free up some memory if module is large
		except ImportError:
			console.hud_alert(name + " is not a valid module name.", "error")
			return
			
		locater = getter()
		locater.find()
		GET_TEXT = locater.file
		
		if GET_TEXT is None:
			console.hud_alert(name + " is a builtin module.", "error")
			return
			
		document_string = '''# Please Note: This is a module CLONE! It *may* (hopefully not) have errors caused by the transfer script!\n# This module was cloned using {} version {} on mode {}\n# Cloned module: {}{}\n\n'''.format(__name__, __version__, mode, name, locater.cur_suffix)
		copyname = name+"_copy.py"
		
		moduletext = document_string + GET_TEXT
		
		with open(copyname,'w') as fw:
			fw.write(moduletext)
		console.hud_alert("Cloned!")
		
	console.clear()
	name = console.input_alert('Name:')
	attempts = 0
	path = sys.path[0] + name + suffixs[0]
	start = sys.path[0]
	main()
	
if mode == 1:
	# use inspect module to get source file
	
	import inspect
	import console
	name = console.input_alert("Module to clone")
	try:
		exec "import "+name
	except ImportError:
		console.hud_alert("cant find " + name, "error")
		sys.exit(0)
	exec "text = inspect.findsource({})".format(name)
	lines = text[0]
	GET_TEXT = ''
	for line in lines:
		GET_TEXT += line
	document_string = '''# Please Note: This is a module CLONE! It *may* (hopefully not) have errors caused by the transfer script!\n# This module was cloned using {} version {} on mode {}\n# Cloned module: {}\n\n'''.format(__name__, __version__, mode, name)
	copyname = name+"_copy.py"
	
	moduletext = document_string + GET_TEXT
	
	with open(copyname,'w') as fw:
		fw.write(moduletext)
	console.hud_alert("Cloned!")

