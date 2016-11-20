# coding: utf-8

# https://gist.github.com/bmw1821/bc2ccf257d60804be010

import sys
import os
from UIKit import *

sys.path.append(os.path.expanduser('~/Documents/site-packages/Pydia/Pydia Supporting Files/'))

import Pydia_Sources
import Pydia_Package

Sources = Pydia_Sources
Package = Pydia_Package

def supporting_file_dir_for_identifier(identifier):
	return os.path.expanduser('~/Documents/site-packages/Pydia/Package Support/') + identifier + '/'
	
def activate_supporting_files_for_identifier(identifier):
	sys.path.append(supporting_file_dir_for_identifier(identifier))
	
def launch():
	sys.path.append(os.path.expanduser('~/Documents/site-packages/Pydia/Pydia Supporting Files/Pydia UI'))
	from Pydia_UI import main
	main()

