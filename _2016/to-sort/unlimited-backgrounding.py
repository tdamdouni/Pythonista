# coding: utf-8

# https://forum.omz-software.com/topic/2016/unlimited-backgrounding/10

from __future__ import print_function
import sound
import os
import urllib

# download a silent mp3 if it's not there yet:
if not os.path.exists('silence.mp3'):
  urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
player = sound.Player('silence.mp3')
player.number_of_loops = -1 # repeat forever
player.play()

# do background stuff...

# when you're done:
player.stop()

# --------------------

# sound.Player.number_of_loops = -1

# --------------------

from sound import Player

player = Player('')
player.number_of_loops = -1
player.play()

# --------------------

from objc_util import *
from time import sleep
from datetime import datetime

# "Imports"
AVAudioSession = ObjCClass('AVAudioSession')
AVPlayer = ObjCClass('AVPlayer')
AVPlayerItem = ObjCClass('AVPlayerItem')
NSURL = ObjCClass('NSURL')

# Set Pythonista app to play non-blocking, 'mixed with others' sounds
audio_session = AVAudioSession.sharedInstance()
audio_session.setCategory_withOptions_error_('AVAudioSessionCategoryPlayback', 1, None)

# Create the item to play
sound = NSURL.fileURLWithPath_('silence.mp3')
item = AVPlayerItem.playerItemWithURL_(sound)

# Play the sound (only once)
player = AVPlayer.alloc().initWithPlayerItem_(item)
player.setActionAtItemEnd_(2)
player.play()

while True:
    print('Still running', datetime.now())
    sleep(1)

# --------------------

time.sleep(1)

# --------------------

# coding: utf-8

import sound
import os
import urllib
import clipboard
import time

# download a silent mp3 if it's not there yet:
if not os.path.exists('silence.mp3'):
  urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
player = sound.Player('silence.mp3')
player.number_of_loops = -1 # repeat forever
player.play()

# do background stuff...
current = clipboard.get()
print(current)
while True:
    if current != clipboard.get():
            current = clipboard.get()
            print(current)
    #EDIT: this seems to help
    time.sleep(1)

# when you're done:
player.stop()

# --------------------

# coding: utf-8

import editor
import notification
import sound
import os
import urllib

# download a silent mp3 if it's not there yet:
if not os.path.exists('silence.mp3'):
	urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
player = sound.Player('silence.mp3')
player.number_of_loops = -1 # repeat forever
player.play()

# run the currently open file. I know execfile isnt ideal, but the other option I found is os.system, which didn't work, I think because it uses subprocessing.'
execfile(editor.get_path())

# notify the user when the script is done.
notification.schedule('Your script is done running', delay=0)

# --------------------

time.sleep()

# --------------------
