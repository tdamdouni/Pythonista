#!python2
# coding: utf-8

# https://forum.omz-software.com/topic/1303/crossword-codeword-grid-query/33

from __future__ import print_function
import ui

# test of view interchanging

def button1_tapped(sender):
	child_view = SecondClass()
	parent_view.add_subview(child_view)
	
	
def button2_tapped(sender):
	print('button2 tapped')
	
class FirstClass(ui.View):

	def __init__(self):
		self.present()
		self.background_color = 'black'
		button1 = ui.Button(frame = (1, 1, self.width, self.height))
		print('parent_view started at ', self.width)
		button1.title = 'First Class'
		self.add_subview(button1)
		button1.action = button1_tapped
		
		
class SecondClass (ui.View):

	def __init__(self):
		print('parent_view now = ', parent_view.width)
		self.background_color = 'white'
		button2 =ui.Button(frame = (1, 1, parent_view.width, parent_view.height))
		button2.title = 'Second Class'
		parent_view.add_subview(button2)
		button2.action = button2_tapped
		
		
		
parent_view = FirstClass()

# --------------------

import ui

# test of view interchanging

def button1_tapped(sender):
	root_view = sender.superview.superview
	for subview in root_view.subviews:
		root_view.remove_subview(subview)
	root_view.add_subview(SecondClass(root_view.bounds))
	
def button2_tapped(sender):
	print('button2 tapped')
	
class FirstClass(ui.View):
	def __init__(self, in_frame):
		self.frame = in_frame
		self.background_color = 'black'
		button1 = ui.Button(frame = (1, 1, self.width, self.height))
		print('FirstClass frame is ', self.frame)
		button1.title = 'First Class'
		self.add_subview(button1)
		button1.action = button1_tapped
		
class SecondClass(ui.View):
	def __init__(self, in_frame):
		self.frame = in_frame
		print('SecondClass frame is ', self.frame)
		self.background_color = 'white'
		button2 =ui.Button(frame = (1, 1, self.width, self.height))
		button2.title = 'Second Class'
		self.add_subview(button2)
		button2.action = button2_tapped
		
parent_view = ui.View()
parent_view.present()
parent_view.add_subview(FirstClass(parent_view.bounds))

# --------------------

# --------------------
import ui

def button_tapped(sender):
	sender.send_to_back()
	
parent_view = ui.View()
parent_view.hidden = True
buttons = [ui.Button(), ui.Button(), ui.Button(), ui.Button()]
for i, b in enumerate(buttons):
	b.bg_color = 'white'
	b.action = button_tapped
	b.flex = 'WH'
	b.frame = (25, 25, 200, 200)
	b.name = b.title = 'Button {}'.format(i)
	parent_view.add_subview(b)
	b.send_to_back()  # start with FIFO order
parent_view.present()
parent_view.hidden = False

# --------------------

import ui, console

def button_tapped(sender):
	sender.superview.send_to_back()
	print(sender.name)
	
class FirstClass(ui.View):
	def __init__(self):
		self.background_color = 'blue'
		button = ui.Button(frame = (0, 0, 1, 1), title = 'Class 1')
		button.name = button.title
		button.bg_color = 'white'
		button.flex  = 'WH'
		self.add_subview(button)
		button.action = button_tapped
		
class SecondClass(ui.View):
	def __init__(self):
		self.background_color = 'red'
		button = ui.Button(frame = (0, 0, 1, 1), title = 'Class 2')
		button.name = button.title
		button.bg_color = 'white'
		button.flex = 'WH'
		self.add_subview(button)
		button.action = button_tapped
		
parent_view = ui.View()
grids = [FirstClass(), SecondClass()]
for i, b in enumerate(grids):
	#b.frame = (0, 0, parent_view.width, parent_view.height)
	b.flex = 'WH'
	parent_view.add_subview(b)
	b.send_to_back()
	
parent_view.present('full_screen')

# --------------------

import ui

def button_tapped(sender):
	sender.superview.send_to_back()
	print(sender.name)
	
def make_button(in_title='Untitled'):
	button = ui.Button(title=in_title)
	button.action = button_tapped
	button.bg_color = 'white'
	button.flex = 'TLBR'
	button.name = button.title
	return button
	
class FirstClass(ui.View):
	def __init__(self, in_frame):
		self.frame = in_frame
		self.bg_color = 'blue'
		self.flex = 'WH'
		button = make_button('Class 1')
		button.center = self.center
		self.add_subview(button)
		
class SecondClass(ui.View):
	def __init__(self, in_frame):
		self.frame = in_frame
		self.bg_color = 'red'
		self.flex = 'WH'
		button = make_button('Class 2')
		button.center = self.center
		self.add_subview(button)
		
parent_view = ui.View()
parent_view.hidden = True
print((parent_view.bounds, parent_view.frame))
parent_view.present()
print((parent_view.bounds, parent_view.frame))
grids = [FirstClass(parent_view.bounds),
         SecondClass(parent_view.bounds)]
for grid in grids:
	parent_view.add_subview(grid)
	grid.send_to_back()
parent_view.hidden = False

# --------------------

import ui
class MyView(ui.View):
	def __init__(self):
		print('__init__()')
	def layout(self):
		print('layout()')
MyView().present()

# --------------------

