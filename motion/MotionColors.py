# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/804870892914864ba32e

from scene import *
import motion

def mean(list1, limit=0):
	'''
	Find the mean of values in a list.
	Options:
	list1- the inout list of integers
	limit- how many of the most recent items to include. 0 to include all.
	'''
	#Truncate the list to include only the last 'limit' elements
	if len(list1) >= limit and limit:
		list1 = list1[len(list1)-limit:]
	#Return the mean
	return float(sum(list1))/float(len(list1))
	
class main(Scene):
	def setup(self):
		self.fpslist = []
		motion.start_updates()
	def draw(self):
		gravity_vectors = motion.get_attitude()
		roll, pitch, yaw = [x if x < 1.0 else 1.0 for x in [abs(x) for x in gravity_vectors]]
		background(pitch, roll, yaw)
		
		
		tint(1,1,1)
		self.fpslist.append(1/self.dt)
		self.fps = mean(self.fpslist, 5)
		
		fpstext = str(self.fps)[:4]+' FPS'
		text(fpstext, x=5, y=5, alignment=9)
		
		rgbtext = 'R: ' + str(pitch)[:5] + '  G: ' + str(roll)[:5] + '  B: ' + str(yaw)[:5]
		text(rgbtext, x=self.size.w-5, y=5, alignment=7)
	def stop(self):
		motion.stop_updates()
		
		
run(main())

