# https://forum.omz-software.com/topic/3611/how-to-update-an-existing-plot-in-pythonista

import numpy as np
import time
import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure()
tstart = time.time()               # for profiling
x = np.arange(0,2*np.pi,0.01)      # x-array
line, = plt.plot(x,np.sin(x))
for i in np.arange(1,200):
	line.set_ydata(np.sin(x+i/10.0))  # update the data
	plt.draw()
	fig.canvas.flush_events()
	plt.pause(0.001)  #redraw figure, allow GUI to handle events
	
print ('FPS:' , 200/(time.time()-tstart))
plt.ioff()
plt.show()

