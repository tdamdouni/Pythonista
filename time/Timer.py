# coding: utf-8

# https://forum.omz-software.com/topic/1465/help-typeerror-expected-callable-function/7

import ui,time

class stopwatch(ui.View):
	def __init__(self):
		self.frame=(0,0,768,768)
		self.bg_color='white'
		fast=ui.Label(frame=(10,10,200,50),name='fast')
		slow=ui.Label(frame=(10,70,200,50),name='slow')
		stop=ui.Button(frame=(150,150,80,80),bg_color='red',name='stop')
		go=ui.Button(frame=(250,150,80,80),bg_color='green',name='go')
		go.title='go'
		stop.title='stop'
		go.action=self.go
		stop.action=self.stop
		self.add_subview(fast)
		self.add_subview(slow)
		self.add_subview(stop)
		self.add_subview(go)
		self._stopped=True
		
	def stop(self,sender):
		self._stopped=True
		
	def go(self,sender):
		if self._stopped:
			self._stopped=False
			self.fast_loop()
			self.slow_loop()
			
	def fast_loop(self):
		if self.on_screen and not self._stopped:
			self['fast'].text='{:0.14}'.format(time.time())
			r=self['fast'].bg_color[0]
			self['fast'].bg_color=((r+1)%2,1,1)
			ui.delay(self.fast_loop,0.1)
			
	def slow_loop(self):
		if self.on_screen and not self._stopped:
			self['slow'].text='{:0.14}'.format(time.time())
			r=self['slow'].bg_color[0]
			self['slow'].bg_color=((r+1)%2,1,1)
			ui.delay(self.slow_loop,1.0)
			
if __name__=='__main__':
	v=stopwatch()
	v.present()

