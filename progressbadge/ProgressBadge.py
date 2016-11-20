# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/28d2311cc6b28fe9bec0

from objc_util import *
import time
import notification

APP=UIApplication.sharedApplication()
DISPLAYMODE=0

def setBadge(text):
	APP.setApplicationBadgeString_(text)
	
def getTimeString(seconds):
	seconds=int(seconds)
	if seconds<60:
		return str(seconds)+'s'
	elif seconds<3600:
		return str(seconds/60)+'m'
	else:
		return str(seconds/3600)+'h'
		
class Container:
	def __init__(self):
		self.tasks=[]
		self.updateTime=0
		self.previousValues=[]
		
	def add(self,task):
		self.tasks.append(task)
		task.super=self
		
	@property
	def shouldRefresh(self):
		#Don't attempt to referesh more than twice per second
		return time.time()-self.updateTime>0.5
		
	def update(self):
		self.previousValues.append((time.time(),sum([p.value for p in self.tasks])))
		if self.shouldRefresh:
			#Calculate the percent of all progressbars
			topValue=sum([p.topValue for p in self.tasks])
			totalValue=sum([p.value for p in self.tasks])
			percent=float(totalValue)/float(topValue)*100
			
			
			#Set the badge for display mode 0, estimated time remaining.
			if DISPLAYMODE>0:
				values=self.previousValues
				if len(values)>=5:
					recentTimeRange=values[-1][0]-values[0][0]
					recentValueRange=values[-1][1]-values[0][1]
					changePerSecond=recentValueRange/recentTimeRange
					remainingChange=topValue-totalValue
					seconds=remainingChange/changePerSecond
					badgeStr=getTimeString(seconds)
				else:
					badgeStr='...'
			#Set the badge for display mode 0, percentage.
			else:
				if percent<10:
					badgeStr=str(percent)[:3]+'%'
				elif percent<100:
					badgeStr=str(percent)[:4]+'%'
				else:
					badgeStr='100%'
					
			setBadge(badgeStr)
			self.updateTime=time.time()
			
TASKCONTAINER=Container()

class Progress:
	def __init__(self, topValue=100, title=None, notify=True):
		self.topValue=topValue
		self.value=0
		self.title=title
		self.notify=notify
		self.hasNotified=False
		TASKCONTAINER.add(self)
		
	def update(self,value):
		self.value=value
		self.super.update()
		#Notify the user if notifications are enabled and the task is finished
		if value==self.topValue and self.notify and not self.hasNotified:
			if self.title is None:
				message='Your progressbar has finished!'
			else:
				message='Your progressbar "{}" has finished!'.format(self.title)
			notification.schedule(message)
			self.hasNotified=True
			
	def increment(self,step=1):
		self.update(self.value+step)
		
	def finish(self):
		self.update(self.topValue)
		time.sleep(0.5)
		self.super.update()
		
def setDisplayMode(mode):
	global DISPLAYMODE
	if isinstance(mode,str):
		if 'time' in mode.lower():
			DISPLAYMODE=1
			return
		else:
			DISPLAYMODE=0
	else:
		DISPLAYMODE=mode
		
#Reset badge
def stop():
	setBadge('Done')
	
if __name__=='__main__':
	#This progress counts some value out of 1000
	setDisplayMode('time remaining')
	p1=Progress(200,'Test Progressbar')
	for x in range(201):
		p1.increment()
		time.sleep(0.1)
	stop()

