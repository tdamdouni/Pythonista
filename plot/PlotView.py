# https://gist.github.com/mcarrara3/38abe25c4be131851c14

# Pythonista Plotter
# Version: 1.0
# Author: Matteo Carrara
# Date: 07/22/2014

# Important: to run the code create a ui.View and set its class to PlotView! Enjoy!

import ui
import numpy as np
from math import pi

class PlotView(ui.View):
	def __init__(self, parent = None):
		self.background_color = 'white'
		self.num_spectra = 0
		self.x_set = []
		self.y_set = []
		self.spectrum_colour = []
		self.style = []
		self.line_width = []
		self.x_label = ''
		self.y_label = ''
		self.plot_title = ''
		self.x_lim = []
		self.y_lim = []
		self.x_min = 0
		self.x_max = 1
		self.y_min = 0
		self.y_max = 1
		self.x_offset = 50
		self.y_offset = 50
		self.x_axis_format = '{:.2f}'
		self.y_axis_format = '{:.2f}'
		# y-label
		self.ylabel = ui.Label()
		self.ylabel.width = 1000
		self.ylabel.alignment = ui.ALIGN_CENTER
		self.ylabel.font = ('Helvetica', 15)
		self.ylabel.transform = ui.Transform.rotation(-pi/2)
		self.add_subview(self.ylabel)

	def set_labels(self,x_label,y_label):
		self.x_label = x_label
		self.y_label = y_label

	def set_plot_title(self, plot_title):
		self.plot_title = plot_title

	def axis(self, x_off,y_off, x_dp, y_dp):
			# optional adjustment for x_axis offset, y_axis offset, and decimal places for x-axis labels and y-axis labels
		self.x_offset,self.y_offset = x_off, y_off
		self.x_axis_format = '{:.'+'{:d}'.format(x_dp)+'f}'
		self.y_axis_format = '{:.'+'{:d}'.format(y_dp)+'f}'

	def set_axis_limits(self, xLim, yLim):
		self.x_lim.append(xLim[:])
		self.y_lim.append(yLim[:])

	def set_xy(self, x,y,colour,style, line_width):

		if min(x) < self.x_min: self.x_min = min(x)
		if max(x) > self.x_max: self.x_max = max(x)
		if min(y) < self.y_min: self.y_min = min(y)
		if max(y) > self.y_max: self.y_max = max(y)

		if self.x_lim:
			self.x_min,self.x_max = self.x_lim[0]
		if self.y_lim:
			self.y_min,self.y_max = self.y_lim[0]

		# store the x and y values (they must be numpy arrays)
		x_temp = x[:]
		y_temp = y[:]
		self.x_set.append(x_temp)
		self.y_set.append(y_temp)
		self.spectrum_colour.append(colour)
		self.style.append(style)
		self.line_width.append(line_width)

	def draw(self):
		scale_x = (self.width - 3*self.x_offset) / (self.x_max - self.x_min)
		scale_y = (self.height - 2*self.y_offset) / (self.y_max - self.y_min)
		step_x_axis = scale_x * (self.x_max - self.x_min) / 10
		step_y_axis = scale_y * (self.y_max - self.y_min) / 10

		# draw grid
		for ii in range(9):
			# horizontal grid
			hGridPath = ui.Path()
			ui.set_color('gray')
			hGridPath.move_to(2.*self.x_offset,self.y_offset+step_y_axis*(ii+1))
			hGridPath.line_to(self.width-self.x_offset,self.y_offset+step_y_axis*(ii+1))
			hGridPath.line_width = 0.5
			hGridPath.set_line_dash([5])
			hGridPath.stroke()

			# vertical grid
			vGridPath = ui.Path()
			ui.set_color('gray')
			vGridPath.move_to(2*self.x_offset+step_x_axis*(ii+1),self.y_offset)
			vGridPath.line_to(2*self.x_offset+step_x_axis*(ii+1),self.height-self.y_offset)
			vGridPath.line_width = 0.5
			vGridPath.set_line_dash([5])
			vGridPath.stroke()

		# draw x and y axis
		'''''
		axesPath = ui.Path()
		ui.set_color('black')
		# move to graph (0,0) and add x-axis
		axesPath.move_to(self.x_offset, self.y_offset)
		axesPath.line_to(self.width-self.x_offset, self.y_offset)

		# move to graph origin and add y-axis
		axesPath.move_to(self.x_offset, self.y_offset)
		axesPath.line_to(self.x_offset, self.height-self.y_offset)
		axesPath.stroke()
		'''''

		# draw x and y axis with box
		axesPath = ui.Path()
		ui.set_color('black')
		# move to graph (0,0) and add x-axis
		axesPath.move_to(2*self.x_offset, self.y_offset)
		# top x-axis
		axesPath.line_to(self.width-self.x_offset, self.y_offset)
		# right y-axis
		axesPath.line_to(self.width-self.x_offset, self.height-self.y_offset)
		# bottom x-axis
		axesPath.line_to(2*self.x_offset, self.height-self.y_offset)
		# left y-axis
		axesPath.line_to(2*self.x_offset, self.y_offset)
		axesPath.line_width = 2
		axesPath.stroke()

		# x label
		xLabelRect = (2*self.x_offset, self.height-self.y_offset/2,self.width-3*self.x_offset,self.y_offset)
		ui.draw_string(self.x_label, rect=xLabelRect, font=('Helvetica', 15),alignment=ui.ALIGN_CENTER)

		# y label
		self.ylabel.text = self.y_label
		self.ylabel.center = (self.x_offset/2., self.height/2.)

		# title
		titleRect = (2*self.x_offset, self.y_offset/3, self.width-3*self.x_offset, self.y_offset)
		ui.draw_string(self.plot_title, rect=titleRect, font=('Helvetica', 15),alignment=ui.ALIGN_CENTER)

		# mark the axes
		for i in range(11):

			# REM (0,0) position is top-left in a view, while it's usually bottom-left in a plot

			# top x-axis
			xPath = ui.Path()
			ui.set_color('black')
			xPath.move_to(2*self.x_offset+step_x_axis*i,self.y_offset+5)
			xPath.line_to(2*self.x_offset+step_x_axis*i,self.y_offset)
			xPath.line_width = 2
			xPath.stroke()

			# bottom x-axis
			xbPath = ui.Path()
			ui.set_color('black')
			xbPath.move_to(2*self.x_offset+step_x_axis*i,self.height-self.y_offset-5)
			xbPath.line_to(2*self.x_offset+step_x_axis*i,self.height-self.y_offset)
			xbPath.line_width = 2
			xbPath.stroke()
			# x-axis values
			label = self.x_axis_format.format(self.x_min+i*(self.x_max-self.x_min)/10.)
			stringRect = (2*self.x_offset-6+step_x_axis*i, self.height-self.y_offset,0,13)
			ui.draw_string(label, rect=stringRect, font=('Helvetica', 13), alignment=ui.ALIGN_CENTER)

			# left y-axis
			yPath = ui.Path()
			ui.set_color('black')
			yPath.move_to(2*self.x_offset+5,self.y_offset+step_y_axis*i)
			yPath.line_to(2*self.x_offset,self.y_offset+step_y_axis*i)
			yPath.line_width = 2
			yPath.stroke()
			# y-axis values
			label = self.y_axis_format.format(self.y_min+(10.-i)*(self.y_max-self.y_min)/10.)
			stringRect = (0,self.y_offset-13+step_y_axis*i,2*self.x_offset*0.95,13)
			ui.draw_string(label, rect=stringRect, font=('Helvetica', 13), alignment=ui.ALIGN_RIGHT)

			# right y-axis
			yrPath = ui.Path()
			ui.set_color('black')
			yrPath.move_to(self.width-self.x_offset-5,self.y_offset+step_y_axis*i)
			yrPath.line_to(self.width-self.x_offset,self.y_offset+step_y_axis*i)
			yrPath.line_width = 2
			yrPath.stroke()

		for j in range(len(self.x_set)):

			temp_x = []
			temp_y = []
			temp_colour = []
			temp_x = self.x_set[j] # j-th data set
			temp_y = self.y_set[j] # j-th data set

			dataPath = ui.Path()
			ui.set_color(self.spectrum_colour[j])

			dataPath.move_to(2*self.x_offset+scale_x*(temp_x[0]-self.x_min), self.height - self.y_offset-scale_y*(temp_y[0]-self.y_min))

			dataPath.line_width = float(self.line_width[j])

			for i in range(len(temp_x)):

				draw_x = 2*self.x_offset+scale_x*(temp_x[i]-self.x_min)
				draw_y = self.height -self.y_offset-scale_y*(temp_y[i]-self.y_min)

				if self.style[j] == '-':
					dataPath.line_to(draw_x,draw_y)
					dataPath.stroke()
				elif self.style[j] == '--':
					dataPath.line_to(draw_x,draw_y)
					dataPath.set_line_dash([5])
					dataPath.stroke()
				elif self.style[j] == '-.':
					dataPath.line_to(draw_x,draw_y)
					dataPath.set_line_dash([5, 3, 1, 3])
					dataPath.stroke()
				elif self.style[j] == 'o':
					path = ui.Path.oval(draw_x-3, draw_y-3,6,6)
					ui.set_color(self.spectrum_colour[j])
					path.stroke()
				elif self.style[j] == 'of':
					path = ui.Path.oval(draw_x-3, draw_y-3,6,6)
					ui.set_color(self.spectrum_colour[j])
					path.fill()
				elif self.style[j] == 's':
					path = ui.Path.rect(draw_x-3, draw_y-3,6,6)
					ui.set_color(self.spectrum_colour[j])
					path.stroke()
				elif self.style[j] == 'sf':
					path = ui.Path.rect(draw_x-3, draw_y-3,6,6)
					ui.set_color(self.spectrum_colour[j])
					path.fill()


v = ui.load_view('PlotView')

# data generation
x = np.linspace(-1,1,80)
x2 = np.linspace(-1,1,10)
y1 = np.sin(2*np.pi*x)
y3 = np.cos(2*np.pi*2*x)
y2 = x2

# plot settings MUST be done before loading data into the view
v.set_labels('x axis label [a.u.]','y axis label [a.u.]')
v.set_axis_limits(np.array([-1,1]),np.array([-1,1]))
v.set_plot_title('My plot')

# load data into view
v.set_xy(x2,y2,'blue','-',1)
v.set_xy(x2,y2, 'magenta', 'of',1)
v.set_xy(x,y1,'red','o',1)
v.set_xy(x,y1, 'green', '--',1)
v.set_xy(x,y3, 'orange', '-.',2)
v.set_xy(x,y3, 'violet','sf',1)

v.present()
