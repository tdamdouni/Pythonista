# https://forum.omz-software.com/topic/3809/display-gif/4

# http://fc00.deviantart.net/fs71/f/2012/189/a/a/dressage_horse_animation_by_lauwiie1993-d56it04.gif

# http://bestanimations.com/Animals/Mammals/Horses/horse-walking-animated-gif1.gif

import os, ui

w=ui.WebView()
filename=os.path.abspath('horse2.gif')
if not (os.path.exists(filename)):
	raise FileNotFoundError('This file does exist!')
w.load_url(filename)
w.present('sheet')

