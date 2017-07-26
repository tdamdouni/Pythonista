# https://gist.github.com/rlabbe/f9360578ba48606c2c148392bc802304

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

xs = np.linspace(-4, 4, n)
ys = np.linspace(-4, 4, n)

X, Y = np.meshgrid(xs, ys)

# mixture of Gaussians - based on Matlab peaks() function
Z = abs(3*(1-X)**2 * np.exp(-(X**2) - (Y+1)**2) \
        -10*(X/5 - X**3 - Y**5)*np.exp(-X**2-Y**2) \
        - 1/3*np.exp(-(X+1)**2 - Y**2))
        
#3D representation
ax = plt.gca(projection='3d')
ax.plot_surface(X, Y, Z, color='g', rstride=1, cstride=1);
plt.show()


#2D heatmaupu
plt.imshow(Z, cmap='hot')()
