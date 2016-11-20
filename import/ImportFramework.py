# https://gist.github.com/lukaskollmer/1e0587599ab4d40f59299d72870f22b1

from objc_util import *


class ImportFrameworkError(Exception):
	def __init__(self, name):
		self.name = name
		
	def __str__(self):
		return 'Couldn\'t import {}.framewrork. (Neither from public, nor from private frameworks)'.format(self.name)
		
def _framework_path(name, private):
	return '/System/Library/{}Frameworks/{}.framework'.format('Private' if private else '', name)
	
def importFramework(name):
	global _framework_path # This is required to work when the import stuff is importes in the startup file
	public_path = _framework_path(name, private=False)
	private_path = _framework_path(name, private=True)
	
	bundle = NSBundle.bundleWithPath_(public_path)
	
	if not bundle is None:
		bundle.load()
	else:
		# Could not load public bundle, will try private
		bundle = NSBundle.bundleWithPath_(private_path)
		if not bundle is None:
			bundle.load()
		else:
			raise ImportFrameworkError(name)
			
if __name__ == '__main__':
	importFramework('UIKit')
	importFramework('')

