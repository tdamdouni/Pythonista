# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2028/play-mp3-from-ui-doesn-t-work-sound-module_

play_b = ui.ButtonItem(title='play',action=playmp3,enabled=True)

###==============================

def playmp3(sender):
	player = sound.Player('filename')
	player.play()
	
###==============================

player = sound.Player('filename')

def playmp3(sender):
	player.play()

