# https://twitter.com/pteras14/status/793033736170373120/photo/1

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
	return 1/(1+np.exp(-x))

x= np.arrange(-5.0,5.0,0.1)
y=sigmoid(x)
plt.plot(x,y)
plt.ylim(-0.1,1.1)
plt.show()
