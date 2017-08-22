# https://forum.omz-software.com/topic/4125/screen-auto-lock

# Yes, you can add console.set_idle_timer_disabled(True) to your setup method to turn off auto-locking when your game starts.

#You should also add a stop method to your scene (if you haven't already), and go back to the normal behavior there:

class MyScene (Scene):
	# ...
	def stop(self):
		# Note: This will be called automatically when the scene is closed.
		console.set_idle_timer_disabled(False)

