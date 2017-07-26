# -*- coding: utf-8 -*-

# https://github.com/mogira/MP4Pythonista

from __future__ import print_function, unicode_literals
from objc_util import ObjCClass
from DBGUtils import *
import MPUtils
	
if __name__ == '__main__':
	MPUtils.init()
	
	printItemCollections(MPUtils.getNowPlayingQueue())
	
	player = MPUtils.getPlayer()
	mq = ObjCClass('MPMediaQuery').songsQuery()
	
	f0 = MPUtils.createFilter('isCloudItem', False)
	mq.addFilterPredicate(f0)
	
	player.setQueueWithQuery(mq)
	player.prepareToPlay()
	#player.play()

	print('↑ will be rewrited to ↓\n')
	printItemCollections(player.queueAsQuery().items())
