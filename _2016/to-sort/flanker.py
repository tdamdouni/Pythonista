# https://gist.github.com/jsbain/86effb0ad8d865eb843ec341afe35ef6

# https://forum.omz-software.com/topic/3643/multiscene-switch-image-after-specified-time/3

from scene import *
import random
import sound
from time import time
import logging
logger = logging.getLogger('flanker')
if not logger.handlers:
	hdlr = logging.FileHandler('flanker_log.txt','w')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

correct='game:Beep'
incorrect='game:Clank'

leftarrow=Texture('iob:arrow_left_c_256')
leftarrow.name='left'
rightarrow=Texture('iob:arrow_right_c_256')
rightarrow.name='right'
noarrow=Texture('iob:stop_256')
noarrow.name='noarrow'
arrows=[leftarrow,rightarrow]
class FlankerFrame(Node):
	'''class representing a five frame of images.  middle one is shown after a delay, then all are hidden'''
	def __init__(self,*args,**kwargs):
		Node.__init__(self,*args,**kwargs)
		self.anchor_point=(0,.50)

		dw=self.parent.size.width/7
		self.position=(1.5*dw,self.parent.size.height/2)
		self.slots=[0,]*5
		for i in range(5):
			s=SpriteNode(leftarrow,parent=self, position=(i*dw,0))
			s.scale=dw/s.size.width
			s.alpha=0
			self.slots[i]=s

def FlankAction(initial, middle):
	'''show flanker, wait an initial amount, then a middle amount, then hide'''
	return Action.sequence([Action.fade_to(1,0),Action.wait(initial+middle),Action.fade_to(0,0)])
def MiddleAction(initial,middle):
	'''show blank, wait, then show middle then hide'''
	return Action.sequence([
			Action.wait(initial),
			Action.fade_to(1,0),
			Action.wait(middle),
			Action.group([Action.call(f.arm_buttons,0),Action.fade_to(0,0)])])

class FlankerScene(Scene):
	def setup(self):
		self.F=FlankerFrame(parent=self)
		self.leftbutton=SpriteNode(leftarrow,position=(0,0),parent=self)
		self.leftbutton.anchor_point=(0,0)
		self.rightbutton=SpriteNode(rightarrow,position=(self.size.width,0),parent=self)
		self.rightbutton.anchor_point=(1,0)
		self.go=LabelNode('GO',position=(self.size.width/2,0),parent=self,font=('Arial',72))
		self.go.anchor_point=(0.5,0)
		self.currenttex=None
		self.leftbutton.alpha=.2
		self.rightbutton.alpha=.2
		
		self.armed=False
	def arm_buttons(self):
		self.start_time=time()
		self.armed=True
		self.leftbutton.alpha=1
		self.rightbutton.alpha=1
	def update(self):
		#maybe want to get a more accurate start time, since action did not start running until this frame.  or consider using self.t instead of time()
		pass
	def score(self,tex):
		end_time=time()
		if tex==self.currenttex:
			sound.play_effect(correct)
			self.go.color='green'
			self.go.text='{:2.2f}ms'.format(1000*(end_time-self.start_time))
			logger.info('   Correct:{:2.2f}ms'.format(1000*(end_time-self.start_time)))
		else:
			sound.play_effect(incorrect)
			self.go.text='{:2.2f}ms'.format(1000*(end_time-self.start_time))
			self.go.color='red'
			logger.info('   Incorrect:{:2.2f}ms'.format(1000*(end_time-self.start_time)))
		self.armed=False
	def touch_began(self,touch):
		#todo: 'arm' buttons
		if self.armed:
			if touch.location in self.rightbutton.bbox:
				self.score(rightarrow)				
			elif touch.location in self.leftbutton.bbox:
				self.score(leftarrow)
			return
		if not self.armed and touch.location in self.go.bbox:
			self.setup_test()
		
	def setup_test(self):
		middletex=random.choice(arrows)
		flanktext=random.choice(arrows+[noarrow,])
		for i in [0,1,2,3,4]:
			if i==2:
				self.F.slots[i].run_action(MiddleAction(.2,.2))
				self.F.slots[i].texture=middletex
			else:
				self.F.slots[i].run_action(FlankAction(.2,.2))
				self.F.slots[i].texture=flanktext
		self.currenttex=middletex
		logger.info('flankers:'+flanktext.name+'\tmiddle:'+middletex.name)
		self.leftbutton.alpha=.2
		self.rightbutton.alpha=.2

f=FlankerScene()
run(f)
