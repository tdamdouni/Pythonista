# coding: utf-8

# https://forum.omz-software.com/topic/2928/ui-animate-wider-usage/10

from __future__ import print_function
import ui
import time, warnings

class CallMeBack(object):
	'''
	CLASS - CallMeBack
	
	Purpose
	to call a user supplied function 100 times with simlar units of
	elapased time between calls with a number between 0.0 and 1.0 for
	the passed duration.
	
	This is an attempt to mimick the part of @omz's animate function,
	that you can set and forget to get a series of numbers
	between 0 - 1.0 over a specfic duration without binding to any
	attributes. just passes the value to the supplied function/method
	
	its only work in progress. i am certin will have to refactor. i am guessing i will need to have some @classmethod decorators to
	make it as flexible as @omz's ui.animate. this is at least a start.
	
	A pause method? maybe does not make sense
	
	'''
	
	def __init__(self, func, duration = 1.0, begin = True,
	on_completion = None, obj_ref = None):
	
		self.iterations = 0         # a counter of the num of iterations done
		self.duration = duration    # the time to spead 100 callbacks over
		self.time_unit = 0          # 1/100th of the duration
		self._value = 0             # current value
		
		self.func = func                # the callers func that is called
		
		# if supplied, calls this function after the 100 iterations
		self.on_completion = on_completion
		
		self.start_time = 0         # is set once the start method is invoked
		self.finish_time = 0        # used for debug. measure how long we took
		
		self.working = False        # a flag, to protect from being called
																																				# whilst running. we are not reenterant
																																				
		# so its possible to store a reference to a object, which you can
		# recover in the callback function
		self.obj_ref = obj_ref
		
		# start from init with begin = True *arg
		if begin:
			self.start()
			
	def start(self, duration = None):
		# the timing and process start method. can be called from __init__
		# or here externally
		
		# aviod being called while running.
		if self.working:
			warnings.warn('CallMeBack cannot be called whilst it is running.')
			return
			
		# block being called again until we finish
		self.working = True
		
		if duration:
			self.duration = duration
			
		self.start_time = time.time()
		self.time_unit = self.duration / 100.
		
		# would be nice to have exp, log etc...
		ui.delay(self._work_linear(), 0)
		
	def _work_linear(self):
		# the method that is called 100 times at evenlyish time intervals
		# which in turns calls the callers function with numbers 0.0 to 1.0
		
		# i know, this can be better. for now its ok to spell it out
		_expected_time = self.iterations  * self.time_unit
		_real_time =time.time() - self.start_time
		_diff = _expected_time - _real_time
		
		if self.iterations == 100:
			# hmmm, call last time
			self.func(self, 1.0)
			
			# we are finished
			self.finish_time = time.time()
			ui.cancel_delays()
			print('duration {}, total time {}, difference {}'.format(self.duration , self.finish_time - self.start_time,
			(self.finish_time - self.start_time) - self.duration))
			
			# if a completion routine has been defined, is called here
			if self.on_completion:
				self.on_completion(self)
				
			# reset some values, so calling multiple times work
			self.reset()
			self.working = False
			return
			
		# call the callers function with ref to this object and the current
		# value
		self._value = self.iterations / 100.
		self.func(self, self._value)
		self.iterations += 1
		
		# call ui.delay with .95% of the time unit we have.
		# this seems ok at the moment. if a lot of processing happens
		# in the callers function, it will start to fall behind
		# hofully _diff counteracts it
		ui.delay(self._work_linear, (self.time_unit ) + _diff)
		
	@property
	def value(self):
		return self._value
		
	@property
	def finished(self):
		return self.working
		
	def reset(self):
		# reset some vars, in the event we are started again
		self.iterations = 0
		self._value = 0
		self.working = False
		
	def cancel(self, ignore_completion = False, finish_with = None):
		# for manual cancelling
		# finish_with just allows your func to be called a last time
		# with a value like 1.0 Could provide a more appealling effect
		
		ui.cancel_delays()
		if finish_with:
			self.func(finish_with)
			
		if self.on_completion:
			if not ignore_completion:
				self.on_completion(self)

