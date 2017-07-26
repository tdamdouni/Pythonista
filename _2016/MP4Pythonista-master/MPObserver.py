# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import *

class MPObserver:
	def __init__(self, l_mpc):
		def willResignActive(_self, _cmd):
			l_mpc.onWillResignActive()
		def didBecomeActive(_self, _cmd):
			l_mpc.onDidBecomeActive()
		def playbackStateDidChange(_self, _cmd):
			l_mpc.onPlaybackStateDidChange()
		def nowPlayingItemDidChange(_self, _cmd):
			l_mpc.onNowPlayingItemDidChange()
		self.mpc = l_mpc
		self.nmo = create_objc_class(
			'NSMPObserver',
			methods = [
				willResignActive,
				didBecomeActive,
				playbackStateDidChange,
				nowPlayingItemDidChange
			]
		).alloc()
		self.nc = ObjCClass('NSNotificationCenter').defaultCenter()
	def addAllObservers(self):
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('willResignActive'),
			'UIApplicationWillResignActiveNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('didBecomeActive'),
			'UIApplicationDidBecomeActiveNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('playbackStateDidChange'),
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('nowPlayingItemDidChange'),
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification',
			None
		)
		self.mpc.player.beginGeneratingPlaybackNotifications()
	def removeAllObservers(self):
		self.nc.removeObserver_name_object_(
			self.nmo,
			'UIApplicationWillResignActiveNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'UIApplicationDidBecomeActiveNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification',
			None
		)
		self.mpc.player.endGeneratingPlaybackNotifications()

if __name__=='__main__':
	from objc_util import NSBundle
	
	NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
	
	class TestClass:
		def __init__(self):
			self.player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		def onWillResignActive(self):
			print('willResignActive')
		def onDidBecomeActive(self):
			print('didBecomeActive')
		def onPlaybackStateDidChange(self):
			print('playbackStateDidChange')
		def onNowPlayingItemDidChange(self):
			print('nowPlayingItemDidChange')
	
	c = TestClass()
	d = MPObserver(c)
	print("MPObserver is set in 'd'")
