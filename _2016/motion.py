# https://gist.github.com/omz/a47ae64580439da539574b5da3c71932

# https://twitter.com/olemoritz/status/824848141732106242

# https://forum.omz-software.com/topic/3827/motion-module

# `motion` module from Pythonista
# This is missing in the current App Store versions (in Pythonista 3.x, it's only missing in Python 2 mode).
# As a temporary workaround, you can put this file in the "site-packages" folder (under "Modules" or "Modules & Templates").

import _motion

shared_manager = _motion.MotionManager()

def start_updates():
	shared_manager.start()

def stop_updates():
	shared_manager.stop()

def get_gravity():
	return shared_manager.gravity

def get_user_acceleration():
	return shared_manager.user_acceleration

def get_attitude():
	return shared_manager.attitude

def get_magnetic_field():
	return shared_manager.magnetic_field

class MotionUpdates (object):
	def __enter__(self):
		start_updates()
	
	def __exit__(self, type, value, traceback):
		stop_updates()
