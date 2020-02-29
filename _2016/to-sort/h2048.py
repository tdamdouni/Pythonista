# -*- coding: utf-8 -*-

# https://gist.github.com/jsbain/4ce5587ea7ef42533027

"""
Created on Sat Jul 12 09:33:29 2014

@author: henryiii
"""
from __future__ import print_function

import random
import numpy as np
import ui
from functools import partial

class GameOver(Exception):
	pass

class Board (object):
	def __init__(self, data=np.zeros((4,4),dtype=int)):
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

	def move(self, dir):
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
			row[:] = vals
			
		return made_move

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
					print('game over')
					break
		else:
			break 
	print('done')
	return board

def _ui_setup(board, labels, v):
	for i in range(board.data.shape[0]):
		for j in range(board.data.shape[1]):
			lab = board.traditional_data[i,j]
			labels[i,j].text = str(lab) if lab else ''
			labels[i,j].background_color = (lab/11.,1-lab/11.,1,.3) if lab else 'white'
	v.name = 'Score: {}'.format(board.score)

def _ui_move(board, labels, v, dir, ext):
	if board.move(dir):
				board.add_tile()
				if not board.check_move():
					print('Game over.')
					print(board)
					v.close()
	_ui_setup(board, labels, v)



class myView(ui.View):
	moves=[None for i in range(4)]   #list containing function handles
	old=(0,0)   #old touch location
	
	def touch_began(self, touch):
		# Called when a touch begins.  store old location
		self.old=touch.location

	def touch_ended(self, touch):
		# Called when a touch ends.
		#   compute vector from old to new touch
		u=[touch.location[i]-self.old[i] for i in range(2)]
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
		self.moves[dir](self)


def run_ui():
	v = myView(frame=(0,0,100,140))
	v.background_color = 'white'
	v.touch_enabled=True
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
			labels[i,j].font = ('<system-bold>',24)
			labels[i,j].frame = (
				100/board.data.shape[1]*(j+.04),
				100/board.data.shape[0]*(i+.04),
				100/board.data.shape[1]*.92,
				100/board.data.shape[0]*.92)
			v.add_subview(labels[i,j])
	_ui_setup(board,labels,v)
	
	for i in range(4):
		but = ui.Button()
		but.title = ('RIGHT','UP','LEFT','DOWN')[i]
		but.frame = ((60,110,20,20),
								(40,100,20,20),
								(20,110,20,20),
								(40,120,20,20))[i]
		but.flex = 'WHTBLR'
		but.action = partial(_ui_move,board,labels,v,i)
		v.add_subview(but)
		v.moves[i]=but.action   #to allow swipes
	
	v.present()

if __name__ == '__main__':
	#self = run_console()
	run_ui()
