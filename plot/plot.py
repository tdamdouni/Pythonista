# simple plot class for 1-d plotting on iPad.

# https://gist.github.com/anonymous/4e792e1194816431f053

import canvas

class plot:
	def __init__(self):
		self.num_spectra = 0
		self.x_set = []
		self.y_set = []
		self.spectrum_colour = []
		self.style = []
		self.x_min = 1000000.0
		self.x_max = 0
		self.y_min = 1000000.0
		self.y_max = 0
		canvas.set_size(688, 688)
		self.x_offset = 50
		self.y_offset = 30
		self.x_axis_format = '{:.1f}'
		self.y_axis_format = '{:.1f}'
		
	def axis(self,x_off,y_off,x_dp,y_dp):
		# optional adjustment for x_axis offset, y-axis offset, 
		# and decimal places for x-axis labels and y-axis labels
		self.x_offset,self.y_offset=x_off,y_off
		self.x_axis_format = '{:.'+'{:d}'.format(x_dp)+'f}'
		self.y_axis_format = '{:.'+'{:d}'.format(y_dp)+'f}'
		
	def set_xy(self,x,y,colour,style):
		if min(x) < self.x_min: self.x_min = min(x)
		if min(y) < self.y_min: self.y_min = min(y)
		if max(x) > self.x_max: self.x_max = max(x)
		if max(y) > self.y_max: self.y_max = max(y)
		
		# store the x and the y values
		x_temp = x[:]
		y_temp = y[:]
		self.x_set.append(x_temp)
		self.y_set.append(y_temp)
		self.spectrum_colour.append(colour)
		self.style.append(style)
		
	def plot_spectra(self):
		# calculate scale and axis label steps:
		scale_x = (688.0-2*self.x_offset) / (self.x_max - self.x_min)
		scale_y = (688.0-2*self.y_offset) / (self.y_max - self.y_min)
		step_x = scale_x*(self.x_max-self.x_min)/10
		step_y = scale_y*(self.y_max-self.y_min)/10
		
		# Draw x and y axix:
		canvas.set_stroke_color(0,0,0)
		# x-axis
		canvas.draw_line(self.x_offset,self.y_offset,688,self.y_offset)
		# y-axis
		canvas.draw_line(self.x_offset,self.y_offset,self.x_offset,688)
	
		# label and mark the axes..
		for i in range(11):
			canvas.set_fill_color(0,0,0)
			# x-axis...
			label =  self.x_axis_format.format(self.x_min+i*(self.x_max-self.x_min)/10)
			canvas.draw_text(label,self.x_offset+step_x*i,0, font_name='Helvetica',font_size=16)
			canvas.draw_line(self.x_offset+step_x*i,self.y_offset-5, self.x_offset+step_x*i,self.y_offset)
			
			# y-axis...
			label = self.y_axis_format.format(self.y_min+i*(self.y_max-self.y_min)/10)
			canvas.draw_text(label,0,self.y_offset+step_y*i, font_name='Helvetica',font_size=16)
			canvas.draw_line(self.x_offset-5,self.y_offset+step_y*i, self.x_offset,self.y_offset+step_y*i)
			
		# draw each dataset...
		for j in range(len(self.x_set)):
			temp_x = []
			temp_y = []
			temp_colour = []
			temp_x = self.x_set[j]
			temp_y = self.y_set[j]
			
			canvas.set_stroke_color(*self.spectrum_colour[j])
			canvas.set_line_width(2)
			canvas.move_to(self.x_offset+scale_x * (temp_x[0]-self.x_min), self.y_offset+scale_y * (temp_y[0]-self.y_min))
			
			for i in range(len(temp_x)):
				draw_x = self.x_offset+scale_x * (temp_x[i]-self.x_min)
				draw_y = self.y_offset+scale_y * (temp_y[i]-self.y_min)
				if (self.style[j] == '-'):	
					canvas.add_line(draw_x, draw_y)
				if (self.style[j] == 'o'):
					canvas.add_ellipse(draw_x-3,draw_y-3,6,6)
			canvas.draw_path()

# usage...
option = 0

if option == 0:
	p = plot()
	p.axis(50,30,2,2) # optional axis adjustment
	
	# pass in [x...][y...][r,g,b] to plot as red points 'o'...
	p.set_xy([2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0], [1.0,1.0,2.0,4.0,9.0,10.0,9.0,4.0,2.0,1.0],[1,0,0],'o')
	
	# pass in another [x...][y...][r,g,b] to plot as black line '-'...
	p.set_xy([2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0], [1.0,1.0,2.0,4.0,9.0,10.0,9.0,4.0,2.0,1.0],[0,0,0],'-')
	
	# plot all datasets...
	p.plot_spectra()

