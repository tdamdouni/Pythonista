import matplotlib.pyplot as plt
from numpy import linspace, sin, diff
import numpy as np
import scene_drawing as sd
from scene import *
import ui
import time
import motion




class graph(Scene):
	def setup(self, *args, **kwargs):
		#super().__init__(*args,**kwargs)
		self.background_color='white'
		self.xlims = (-10,0)
		self.ylims = (-1,1)
		
		
	def draw(self):
		sd.stroke_weight(0.4)
		sd.fill(255,255,0)
		
		timenow = time.time()
		x = linspace(-10,0,1000)
		y = sin((x-timenow))
		
		#renormalize data
		x,y = self.resize(x,y)

		self.plot(x,y)
				
	def resize(self,x,y):
		x = np.array(x)
		y = np.array(y)
		y = (y - self.ylims[0])/diff(self.ylims)*self.size[1]
		x = (x - self.xlims[0])/diff(self.xlims)*self.size[0]
		return (x,y)
	
	def plot(self,x,y):
		for i in range(len(x) - 1):
			sd.line(x[i],y[i],x[i+1],y[i+1])

if __name__ == '__main__':
	v = ui.load_view()
	v['view1'].scene = graph()
	
	v.present()
