# -*- coding: utf-8 -*-
from console import write_link
from os import path
import sys
import types
from urllib import quote, unquote
 
action_markdown = '''
# {name}
=========================
 
# The Drafts Action
 
Here's the code for the action. It assumes that the Python scripts is in Pythonista's Documents folder and the script's title is *{name}*.
 
    {action}
	
# Import Link
 
If you're on an iOS device and have Drafts installed, you can spare yourself the effort of manually creating the action in Drafts. Just click on the following link:
 
[Import action to Drafts]({importlink})
'''
 
manual_markdown = '''
# Manual
 
[[Instructions here]]
 
# Remarks
 
[[Remarks here]]
'''
 
class DraftsAction():
	def __init__(self, title='', scriptpath=''):
		if scriptpath == '':
			self._scriptpath = sys.argv[0]
		else:
			self._scriptpath = scriptpath
			
		self.name = self._name_of_script()
		
		if title == '':
			self.actiontitle = self.name
		else:
			self.actiontitle = title
			
		self.absolutepath = self._path_of_script()
		self.action = ''
		self.importlink = ''
		# self.data should be read-only.
		self.data = {}
		self.data_update()
		
		
	def __str__(self):
		self.data_update()
		return str(self.data)
 
 
	def _name_of_script(self):
		'''
		Get the name of current file.
		Return name, if it is a .py-script,
		or else raise an error.
		'''
		basename = path.basename(self._scriptpath)
		scriptname = path.splitext(basename)
		return scriptname[0]
 
 
	def _path_of_script(self):
		'''
		Return the path to the script file.
		'''
		absolutepath = path.abspath(self._scriptpath)
		return path.split(absolutepath)[0]
 
 
	def drafts_action(self, *args):
		'''
		A url scheme to a Pythonista script.
		This is to be used as an action content
		in Drafts.
		'''
		argstring = ''
		for arg in args:
			argstring += '&argv=' + arg
		scheme = 'pythonista://{script}?action=run{args}'
		self.action = scheme.format(script=self.name,
	                     args=argstring)
		self.data_update()
 
 
	def drafts_import_link(self):
		'''
		A link for Drafts to import an action.
		'''
		if self.action == '': return
		scheme = 'drafts4://x-callback-url/import_action?type=URL&name={name}&url={url}'
		self.importlink = scheme.format(name=quote(self.actiontitle),
	                  url=quote(self.action))
	 	self.data_update()
 
 
	def data_update(self):
		'''
		Update the data dictionary.
		'''
		self.data =  {'action': self.action,
		              'actiontitle': self.actiontitle,
		              'importlink': self.importlink,
		              'name': self.name,
		              'path': self.absolutepath}
	        
 
	def create_action_file(self):
		'''
		Create a markdown file with Drafts action 
		and import link in the scripts directory.
		'''
		if self.action == '' or self.importlink == '':
			raise ValueError("Make sure you've defined an action and an import link.")
		return action_markdown.format(name=self.name,
		                             action=self.action,
		                             importlink=self.importlink)
 
 
	def create_manual(self):
		'''
		Create a markdown manual template in 
		the scripts directory.
		'''
		if self.action == '' or self.importlink == '':
			raise ValueError("Make sure you've defined an action and an import link.")
		return manual_markdown