from ui import *
import photos

import sys
sys.path.append('..')

from CV import *
from pathfinding import *
import MazeEditView
reload(MazeEditView)
from MazeEditView import MazeEditView
from StartEndView import StartEndView
from SolutionView import SolutionView

@in_background
def act(sender):
	nv = sender.navigation_view
	p=photos.capture_image()
	#Generate maze map from image
	image=mazeGen.finalScan(p.resize((320,240)))
	
	def f_handle(image):
		'''Callback function for MazeEditView'''
		global edited,sev
		edited=image
		def f_handle_2(start,end):
			sol=SolutionView(edited, start, end)
			nv.push_view(sol)
		sev = StartEndView(image=edited,finished_handler=f_handle_2)
		sev.name='Step 3: Mark Start and End Points'
		sev.right_button_items=[ButtonItem(title='Continue', action=sev.finish)]
		nv.push_view(sev)
		
	#View for editing scan, f_handle is callback for returning edited image	
	mev = MazeEditView(image=image,finished_handler=f_handle)
	mev.name='Step 2: Fix Mistakes'
	mev.right_button_items=[ButtonItem(title='Continue', action=mev.finish)]
	nv.push_view(mev)
	#Problem is here because mev is not closed automatically, code that closes is after wait modal. fix by pushing new view from within callback function. 
	mev.wait_modal()
	sev.wait_modal()
	edited.show()
	
v=View(background_color=(255,255,255),name='Step 1: Capture Image')

startButton=Button(frame=(0,0,350,150), flex= 'LRBT')
startButton.title='start'
startButton.tint_color=(.5,.5,1)
startButton.font = ('Menlo-Bold',100)
startButton.action=act

v.add_subview(startButton)

nav=NavigationView(v)
nav.present(hide_title_bar=1)
