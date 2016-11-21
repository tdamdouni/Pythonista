# coding: utf-8

# https://forum.omz-software.com/topic/1765/cyclic-animations

# https://forum.omz-software.com/topic/2928/ui-animate-wider-usage/9

import time
import ui, console

root=ui.View(frame=(0,0,500,500))
somecontainer=ui.View(frame=(50,5,200,200),bg_color=(1,0,0))
root.add_subview(somecontainer)
b=ui.Button(bg_color=(0,1,0),frame=(50,50,100,100))
somecontainer.add_subview(b)
b.action=lambda sender:console.hud_alert('yes, i am a button')


def demo(flex):
	#show the flex mode of b by resizing its parent view, first big, then small.
	b.flex=flex
	b.title="b.flex='{}'".format(b.flex)
	duration=1.0 #animation speed
	def small():
		somecontainer.frame=(50,50,200,200)
	def big():
		somecontainer.frame=(50,50,400,400)
	def animation_small():
		#completion could call animation_big again, as long as you have a stopping condition!
		ui.animate(small, duration=duration)
	def animation_big():
		#animate to big size, then call animation_small
		ui.animate(big, duration=duration,completion=animation_small)
	animation_big()
	
	
root.present('sheet')
for x in ['','lrtb','l','t','w','h','wh','wl','ht']:
	demo(x)
	time.sleep(3.0)

