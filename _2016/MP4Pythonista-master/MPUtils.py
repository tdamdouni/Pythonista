# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import NSBundle, ObjCClass

def init():
	NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()

def getPlayer():
	return ObjCClass('MPMusicPlayerController').systemMusicPlayer()

def getNowPlayingQueue():
	p = getPlayer()
	q = []
	for i in range(p.numberOfItems()):
		q.append(p.nowPlayingItemAtIndex(i))
	return q

def createFilter(property, value, is_contains=0):
	mpp = ObjCClass('MPMediaPropertyPredicate').alloc()
	mpp.setProperty(property)
	mpp.setValue(value)
	mpp.setComparisonType(is_contains)
	return mpp
