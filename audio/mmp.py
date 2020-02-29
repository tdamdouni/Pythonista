# coding: utf-8

from __future__ import print_function
import webbrowser
from objc_util import *

def main():
    try:
        NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
        webbrowser.open('music://')
        mp = ObjCClass('MPMusicPlayerController')
        mq = ObjCClass('MPMediaQuery')
        query = mq.songsQuery()
        player = mp.systemMusicPlayer()
        player.setQueueWithQuery_(query)
        player.shuffleMode = 2
        player.prepareToPlay()
        player.play()
    except Exception as e:
        print(str(e))
    

if __name__ == '__main__':
    main()
