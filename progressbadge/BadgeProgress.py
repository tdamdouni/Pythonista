# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/28d2311cc6b28fe9bec0

from objc_util import *
import time
import notification

app=UIApplication.sharedApplication()

def setBadge(text):
	app.setApplicationBadgeString_(text)
	
	
class Container:
	def __init__(self):
		self.tasks=[]
		self.updateTime=0
		
	def add(self,task):
		self.tasks.append(task)
		task.super=self
		
	@property
	def shouldRefresh(self):
		#Don't attempt to referesh more than twice per second
		return time.time()-self.updateTime>0.5
		
	def update(self):
		if self.shouldRefresh:
			topValue=sum([p.topValue for p in self.tasks])
			totalValue=sum([p.value for p in self.tasks])
			percent=float(totalValue)/float(topValue)*100
			if percent<10:
				percentStr=str(percent)[:3]+'%'
			elif percent<100:
				percentStr=str(percent)[:4]+'%'
			else:
				percentStr='100%'
			setBadge(percentStr)
			self.updateTime=time.time()
			
	def stop(self):
		setBadge('')
		
class Progress:
	def __init__(self, topValue=100, title=None, notify=True):
		self.topValue=topValue
		self.value=0
		self.title=title
		self.notify=notify
		self.super=None
		
	def update(self,value):
		self.value=value
		#Notify the user if notifications are enabled and the task is finished
		if value==self.topValue and self.notify:
			if self.title is None:
				message='Your progressbar has finished!'
			else:
				message='Your progressbar "{}" has finished!'.format(self.title)
			notification.schedule(message)
			
	def increment(self,step=1):
		self.update(self.value+step)
		
	def finish(self):
		self.update(self.topValue)
		time.sleep(0.5)
		self.super.update()
		
if __name__=='__main__':
	#Container for tasks
	container=Container()
	#This progress counts some value out of 1000
	p1=Progress(200,'Test Progressbar')
	container.add(p1)
	#Loop to increment p1
	for x in range(201):
		p1.increment()
		container.update()
		time.sleep(0.1)
	#Make sure the task registers as completed.
	p1.finish()
	container.stop()

