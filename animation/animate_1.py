# coding: utf-8

# https://gist.github.com/balachandrana/097b35a63c3bcf8b64ec198413df9b7e

# code from https://github.com/controversial/ui2/blob/master/ui2/animate.py
# code modified for bug in https://forum.omz-software.com/topic/3504/lab-ui-animate-sliding-in-views
from copy import copy

from objc_util import *

# Constants representing easings. See http://apple.co/29FOF5i

ANIMATE_EASE_IN = 1 << 16
ANIMATE_EASE_OUT = 2 << 16
ANIMATE_EASE_IN_OUT = 0 << 16
ANIMATE_EASE_NONE = ANIMATE_LINEAR = 3 << 16


class Animation(object):
	"""Represents an animation to one or more properties of an object."""
	def __init__(self, animation, duration=0.25, delay=0.0, completion=None,
	easing=ANIMATE_EASE_IN_OUT):
		self.animation = animation
		self.duration = duration
		self.delay = delay
		self.completion = completion
		self.easing = easing
		
		self._completion = None  # Used internally when a callback is needed
		
	def play(self):
		"""Perform the animation."""
		# If any callbacks are set, we set up a block
		funcs = (self.completion, self._completion)  # Possible callbacks
		if any(funcs):
			def c(cmd, success):
				"""A completion function wrapping one or more callbacks."""
				for func in funcs:
					if func:  # Only call the registered ones
						func(success)
				# Lets the function be garbage collected when it's safe
				release_global(ObjCInstance(cmd))
			oncomplete = ObjCBlock(c, argtypes=[c_void_p, c_bool])
			# This prevents the oncomplete function from being garbage
			# collected as soon as the play() function exits
			retain_global(oncomplete)
		else:
			oncomplete = None
			
		UIView.animateWithDuration_delay_options_animations_completion_(
		self.duration,
		self.delay,
		self.easing,
		ObjCBlock(self.animation),
		oncomplete
		)
		
		
class ChainedAnimationComponent(Animation):
	def __init__(self, animation_obj, next_animation):
		"""A single step in a chain of animations."""
		self.animation_obj = animation_obj
		self.next_animation = next_animation
		
		self.duration = self.animation_obj.duration
		self.delay = self.animation_obj.delay
		self.animation = self.animation_obj.animation
		self.easing = self.animation_obj.easing
		
		self._completion = None
		
	def completion(self, success):
		# If it has a completion function already, run it first.
		if self.animation_obj.completion is not None:
			self.animation_obj.completion(success)
		# Then play the next animation if we're not at the end of the chain
		if self.next_animation is not None:
			self.next_animation.play()
			
			
class ChainedAnimation(object):
	"""Represents a series of several animations to be played in sequence."""
	def __init__(self, *animations, **kwargs):
		if hasattr(kwargs, 'completion'):
			self.completion = kwargs['completion']
		else:
			self.completion = None
			
		anims = []
		for i, a in reversed(list(enumerate(animations))):
		
			if i == len(animations) - 1:
				# This is the last element in the chain (first in iteration),
				# so it has no successor. We can use the old Animation object.
				anims.append(copy(a))
			else:
				anims.append(ChainedAnimationComponent(copy(a), anims[-1]))
				
		self.anims = anims[::-1]
		
		# Register the completion event on the final component
		
		if self.completion is not None:
			self.anims[-1]._completion = self.completion
			
	def play(self):
		"""Perform the animations."""
		self.anims[0].play()
		
		
def animate(animation, *args, **kwargs):
	"""A drop-in replacement for ui.animate.
	
	This adds support for different easings.
	"""
	Animation(animation, *args, **kwargs).play()

