# https://gist.github.com/henryiii/0a58c7e958c1b317f64a
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 09:33:29 2014

@author: henryiii

Added improvents by JonB (swipes), techteej (design), LawAbidingCactus (size)
"""
from __future__ import print_function

import console, random
import numpy as np
from functools import partial
import time
import ui

size = int(console.input_alert('2048','What size?','4'))
#GAME_FONT = 'ClearSans-Bold' # need to install this font, this is what the actual 2048 uses
GAME_FONT = 'AppleSDGothicNeo-Bold' 
COLORS = ((0.93333333333, 0.89411764705, 0.85490196078), (0.93333333333, 0.89411764705, 0.85490196078), (0.9294117647, 0.87843137254, 0.78431372549), (0.94901960784, 0.69411764705, 0.47450980392), (0.96078431372, 0.58431372549, 0.38823529411),(0.96470588235, 0.4862745098, 0.3725490196), (0.96470588235, 0.36862745098, 0.23137254902),(0.9294117647, 0.81176470588, 0.44705882352), (0.9294117647, 0.8, 0.38039215686),(0.9294117647, 0.78431372549, 0.31372549019), (0.9294117647, 0.7725490196, 0.24705882352), (0.9294117647, 0.76078431372, 0.18039215686),) # Add 12 colors here, the first is empty cell

class Board (object):
	def __init__(self, data=np.zeros((size,size),dtype=int)):
		self.data = data

	def add_tile(self):
		data = self.data.reshape(-1)
		locs = np.nonzero(data == 0)[0]
		if len(locs):
			data[random.choice(locs)] = random.randint(1,2)
			return True
		return False
		
	def check_move(self):
		'Checks to see if move available'
		if np.count_nonzero(self.data == 0):
			return True
		for row in self.data:
			if np.count_nonzero(np.ediff1d(row) == 0):
				return True
		for row in self.data.T:
			if np.count_nonzero(np.ediff1d(row) == 0):
				return True
		return False

	def __repr__(self):
		return self.__class__.__name__+ '(' +repr(self.data)  + ')'

	def __str__(self):
		return str(self.traditional_data) + '\nScore: {}'.format(self.score)

	@property
	def traditional_data(self):
		data = 2**self.data
		data[data == 1] = 0
		return data

	@property
	def score(self):
		return (self.traditional_data).sum()

	def move(self, dir, test = False):
		'right,up,left,down as 0,1,2,3'
		made_move = False
		data = self.data
		if dir%2:
			data = data.T
		if (dir-1)//2 != 0:
			data = np.fliplr(data)

		for row in data:
			vals = row[row!=0]
			for n in range(len(vals)-1):
				if vals[n]==vals[n+1]:
					vals[n]+=1
					vals[n+1]=0
			vals = vals[vals!=0]
			vals.resize(row.shape)
			made_move |= not np.all(vals == row)
			if not test:
				row[:] = vals
			
		return made_move

	def directions(self):
		return {x for x in range(4) if self.move(x,True)}
		
	def auto_simple(self, pattern=(0,1,2,3)):
		for d in pattern:
			if self.move(d):
				return True
		return False

def run_console():
	board = Board()
	board.add_tile()
	while True:
		print(board)
		x = raw_input('wasd:').lower()
		if len(x)==1 and x in 'wasd':
			v = 'dwas'.find(x)
			if board.move(v):
				board.add_tile()
				if not board.check_move():
					console.hud_alert('Game over.', 'error', 2.5)
					break
		else:
			break 
	print('Done')
	return board

def _ui_setup(board, labels, v):
	for i in range(board.data.shape[0]):
		for j in range(board.data.shape[1]):
			lab = board.traditional_data[i,j]
			simplelabel = board.data[i,j]
			labels[i,j].text = str(lab) if lab else ''
			labels[i,j].background_color = COLORS[simplelabel]
	v.name = 'Score: {}'.format(board.score)
	
def gameoverhud():
	console.hud_alert('Game over.', 'error', 2.5)
	time.sleep(1)
	
def _ui_move(board, labels, v, dir, sender):
	if board.move(dir):
		board.add_tile()
		if not board.check_move():
			gameoverhud()
			ui.delay(v.close(), 2.5)
		else:
			_ui_setup(board, labels, v)
	
def _ui_move_auto(board, labels, v, sender):
	if board.auto_simple():
		board.add_tile()
		if not board.check_move():
			gameoverhud()
			ui.delay(v.close(), 2.5)
		_ui_setup(board, labels, v)
		_setup_buts(board)
	
def run_ui():	
#	import ui
	class MyView(ui.View):
		moves=[None for i in range(4)]   # list containing function handles
		old=np.array((0,0))  # old touch location
	
		def touch_began(self, touch):
			# Called when a touch begins.  store 	old location
			self.old[:]=touch.location

		def touch_ended(self, touch):
			# Called when a touch ends.
			# compute vector from old to new touch
			u=np.array(touch.location)-self.old
			# first, determine whether x or y moved the most
			if abs(u[0])>abs(u[1]):
				dir=0
			else:
				dir=1
			# then, determine sign
			if u[dir]>0:
				dir+=2 if dir else 0
			else:
				dir+=0 if dir else 2
			# call the appropriate move function
			if u[0]**2 + u[1]**2 > 30**2:
				self.moves[dir](self)
		
	v = MyView(frame=(0,0,100,140))
	v.background_color = (0.98039215686, 0.9725490196, 0.93725490196)
	
	board=Board()
	board.add_tile()
	labels = np.empty_like(board.data,dtype=object)
	for i in range(board.data.shape[0]):
		for j in range(board.data.shape[1]):
			labels[i,j] = ui.Label()
			labels[i,j].flex = 'HWLRTB'
			labels[i,j].alignment = ui.ALIGN_CENTER
			labels[i,j].border_width = 1
			labels[i,j].corner_radius = 2
			labels[i,j].font = (GAME_FONT, 24)
			labels[i,j].text_color = 0.00, 0.00, 0.00
			labels[i,j].frame = (
				100/board.data.shape[1]*(j+.04),
				100/board.data.shape[0]*(i+.04),
				100/board.data.shape[1]*.92,
				100/board.data.shape[0]*.92)
			v.add_subview(labels[i,j])
	_ui_setup(board,labels,v)
	
	for i in range(4):
		v.moves[i] = partial(_ui_move,board,labels,v,i)
		
	but = ui.ButtonItem()
	but.title = 'Auto Move'
	but.action = partial(_ui_move_auto,board,labels,v)
	v.right_button_items = [but]
		
	v.present()

if __name__ == '__main__':
	#self = run_console()
	run_ui()