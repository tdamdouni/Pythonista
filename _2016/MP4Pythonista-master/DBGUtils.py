# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

def dp(o):
	try:
		cname = o._get_objc_classname()
		cname = cname.decode('utf-8')
	except AttributeError:
		cname = 'Non-Objective-C object'
	finally:
		for i in dir(o):
			print("'%s'" % i)
		print('[%s]\n' % cname)

def printMediaItem(item, verbose=False):
	print(item.title())
	if verbose:
		print('- artist: %s' % item.artist())
		print('- albumTitle: %s' % item.albumTitle())
		print('- persistentID: %d' % item.persistentID())

def printItemCollections(ls, verbose=False):
	for item in ls:
		try:
			item.title()
		except AttributeError: #collections?
			try:
				item = item.items()[0] #item position in collections()[i]
			except AttributeError:
				print('Neither items nor collections.')
				raise
			except:
				raise
		printMediaItem(item, verbose)
	print()
