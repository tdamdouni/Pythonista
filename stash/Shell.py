from __future__ import print_function
# Based on https://gist.github.com/4063716
# 
# Provides a simple shell with basic
# commands for dealing with files and 
# directories.
#
# This script will try and prevent 
# unsafe file operations outside of
# Documents directory.
# 
# Add a setting named allow_unsafe and
# in the config dict and set to True
# to disable these preventative measures.

import os
import cmd
import console
import shlex
import sys

config = {}

def main():
	shell = Shell()
	shell.prompt = '> '
	shell.cmdloop()
	
colors = {'blue':(0,0,1),
          'red':(1,0,0)}

def get_color(color):
	return colors.get(color, None)

def print_in_color(color_name, msg):
	color = get_color(color_name)
	if color:
		console.set_color(*color)
	print(msg)
	console.set_color()

class Shell(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.startup_dir = os.getcwd()
				
	def safe_path(self, path):
		if config.get('allow_unsafe'):
			return True 
		paths = [self.startup_dir, os.path.normpath(path)]
		return self.startup_dir == os.path.commonprefix(paths)

	def do_ls(self, line):
		try:
			for f in sorted(os.listdir(os.getcwd())):
				if os.path.isdir(f):
					print_in_color('blue', f)
				else:
					print_in_color('default', f)
		except OSError as e:
			print(e)

	def do_pwd(self, line):
		print(os.getcwd())
	
	def do_cat(self, line):
		args = shlex.split(line)
		if len(args) == 0:
			return
		try:
			with open(args[0], 'r') as f:
				for l in f:
					sys.stdout.write(l)
		except Exception as e:
			print_in_color('red', e)
	
	def do_cd(self, line):
		args = shlex.split(line)
		if not args:
			args = ['~/Documents']
		dir = os.path.expanduser(args[0])
		if os.path.exists(dir):
			os.chdir(dir)
			self.do_pwd(line)
		else:
			print('Directory does not exist: ' + dir)
	
	def do_mkdir(self, line):
		args = shlex.split(line)
		if len(args) == 0:
			return
		if not self.safe_path(os.getcwd()):
			print('Changes to unsafe directories are disabled.')
			return 
		if os.path.exists(args[0]):
			print('Directory already exists: ' + args[0])
			return
		try:
			os.mkdir(args[0])
		except OSError as e:
			print(e)
		
	def do_rm(self, line):
		args = shlex.split(line)
		if len(args) == 0:
			return
		if not os.path.exists(args[0]):
			print('Invalid path: ' + args[0])
			return 
		elif not self.safe_path(os.path.abspath(args[0])):
			print('Changes to unsafe directories are disabled.')
			return 
		elif os.path.isdir(args[0]):
			try:
				os.rmdir(args[0])
			except OSError as e:
				print(e)
		else:
			try:
				os.remove(args[0])
			except OSError as e:
				print(e)

if __name__ == '__main__':
	main()
