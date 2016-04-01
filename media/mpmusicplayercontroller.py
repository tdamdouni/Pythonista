# coding: utf-8

# https://forum.omz-software.com/topic/2803/valueerror-no-objective-c-class-named-mpmusicplayercontroller-found

import webbrowser
from objc_util import *

def main():
    webbrowser.open('music://')
    mp = ObjCClass('MPMusicPlayerController')
    player = mp.systemMusicPlayer()
    player.play()
    

if __name__ == '__main__':
    main()
# ====================
NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
# ====================